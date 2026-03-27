#!/usr/bin/env python3
"""
Add controlled-vocabulary subjects to a Zenodo record via the InvenioRDM API.

The Zenodo GitHub integration (.zenodo.json) does not support vocabulary
subjects. This script is called by a GitHub Action after each release to
patch subjects into the newly created record using the InvenioRDM records API.

Subjects are set as {"id": "scheme:identifier"} — Zenodo expands these
automatically to include the full term, scheme, and identifier metadata.
This matches exactly what subjects added through the Zenodo UI look like.

Keywords (plain-text subjects from .zenodo.json) are preserved untouched.
Any legacy subjects in {term, scheme, identifier} format are removed.

Usage (manual):
    ZENODO_TOKEN=<token> python3 tools/zenodo_add_subjects.py [--release-tag v1.1.1]

Environment variables:
    ZENODO_TOKEN   Required. Zenodo personal access token with deposit:actions scope.
    RELEASE_TAG    Optional. GitHub release tag to match (e.g. "v1.1.1").
                   Verifies the record version matches before editing.
                   Can also be passed as --release-tag.

Exit codes:
    0  Success
    1  Error (record not found, API failure, etc.)
"""

import json
import os
import sys
import time
import urllib.error
import urllib.request

# ---------------------------------------------------------------------------
# Subjects to add — edit this list to change what appears on Zenodo.
# Use the InvenioRDM vocabulary ID format: {"id": "scheme:identifier"}
# Zenodo expands these automatically into full vocabulary entries.
#
# To find a GEMET concept ID: https://www.eionet.europa.eu/gemet/en/concept/
# To find a MeSH concept ID:  https://id.nlm.nih.gov/mesh/
# ---------------------------------------------------------------------------
SUBJECTS = [
    {"id": "mesh:D001901"},        # Botany
    {"id": "mesh:D014934"},        # Wood (anatomy)
    {"id": "gemet:concept/836"},   # Biogeography
    {"id": "gemet:concept/15073"}, # Biodiversity conservation
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
        print(f"  HTTP {exc.code} {exc.reason}: {body_text[:400]}")
        raise


# ---------------------------------------------------------------------------
# Main logic
# ---------------------------------------------------------------------------

def find_record(token: str, release_tag: str) -> dict:
    """Poll Zenodo until the new record for CONCEPT_RECID appears."""
    expected_version = release_tag.lstrip("v") if release_tag else ""

    print(f"Polling Zenodo for record (concept {CONCEPT_RECID})...")
    for attempt in range(1, MAX_ATTEMPTS + 1):
        # Use legacy deposit API to find the record ID
        deposits = api_request(
            f"/deposit/depositions?q=conceptrecid:{CONCEPT_RECID}&sort=mostrecent&size=1",
            token=token,
        )
        if deposits:
            dep = deposits[0]
            rec_id = dep["id"]
            dep_version = dep.get("metadata", {}).get("version", "")
            if expected_version and expected_version not in dep_version:
                print(
                    f"  Attempt {attempt}/{MAX_ATTEMPTS}: record {rec_id} "
                    f"has version {dep_version!r}, expected {expected_version!r} — waiting..."
                )
            else:
                label = f"version {dep_version!r}" if dep_version else "no version field"
                print(f"  Found record {rec_id} ({label})")
                return dep
        else:
            print(f"  Attempt {attempt}/{MAX_ATTEMPTS}: no records found — waiting...")

        if attempt < MAX_ATTEMPTS:
            time.sleep(RETRY_DELAY)

    print(
        f"ERROR: Could not find a matching Zenodo record after "
        f"{MAX_ATTEMPTS * RETRY_DELAY // 60} minutes."
    )
    sys.exit(1)


def add_subjects(token: str, record: dict) -> None:
    """Patch vocabulary subjects into a record using the InvenioRDM records API."""
    rec_id = record["id"]

    # Step 1: Create an edit draft (InvenioRDM API)
    # If a draft already exists this returns HTTP 409; fall back to GET.
    print(f"  Creating edit draft for record {rec_id}...")
    try:
        draft = api_request(f"/records/{rec_id}/draft", method="POST", token=token)
    except urllib.error.HTTPError as exc:
        if exc.code == 409:
            print("  Draft already exists — fetching it...")
            draft = api_request(f"/records/{rec_id}/draft", token=token)
        else:
            raise

    # Step 2: Build updated subjects list.
    # Keep plain-text keyword subjects {"subject": "..."} unchanged.
    # Remove legacy {term, scheme, identifier} entries and old {id: "..."} entries.
    # Add our vocabulary subjects.
    current_subjects = draft.get("metadata", {}).get("subjects", [])
    keyword_subjects = [
        s for s in current_subjects
        if list(s.keys()) == ["subject"]  # only keep bare {"subject": "..."} entries
    ]
    new_subjects = keyword_subjects + SUBJECTS

    print(
        f"  Subjects: {len(keyword_subjects)} keywords preserved, "
        f"{len(SUBJECTS)} vocabulary subjects added."
    )

    # Step 3: PUT the updated draft.
    # Send only metadata and custom_fields to avoid overwriting system fields.
    metadata = draft.get("metadata", {})
    metadata["subjects"] = new_subjects
    put_body = {"metadata": metadata}
    if "custom_fields" in draft:
        put_body["custom_fields"] = draft["custom_fields"]

    api_request(f"/records/{rec_id}/draft", method="PUT", data=put_body, token=token)

    # Step 4: Publish the draft.
    print("  Publishing draft...")
    api_request(f"/records/{rec_id}/draft/actions/publish", method="POST", token=token)

    print("✓ Vocabulary subjects added:")
    for s in SUBJECTS:
        print(f"    {s['id']}")


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

    record = find_record(token, release_tag)
    add_subjects(token, record)


if __name__ == "__main__":
    main()
