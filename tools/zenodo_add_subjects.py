#!/usr/bin/env python3
"""
Add controlled-vocabulary subjects to a Zenodo record via the InvenioRDM API.

The Zenodo GitHub integration (.zenodo.json) does not support vocabulary
subjects. This script is called by a GitHub Action after each release to
patch subjects into the newly created record using the InvenioRDM records API.

Subjects are set as {"id": "scheme:identifier"} — Zenodo expands these
automatically to include the full term, scheme, and identifier metadata.
This matches exactly what subjects added through the Zenodo UI look like.

Records created by the GitHub integration store metadata in legacy format.
This script reads the full metadata from the legacy deposit API, transforms
it to InvenioRDM format, adds vocabulary subjects, and publishes the draft.

Usage (manual):
    ZENODO_TOKEN=<token> python3 tools/zenodo_add_subjects.py
    ZENODO_TOKEN=<token> python3 tools/zenodo_add_subjects.py --release-tag v1.2.0
    ZENODO_TOKEN=<token> python3 tools/zenodo_add_subjects.py --record-id 19264950

Environment variables:
    ZENODO_TOKEN   Required. Zenodo personal access token with deposit:actions scope.
    RELEASE_TAG    Optional. GitHub release tag to match (e.g. "v1.2.0").
                   Verifies the record version matches before editing.
                   Can also be passed as --release-tag.

Arguments:
    --record-id ID    Target a specific Zenodo record ID directly, bypassing
                      the polling loop. Useful for fixing older versions or
                      testing without creating a new release.
    --debug ID        Dump the InvenioRDM draft and legacy deposit JSON for
                      a record and exit (for troubleshooting).

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
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent

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

# Maps legacy relation strings to InvenioRDM relation_type IDs
RELATION_MAP = {
    "isSupplementTo": "issupplementto",
    "isPartOf": "ispartof",
    "hasPart": "haspart",
    "cites": "cites",
    "isCitedBy": "iscitedby",
    "isNewVersionOf": "isnewversionof",
    "isPreviousVersionOf": "ispreviousversionof",
    "isIdenticalTo": "isidenticalto",
    "isDerivedFrom": "isderivedfrom",
    "isSourceOf": "issourceof",
}

# Maps legacy license IDs to InvenioRDM SPDX IDs
LICENSE_MAP = {
    "cc-zero": "cc0-1.0",
    "cc-by": "cc-by-4.0",
    "cc-by-sa": "cc-by-sa-4.0",
    "cc-by-nc": "cc-by-nc-4.0",
    "cc-by-nc-sa": "cc-by-nc-sa-4.0",
    "cc-by-nd": "cc-by-nd-4.0",
}

# Maps legacy contributor type strings to InvenioRDM role IDs
ROLE_MAP = {
    "ProjectMember": "projectmember",
    "DataCollector": "datacollector",
    "DataCurator": "datacurator",
    "DataManager": "datamanager",
    "Editor": "editor",
    "Producer": "producer",
    "Researcher": "researcher",
    "Supervisor": "supervisor",
    "Other": "other",
}


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
        print(f"  HTTP {exc.code} {exc.reason}: {body_text[:500]}")
        raise


# ---------------------------------------------------------------------------
# Legacy → InvenioRDM metadata transformation
# ---------------------------------------------------------------------------

def _transform_person(person: dict) -> dict:
    """Transform a legacy creator/contributor dict to InvenioRDM person format."""
    name = person.get("name", "")
    p = {"person_or_org": {"type": "personal", "name": name}}
    if ", " in name:
        family, given = name.split(", ", 1)
        p["person_or_org"]["family_name"] = family
        p["person_or_org"]["given_name"] = given
    if "orcid" in person:
        p["person_or_org"]["identifiers"] = [
            {"identifier": person["orcid"], "scheme": "orcid"}
        ]
    if "affiliation" in person:
        p["affiliations"] = [{"name": person["affiliation"]}]
    return p


def legacy_to_invenio(legacy: dict, vocabulary_subjects: list) -> dict:
    """
    Transform legacy deposit metadata to InvenioRDM format and attach subjects.

    vocabulary_subjects: list of {"id": "scheme:id"} entries to add.
    Keywords from legacy["keywords"] are prepended as {"subject": "..."} entries.
    """
    meta = {}

    # Scalar fields that map directly
    for field in ("title", "description", "publication_date", "publisher", "version"):
        if field in legacy:
            meta[field] = legacy[field]

    # Resource type: legacy upload_type string → InvenioRDM id object
    upload_type = legacy.get("upload_type", "dataset")
    meta["resource_type"] = {"id": upload_type}

    # Creators
    meta["creators"] = [_transform_person(c) for c in legacy.get("creators", [])]

    # Contributors
    contributors = []
    for c in legacy.get("contributors", []):
        entry = _transform_person(c)
        role_id = ROLE_MAP.get(c.get("type", "Other"), "other")
        entry["role"] = {"id": role_id}
        contributors.append(entry)
    meta["contributors"] = contributors

    # License → rights
    if "license" in legacy:
        lic_id = LICENSE_MAP.get(legacy["license"], legacy["license"])
        meta["rights"] = [{"id": lic_id}]

    # Related identifiers
    related = []
    for ri in legacy.get("related_identifiers", []):
        new_ri = {
            "identifier": ri["identifier"],
            "scheme": ri.get("scheme", "url"),
        }
        if "relation" in ri:
            rel_id = RELATION_MAP.get(ri["relation"], ri["relation"].lower())
            new_ri["relation_type"] = {"id": rel_id}
        if "resource_type" in ri:
            new_ri["resource_type"] = {"id": ri["resource_type"]}
        related.append(new_ri)
    if related:
        meta["related_identifiers"] = related

    # Subjects: keywords as plain-text entries + vocabulary subjects
    keyword_subjects = [{"subject": kw} for kw in legacy.get("keywords", [])]
    meta["subjects"] = keyword_subjects + vocabulary_subjects

    return meta


# ---------------------------------------------------------------------------
# Main logic
# ---------------------------------------------------------------------------

def find_record(token: str, release_tag: str) -> dict:
    """Poll Zenodo until the new record for CONCEPT_RECID appears."""
    expected_version = release_tag.lstrip("v") if release_tag else ""

    print(f"Polling Zenodo for record (concept {CONCEPT_RECID})...")
    for attempt in range(1, MAX_ATTEMPTS + 1):
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
    print(f"  Creating edit draft for record {rec_id}...")
    try:
        api_request(f"/records/{rec_id}/draft", method="POST", token=token)
    except urllib.error.HTTPError as exc:
        if exc.code == 409:
            print("  Draft already exists — continuing...")
        else:
            raise

    # Step 2: Fetch full metadata from the legacy deposit API.
    # The InvenioRDM draft for GitHub-integration records contains only minimal
    # metadata. The legacy deposit API has the complete data (creators, keywords,
    # license, related identifiers, etc.) populated from .zenodo.json.
    print("  Fetching full metadata from legacy deposit API...")
    deposit = api_request(f"/deposit/depositions/{rec_id}", token=token)
    legacy_meta = deposit.get("metadata", {})

    # Step 3: Transform to InvenioRDM format and add vocabulary subjects.
    invenio_meta = legacy_to_invenio(legacy_meta, SUBJECTS)
    keyword_count = len(legacy_meta.get("keywords", []))
    print(
        f"  Subjects: {keyword_count} keywords + {len(SUBJECTS)} vocabulary subjects."
    )

    # Step 4: PUT the updated draft.
    # Also preserve any existing custom_fields (e.g. code:codeRepository).
    draft = api_request(f"/records/{rec_id}/draft", token=token)
    put_body = {"metadata": invenio_meta}
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

    # --debug: dump InvenioRDM draft + legacy deposit JSON for a record and exit
    if "--debug" in args:
        idx = args.index("--debug")
        if idx + 1 >= len(args):
            print("ERROR: --debug requires a record ID argument.")
            sys.exit(1)
        rec_id = args[idx + 1]
        print(f"=== InvenioRDM draft for {rec_id} ===")
        try:
            api_request(f"/records/{rec_id}/draft", method="POST", token=token)
        except urllib.error.HTTPError as exc:
            if exc.code != 409:
                raise
        draft = api_request(f"/records/{rec_id}/draft", token=token)
        print(json.dumps(draft, indent=2))
        print(f"\n=== Legacy deposit for {rec_id} ===")
        deposit = api_request(f"/deposit/depositions/{rec_id}", token=token)
        print(json.dumps(deposit, indent=2))
        return

    # --record-id: target a specific record directly, bypassing the polling loop
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
