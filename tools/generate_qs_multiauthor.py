#!/usr/bin/env python3
"""
generate_qs_multiauthor.py

Generates QuickStatements (v1 tab-separated format) for Carlquist journal articles
with multiple authors that do not yet have Wikidata items.

Filters:
  - type == "article-journal"
  - wikidata-id is empty (not yet in Wikidata)
  - author count > 1 (single-author articles are handled via OpenRefine, or via
    add_publication.py for one-off additions)

Lookups:
  - carlquist_journals.csv  : "journal-title" -> "wikidata-id"
  - carlquist_authors.csv   : "author-as-cited" -> "wikidata-id"

Output:
  - QuickStatements v1 tab-separated format, printed to stdout
  - Warnings printed to stderr
"""

import sys
from pathlib import Path

from qs_common import load_journals, load_authors, build_create_block

# ---------------------------------------------------------------------------
# File paths — adjust if needed
# ---------------------------------------------------------------------------
PUBLICATIONS_CSV = "../carlquist_publications.csv"
JOURNALS_CSV = "../carlquist_journals.csv"
AUTHORS_CSV = "../carlquist_authors.csv"


def generate_qs(pub_path: str, journals: dict, authors: dict) -> None:
    """Main generation loop — writes QS to stdout."""
    import csv

    with open(pub_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    item_count = 0
    skip_existing = 0
    skip_single = 0
    skip_no_journal = 0

    for row in rows:

        # --- Filters ---
        if row.get("type", "").strip() != "article-journal":
            continue

        if row.get("wikidata-id", "").strip():
            skip_existing += 1
            continue

        raw_authors = [a.strip() for a in row.get("author", "").split(";") if a.strip()]
        if len(raw_authors) <= 1:
            skip_single += 1
            continue

        if not journals.get(row.get("container-title", "").strip()):
            print(f"WARNING: No QID for journal: {row.get('container-title','').strip()!r} "
                  f"(title: {row.get('title','').strip()[:60]})", file=sys.stderr)
            skip_no_journal += 1
            continue

        lines, warnings = build_create_block(row, journals, authors)
        for w in warnings:
            print(f"WARNING: {w} (title: {row.get('title','').strip()[:60]})", file=sys.stderr)
        print("\n".join(lines))
        item_count += 1

    # --- Summary ---
    print(f"\n--- Summary ---", file=sys.stderr)
    print(f"Items generated:          {item_count}", file=sys.stderr)
    print(f"Skipped (already in WD):  {skip_existing}", file=sys.stderr)
    print(f"Skipped (single author):  {skip_single}", file=sys.stderr)
    print(f"Skipped (no journal QID): {skip_no_journal}", file=sys.stderr)


def main():
    for path in [PUBLICATIONS_CSV, JOURNALS_CSV, AUTHORS_CSV]:
        if not Path(path).exists():
            print(f"ERROR: File not found: {path}", file=sys.stderr)
            sys.exit(1)

    journals = load_journals(JOURNALS_CSV)
    authors = load_authors(AUTHORS_CSV)
    generate_qs(PUBLICATIONS_CSV, journals, authors)


if __name__ == "__main__":
    main()
