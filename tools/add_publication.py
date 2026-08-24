#!/usr/bin/env python3
"""
add_publication.py

Workflow tool for adding ONE new Carlquist publication that is not yet in
carlquist_publications.csv and not yet in Wikidata. Complements OpenRefine
(still the tool of choice for bulk reconciliation work) and
generate_qs_multiauthor.py (batch processing of existing CSV rows).

Two modes:

  draft     Given a record's fields, print (a) warnings — duplicate title
            check, missing journal/author QIDs — and (b) a QuickStatements
            CREATE block to review and run yourself in your own logged-in
            QuickStatements session. Does NOT modify any file.

  finalize  Given the same fields plus the wikidata-id you got back from
            running the QuickStatements batch, print the exact CSV row to
            append. Only writes to carlquist_publications.csv if --write is
            passed; otherwise it's a dry run.

Record fields are supplied via a JSON file (--json) and/or individual
--field flags, which override the JSON. See tools/new_publication.example.json
for the expected shape.

Examples:
  python3 add_publication.py draft --json new_record.json
  python3 add_publication.py finalize --json new_record.json --wikidata-id Q12345678
  python3 add_publication.py finalize --json new_record.json --wikidata-id Q12345678 --write
"""

import argparse
import csv
import json
import sys
from pathlib import Path

from qs_common import load_journals, load_journal_issns, load_authors, build_create_block

PUBLICATIONS_CSV = Path("../carlquist_publications.csv")
JOURNALS_CSV = Path("../carlquist_journals.csv")
AUTHORS_CSV = Path("../carlquist_authors.csv")

FIELDS = [
    "title", "container-title", "year", "issued", "author", "editor",
    "publisher", "volume", "issue", "page", "type", "container-ISSN",
    "container-eISSN", "container-ISBN", "container-OCLC-number", "DOI",
    "wikidata-id", "wikidata-url", "URL", "language",
]

FLAG_TO_FIELD = {
    "title": "title", "container-title": "container-title", "year": "year",
    "issued": "issued", "author": "author", "editor": "editor",
    "publisher": "publisher", "volume": "volume", "issue": "issue",
    "page": "page", "type": "type", "container-issn": "container-ISSN",
    "container-eissn": "container-eISSN", "container-isbn": "container-ISBN",
    "container-oclc": "container-OCLC-number", "doi": "DOI", "url": "URL",
    "language": "language",
}


def build_record(args) -> dict:
    record = {f: "" for f in FIELDS}
    record["type"] = "article-journal"
    record["language"] = "en"

    if args.json:
        with open(args.json, encoding="utf-8") as f:
            data = json.load(f)
        for k, v in data.items():
            if k in record:
                record[k] = str(v)
            else:
                print(f"WARNING: Ignoring unknown field in JSON: {k!r}", file=sys.stderr)

    for flag, field in FLAG_TO_FIELD.items():
        val = getattr(args, flag.replace("-", "_"), None)
        if val is not None:
            record[field] = val

    return record


def check_duplicate_title(title: str) -> list:
    warnings = []
    if not PUBLICATIONS_CSV.exists():
        return warnings
    needle = title.strip().lower()
    with PUBLICATIONS_CSV.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            existing = row.get("title", "").strip()
            if existing.lower() == needle:
                warnings.append(f"Exact title match already in CSV: {existing!r}")
            elif needle and needle in existing.lower():
                warnings.append(f"Possible duplicate — existing title contains this one: {existing!r}")
    return warnings


def fill_journal_issns(record: dict, journal_issns: dict) -> None:
    """Auto-fill container-ISSN/eISSN from the journal lookup if not already set."""
    issn, eissn = journal_issns.get(record.get("container-title", "").strip(), ("", ""))
    if not record.get("container-ISSN") and issn:
        record["container-ISSN"] = issn
    if not record.get("container-eISSN") and eissn:
        record["container-eISSN"] = eissn


def cmd_draft(args):
    record = build_record(args)
    journals = load_journals(str(JOURNALS_CSV))
    journal_issns = load_journal_issns(str(JOURNALS_CSV))
    authors = load_authors(str(AUTHORS_CSV))
    fill_journal_issns(record, journal_issns)

    warnings = check_duplicate_title(record["title"])
    lines, qs_warnings = build_create_block(record, journals, authors)
    warnings += qs_warnings

    if warnings:
        print("--- Warnings (review before submitting) ---", file=sys.stderr)
        for w in warnings:
            print(f"WARNING: {w}", file=sys.stderr)
        print(file=sys.stderr)

    print("--- QuickStatements draft (run this yourself in your own session) ---", file=sys.stderr)
    print("\n".join(lines))

    print("\n--- Preview: CSV row once you have a wikidata-id ---", file=sys.stderr)
    preview = dict(record)
    preview["wikidata-id"] = "<QID from QuickStatements>"
    preview["wikidata-url"] = "<https://www.wikidata.org/wiki/QID>"
    print(", ".join(f"{k}={preview[k]!r}" for k in FIELDS if preview[k]), file=sys.stderr)


def cmd_finalize(args):
    record = build_record(args)
    journal_issns = load_journal_issns(str(JOURNALS_CSV))
    fill_journal_issns(record, journal_issns)

    record["wikidata-id"] = args.wikidata_id
    record["wikidata-url"] = f"https://www.wikidata.org/wiki/{args.wikidata_id}"

    warnings = check_duplicate_title(record["title"])
    for w in warnings:
        print(f"WARNING: {w}", file=sys.stderr)

    if not PUBLICATIONS_CSV.exists():
        print(f"ERROR: {PUBLICATIONS_CSV} not found", file=sys.stderr)
        sys.exit(1)

    with PUBLICATIONS_CSV.open(newline="", encoding="utf-8") as f:
        header = next(csv.reader(f))

    # Build the row in a StringIO so we can both preview and (optionally) append it.
    import io
    buf = io.StringIO()
    writer = csv.writer(buf)
    writer.writerow([record.get(col, "") for col in header])
    row_text = buf.getvalue()

    print("--- CSV row ---", file=sys.stderr)
    print(row_text, end="")

    if args.write:
        with PUBLICATIONS_CSV.open("a", newline="", encoding="utf-8") as f:
            f.write(row_text)
        print(f"\nAppended to {PUBLICATIONS_CSV}", file=sys.stderr)
    else:
        print("\n(dry run — pass --write to append this row to the CSV)", file=sys.stderr)


def add_common_field_args(p):
    for flag in FLAG_TO_FIELD:
        p.add_argument(f"--{flag}")
    p.add_argument("--json", help="Path to a JSON file with record fields (see new_publication.example.json)")


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)

    p_draft = sub.add_parser("draft", help="Generate QuickStatements draft + warnings; no files modified")
    add_common_field_args(p_draft)
    p_draft.set_defaults(func=cmd_draft)

    p_final = sub.add_parser("finalize", help="Print (and optionally write) the finished CSV row")
    add_common_field_args(p_final)
    p_final.add_argument("--wikidata-id", required=True, help="QID returned after running the QuickStatements batch")
    p_final.add_argument("--write", action="store_true", help="Actually append the row to carlquist_publications.csv")
    p_final.set_defaults(func=cmd_finalize)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
