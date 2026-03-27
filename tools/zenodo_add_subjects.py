#!/usr/bin/env python3
"""
Add controlled-vocabulary subjects to a Zenodo deposit via the deposit API.

The Zenodo GitHub integration (.zenodo.json) does not support the subjects
field, so this script is called by a GitHub Action after each release to
patch subjects into the newly created deposit.

Usage (manual):
    ZENODO_TOKEN=<token> python3 tools/zenodo_add_subjects.py [--release-tag v1.1.1]

Environment variables:
    ZENODO_TOKEN   Required. Zenodo personal access token.
    RELEASE_TAG    Optional. GitHub release tag to match (e.g. "v1.1.1").
                   If set, the script verifies the deposit version matches
                   before editing. Can also be passed as --release-tag.

Exit codes:
    0  Success
    1  Error (deposit not found, API failure, etc.)
"""

import json
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

# ---------------------------------------------------------------------------
# Subjects to add — edit this list to change what appears on Zenodo
# ---------------------------------------------------------------------------
SUBJECTS = [
    {
        "term": "Botany",
        "scheme": "MeSH",
        "identifier": "https://id.nlm.nih.gov/mesh/D001901",
    },
    {
        "term": "Wood anatomy",
        "scheme": "MeSH",
        "identifier": "https://id.nlm.nih.gov/mesh/D014934",
    },
    {
        "term": "Biogeography",
        "scheme": "GEMET",
        "identifier": "https://www.eionet.europa.eu/gemet/en/concept/836",
    },
    {
        "term": "Biodiversity conservation",
        "scheme": "GEMET",
        "identifier": "https://www.eionet.europa.eu/gemet/en/concept/15073",
    },
]

# Zenodo concept record ID (the number in the concept DOI 10.5281/zenodo.XXXXX)
CONCEPT_RECID = "18687469"

ZENODO_API = "https://zenodo.org/api"
MAX_ATTEMPTS = 10
RETRY_DELAY = 30  # seconds between polling attempts


# ---------------------------------------------------------------------------
# API helpers
# ---------------------------------------------------------------------------

def api_request(path: str, method: str = "GET", data: dict = None, token: str = "") -> dict:
    """Make an authenticated Zenodo API request. Raises on HTTP errors."""
    url = f"{ZENODO_API}{path}"
    body = json.dumps(data).encode() if data is not None else None
    req = urllib.request.Request(
        url,
        data=body,
        method=method,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as exc:
        body_text = exc.read().decode(errors="replace")
        print(f"  HTTP {exc.code} {exc.reason}: {body_text[:300]}")
        raise


# ---------------------------------------------------------------------------
# Main logic
# ---------------------------------------------------------------------------

def find_deposit(token: str, release_tag: str) -> dict:
    """Poll Zenodo until the new deposit for CONCEPT_RECID appears."""
    # Strip leading 'v' from tag for version comparison
    expected_version = release_tag.lstrip("v") if release_tag else ""

    print(f"Polling Zenodo for deposit (concept {CONCEPT_RECID})...")
    for attempt in range(1, MAX_ATTEMPTS + 1):
        deposits = api_request(
            f"/deposit/depositions?q=conceptrecid:{CONCEPT_RECID}&sort=mostrecent&size=1",
            token=token,
        )
        if deposits:
            dep = deposits[0]
            dep_id = dep["id"]
            dep_version = dep.get("metadata", {}).get("version", "")
            if expected_version and expected_version not in dep_version:
                print(
                    f"  Attempt {attempt}/{MAX_ATTEMPTS}: deposit {dep_id} "
                    f"has version {dep_version!r}, expected {expected_version!r} — waiting..."
                )
            else:
                label = f"version {dep_version!r}" if dep_version else "no version field"
                print(f"  Found deposit {dep_id} ({label})")
                return dep
        else:
            print(f"  Attempt {attempt}/{MAX_ATTEMPTS}: no deposits found — waiting...")

        if attempt < MAX_ATTEMPTS:
            time.sleep(RETRY_DELAY)

    print(
        f"ERROR: Could not find a matching Zenodo deposit after "
        f"{MAX_ATTEMPTS * RETRY_DELAY // 60} minutes."
    )
    sys.exit(1)


def add_subjects(token: str, deposit: dict) -> None:
    dep_id = deposit["id"]
    state = deposit.get("state", "unknown")

    # Published records must be put into edit mode first
    if state == "done":
        print(f"  Deposit {dep_id} is published — requesting edit mode...")
        api_request(f"/deposit/depositions/{dep_id}/actions/edit", method="POST", token=token)
    elif state == "inprogress":
        print(f"  Deposit {dep_id} is still a draft — no edit action needed.")
    else:
        print(f"  Deposit {dep_id} has unexpected state {state!r} — attempting edit anyway...")
        try:
            api_request(f"/deposit/depositions/{dep_id}/actions/edit", method="POST", token=token)
        except urllib.error.HTTPError:
            pass  # May already be editable

    # Fetch current metadata
    print("  Fetching current metadata...")
    dep_data = api_request(f"/deposit/depositions/{dep_id}", token=token)
    metadata = dep_data["metadata"]

    # Patch in subjects
    metadata["subjects"] = SUBJECTS
    print(f"  Writing {len(SUBJECTS)} subjects...")
    api_request(
        f"/deposit/depositions/{dep_id}",
        method="PUT",
        data={"metadata": metadata},
        token=token,
    )

    # Re-publish
    print("  Re-publishing deposit...")
    api_request(f"/deposit/depositions/{dep_id}/actions/publish", method="POST", token=token)

    print("✓ Subjects added successfully:")
    for s in SUBJECTS:
        print(f"    {s['term']}  ({s['scheme']}  {s['identifier']})")


def main() -> None:
    # Parse --release-tag argument if provided
    release_tag = os.environ.get("RELEASE_TAG", "")
    args = sys.argv[1:]
    if "--release-tag" in args:
        idx = args.index("--release-tag")
        if idx + 1 < len(args):
            release_tag = args[idx + 1]

    token = os.environ.get("ZENODO_TOKEN", "")
    if not token:
        print("ERROR: ZENODO_TOKEN environment variable is not set.")
        sys.exit(1)

    deposit = find_deposit(token, release_tag)
    add_subjects(token, deposit)


if __name__ == "__main__":
    main()
