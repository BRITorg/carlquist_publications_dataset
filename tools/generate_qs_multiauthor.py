#!/usr/bin/env python3
"""
generate_qs_multiauthor.py

Generates QuickStatements (v1 tab-separated format) for Carlquist journal articles
with multiple authors that do not yet have Wikidata items.

Filters:
  - type == "article-journal"
  - wikidata-id is empty (not yet in Wikidata)
  - author count > 1 (single-author articles handled via OpenRefine)

Lookups:
  - carlquist_journals.csv  : "journal-title" → "wikidata-id"
  - carlquist_authors.csv   : "author"        → "wikidata-id"

Output:
  - QuickStatements v1 tab-separated format, printed to stdout
  - Warnings printed to stderr
"""

import csv
import sys
import re
from pathlib import Path

# ---------------------------------------------------------------------------
# File paths — adjust if needed
# ---------------------------------------------------------------------------
PUBLICATIONS_CSV = "../carlquist_publications.csv"
JOURNALS_CSV     = "../carlquist_journals.csv"
AUTHORS_CSV      = "../carlquist_authors.csv"

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
CARLQUIST_QID = "Q2251003"
SCHOLARLY_ARTICLE_QID = "Q13442814"


def load_journals(path: str) -> dict:
    """Return dict mapping journal title → Wikidata QID."""
    journals = {}
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            title = row["journal-title"].strip()
            qid   = row["wikidata-id"].strip()
            if title and qid:
                journals[title] = qid
    return journals


def load_authors(path: str) -> dict:
    """Return dict mapping author name → Wikidata QID (may be empty string)."""
    authors = {}
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["author"].strip()
            qid  = row["wikidata-id"].strip()
            authors[name] = qid  # empty string if no QID
    return authors


def format_date(issued: str) -> str:
    """
    Convert issued string to QuickStatements time format with precision.
      YYYY         → +YYYY-00-00T00:00:00Z/9
      YYYY-MM      → +YYYY-MM-00T00:00:00Z/10
      YYYY-MM-DD   → +YYYY-MM-DDT00:00:00Z/11
    Returns empty string if value cannot be parsed.
    """
    issued = issued.strip()
    if re.fullmatch(r"\d{4}", issued):
        return f"+{issued}-00-00T00:00:00Z/9"
    elif re.fullmatch(r"\d{4}-\d{2}", issued):
        return f"+{issued}-00T00:00:00Z/10"
    elif re.fullmatch(r"\d{4}-\d{2}-\d{2}", issued):
        return f"+{issued}T00:00:00Z/11"
    else:
        print(f"WARNING: Could not parse issued date: {issued!r}", file=sys.stderr)
        return ""


def emit_statement(subject: str, prop: str, value: str, qualifiers: list = None) -> str:
    """
    Build a single QuickStatements tab-separated line.
    qualifiers: list of (prop, value) tuples
    """
    parts = [subject, prop, value]
    if qualifiers:
        for qprop, qval in qualifiers:
            parts += [qprop, qval]
    return "\t".join(parts)


def generate_qs(pub_path: str, journals: dict, authors: dict) -> None:
    """Main generation loop — writes QS to stdout."""

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

        # --- Journal lookup ---
        journal_name = row.get("container-title", "").strip()
        journal_qid  = journals.get(journal_name, "")
        if not journal_qid:
            print(f"WARNING: No QID for journal: {journal_name!r} "
                  f"(title: {row.get('title','').strip()[:60]})", file=sys.stderr)
            skip_no_journal += 1
            continue

        # --- Date ---
        issued_raw  = row.get("issued", "").strip()
        issued_qs   = format_date(issued_raw) if issued_raw else ""
        year        = row.get("year", "").strip()
        description = f"scientific article published in {year}" if year else "scientific article"

        title    = row.get("title", "").strip()
        language = row.get("language", "en").strip() or "en"
        doi      = row.get("DOI", "").strip()
        volume   = row.get("volume", "").strip()
        issue    = row.get("issue", "").strip()
        page     = row.get("page", "").strip()

        # --- Emit block ---
        print("CREATE")

        # Label
        print(emit_statement("LAST", f"L{language}", f'"{title}"'))

        # Description (English)
        print(emit_statement("LAST", "Den", f'"{description}"'))

        # P31 instance of scholarly article
        print(emit_statement("LAST", "P31", SCHOLARLY_ARTICLE_QID))

        # P1433 published in
        print(emit_statement("LAST", "P1433", journal_qid))

        # P577 publication date
        if issued_qs:
            print(emit_statement("LAST", "P577", issued_qs))

        # P356 DOI
        if doi:
            print(emit_statement("LAST", "P356", f'"{doi}"'))

        # P478 volume
        if volume:
            print(emit_statement("LAST", "P478", f'"{volume}"'))

        # P433 issue
        if issue:
            print(emit_statement("LAST", "P433", f'"{issue}"'))

        # P304 page(s)
        if page:
            print(emit_statement("LAST", "P304", f'"{page}"'))

        # P50 / P2093 authors with P1545 ordinal
        for i, author_name in enumerate(raw_authors, start=1):
            ordinal = str(i)
            author_qid = authors.get(author_name, "")
            if author_qid:
                # Known Wikidata item — P50 with QID
                print(emit_statement(
                    "LAST", "P50", author_qid,
                    qualifiers=[("P1545", f'"{ordinal}"')]
                ))
            else:
                # No Wikidata item — P2093 with name string
                print(emit_statement(
                    "LAST", "P2093", f'"{author_name}"',
                    qualifiers=[("P1545", f'"{ordinal}"')]
                ))
                if author_name not in authors:
                    print(f"WARNING: Author not found in lookup: {author_name!r}", file=sys.stderr)

        # Blank line between items for readability
        print()
        item_count += 1

    # --- Summary ---
    print(f"\n--- Summary ---", file=sys.stderr)
    print(f"Items generated:          {item_count}", file=sys.stderr)
    print(f"Skipped (already in WD):  {skip_existing}", file=sys.stderr)
    print(f"Skipped (single author):  {skip_single}", file=sys.stderr)
    print(f"Skipped (no journal QID): {skip_no_journal}", file=sys.stderr)


def main():
    # Verify files exist
    for path in [PUBLICATIONS_CSV, JOURNALS_CSV, AUTHORS_CSV]:
        if not Path(path).exists():
            print(f"ERROR: File not found: {path}", file=sys.stderr)
            sys.exit(1)

    journals = load_journals(JOURNALS_CSV)
    authors  = load_authors(AUTHORS_CSV)
    generate_qs(PUBLICATIONS_CSV, journals, authors)


if __name__ == "__main__":
    main()
