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
    ZENODO_TOKEN=<token> python3 tools/zenodo_add_subjects.py --record-id 19264950

Environment variables:
    ZENODO_TOKEN   Required. Zenodo personal access token with deposit:actions scope.
    RELEASE_TAG    Optional. GitHub release tag to match (e.g. "v1.1.1").
                   Verifies the record version matches before editing.
                   Can also be passed as --release-tag.

Arguments:
    --record-id ID    Skip polling; patch the record with this specific Zenodo
                      record ID directly. Useful for fixing older versions or
                      testing without creating a new release.

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

    # Step 1: Create an edit draft (InvenioRDM API).
    # The POST response contains minimal metadata for legacy records, so we
    # always follow up with a GET to retrieve the full current metadata.
    print(f"  Creating edit draft for record {rec_id}...")
    try:
        api_request(f"/records/{rec_id}/draft", method="POST", token=token)
    except urllib.error.HTTPError as exc:
        if exc.code == 409:
            print("  Draft already exists — continuing...")
        else:
            raise

    # Step 2: GET the draft to obtain the full InvenioRDM metadata.
    draft = api_request(f"/records/{rec_id}/draft", token=token)

    # Step 3: Build updated subjects list.
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

    # Step 4: PUT the updated draft.
    # Send only metadata and custom_fields to avoid overwriting system fields.
    metadata = draft.get("metadata", {})
    metadata["subjects"] = new_subjects
    put_body = {"metadata": metadata}
    if "custom_fields" in draft:
        put_body["custom_fields"] = draft["custom_fields"]

    api_request(f"/records/{rec_id}/draft", method="PUT", data=put_body, token=token)

    # Step 5: Publish the draft.
    print("  Publishing draft...")
    api_request(f"/records/{rec_id}/draft/actions/publish", method="POST", token=token)

    print("✓ Vocabulary subjects added:")
    for s in SUBJECTS:
        print(f"    {s['id']}")


def main() -> None:
    args = sys.argv[1:]

    token = os.environ.get("ZENODO_TOKEN", "")
    if not token:
        print("ERROR: ZENODO_TOKEN environment variable is not set.")
        sys.exit(1)

    # --debug: dump the raw draft JSON for a record and exit (for troubleshooting)
    if "--debug" in args:
        idx = args.index("--debug")
        if idx + 1 >= len(args):
            print("ERROR: --debug requires a record ID argument.")
            sys.exit(1)
        rec_id = args[idx + 1]
        print(f"Creating draft for {rec_id} and dumping response...")
        try:
            api_request(f"/records/{rec_id}/draft", method="POST", token=token)
        except urllib.error.HTTPError as exc:
            if exc.code != 409:
                raise
        draft = api_request(f"/records/{rec_id}/draft", token=token)
        print(json.dumps(draft, indent=2))
        return

    # --record-id bypasses polling and targets a specific record directly
    if "--record-id" in args:
        idx = args.index("--record-id")
        if idx + 1 >= len(args):
            print("ERROR: --record-id requires a record ID argument.")
            sys.exit(1)
        record_id = args[idx + 1]
        print(f"Targeting record {record_id} directly (--record-id).")
        add_subjects(token, {"id": record_id})
        return

    # Normal flow: poll for the latest record, optionally matching a release tag
    release_tag = os.environ.get("RELEASE_TAG", "")
    if "--release-tag" in args:
        idx = args.index("--release-tag")
        if idx + 1 < len(args):
            release_tag = args[idx + 1]

    record = find_record(token, release_tag)
    add_subjects(token, record)


if __name__ == "__main__":
    main()
