#!/usr/bin/env python3
"""
qs_common.py

Shared helpers for generating Wikidata QuickStatements (v1 tab-separated format)
for Carlquist publications. Used by generate_qs_multiauthor.py (batch, existing
CSV rows) and add_publication.py (single new record, not yet in the CSV).
"""

import csv
import re
import sys

CARLQUIST_QID = "Q2251003"
SCHOLARLY_ARTICLE_QID = "Q13442814"


def load_journals(path: str) -> dict:
    """Return dict mapping journal title -> Wikidata QID."""
    journals = {}
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            title = row["journal-title"].strip()
            qid = row["wikidata-id"].strip()
            if title and qid:
                journals[title] = qid
    return journals


def load_journal_issns(path: str) -> dict:
    """Return dict mapping journal title -> (ISSN, eISSN)."""
    issns = {}
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            title = row["journal-title"].strip()
            if title:
                issns[title] = (row.get("ISSN", "").strip(), row.get("eISSN", "").strip())
    return issns


def load_authors(path: str) -> dict:
    """Return dict mapping author-as-cited -> Wikidata QID (may be empty string)."""
    authors = {}
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["author-as-cited"].strip()
            qid = row["wikidata-id"].strip()
            authors[name] = qid  # empty string if no QID
    return authors


def format_date(issued: str) -> str:
    """
    Convert issued string to QuickStatements time format with precision.
      YYYY         -> +YYYY-00-00T00:00:00Z/9
      YYYY-MM      -> +YYYY-MM-00T00:00:00Z/10
      YYYY-MM-DD   -> +YYYY-MM-DDT00:00:00Z/11
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


def build_create_block(row: dict, journals: dict, authors: dict) -> tuple:
    """
    Build the QuickStatements CREATE block for one publication record.

    row: dict with keys title, container-title, year, issued, author,
         DOI, volume, issue, page, language (all as found in
         carlquist_publications.csv — missing keys treated as empty).

    Returns (lines, warnings):
      lines    - list of str, the QS block (including leading "CREATE" and
                 trailing blank line)
      warnings - list of str, human-readable warnings (e.g. missing QIDs)
    """
    lines = []
    warnings = []

    journal_name = row.get("container-title", "").strip()
    journal_qid = journals.get(journal_name, "")
    if journal_name and not journal_qid:
        warnings.append(f"No QID for journal: {journal_name!r}")

    issued_raw = row.get("issued", "").strip()
    issued_qs = format_date(issued_raw) if issued_raw else ""
    year = row.get("year", "").strip()
    description = f"scientific article published in {year}" if year else "scientific article"

    title = row.get("title", "").strip()
    language = row.get("language", "en").strip() or "en"
    doi = row.get("DOI", "").strip()
    volume = row.get("volume", "").strip()
    issue = row.get("issue", "").strip()
    page = row.get("page", "").strip()

    lines.append("CREATE")
    lines.append(emit_statement("LAST", f"L{language}", f'"{title}"'))
    lines.append(emit_statement("LAST", "Den", f'"{description}"'))
    lines.append(emit_statement("LAST", "P31", SCHOLARLY_ARTICLE_QID))

    if journal_qid:
        lines.append(emit_statement("LAST", "P1433", journal_qid))
    if issued_qs:
        lines.append(emit_statement("LAST", "P577", issued_qs))
    if doi:
        lines.append(emit_statement("LAST", "P356", f'"{doi}"'))
    if volume:
        lines.append(emit_statement("LAST", "P478", f'"{volume}"'))
    if issue:
        lines.append(emit_statement("LAST", "P433", f'"{issue}"'))
    if page:
        lines.append(emit_statement("LAST", "P304", f'"{page}"'))

    raw_authors = [a.strip() for a in row.get("author", "").split(";") if a.strip()]
    for i, author_name in enumerate(raw_authors, start=1):
        ordinal = str(i)
        author_qid = authors.get(author_name, "")
        if author_qid:
            lines.append(emit_statement(
                "LAST", "P50", author_qid,
                qualifiers=[("P1545", f'"{ordinal}"')]
            ))
        else:
            lines.append(emit_statement(
                "LAST", "P2093", f'"{author_name}"',
                qualifiers=[("P1545", f'"{ordinal}"')]
            ))
            warnings.append(f"Author not found in lookup: {author_name!r}")

    lines.append("")  # blank line between items for readability
    return lines, warnings
