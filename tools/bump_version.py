#!/usr/bin/env python3
"""
bump_version.py - Update version and date across all metadata files.

Usage:
  python3 tools/bump_version.py NEW_VERSION DATE
  python3 tools/bump_version.py --check

Examples:
  python3 tools/bump_version.py 1.2 2026-06-01
  python3 tools/bump_version.py 1.2.1 2026-06-15
  python3 tools/bump_version.py --check
"""

import json
import re
import sys
from datetime import datetime
from pathlib import Path

# Files and the version/date fields they contain
FILES = {
    "CITATION.cff": {
        "version": (r"^version: .+$", "version: {version}"),
        "date": (r"^date-released: .+$", "date-released: {iso_date}"),
    },
    "README.md": {
        "version": (r"^\*\*Current Version:\*\* .+$", "**Current Version:** {version}"),
        "date": (r"^\*\*Released:\*\* .+$", "**Released:** {long_date}"),
    },
    "DATA_DICTIONARY.md": {
        "version": (r"^\*\*Version:\*\* .+$", "**Version:** {version}"),
        "date": (r"^\*\*Last Updated:\*\* .+$", "**Last Updated:** {long_date}"),
    },
    "dataset_metadata.json": None,  # handled separately
    ".zenodo.json": None,           # handled separately
}

# Script lives in tools/, repo root is one level up
REPO_ROOT = Path(__file__).parent.parent


def iso_to_long_date(iso_date: str) -> str:
    """Convert '2026-06-01' to 'June 1, 2026'."""
    dt = datetime.strptime(iso_date, "%Y-%m-%d")
    return dt.strftime("%B %-d, %Y")


def update_text_file(path: Path, patterns: dict, version: str, iso_date: str, long_date: str, dry_run: bool) -> list[str]:
    """Apply regex substitutions to a text file. Returns list of change descriptions."""
    text = path.read_text(encoding="utf-8")
    changes = []
    for field, (pattern, template) in patterns.items():
        replacement = template.format(version=version, iso_date=iso_date, long_date=long_date)
        new_text, count = re.subn(pattern, replacement, text, flags=re.MULTILINE)
        if count == 0:
            print(f"  WARNING: Pattern not found in {path.name}: {pattern}")
        elif new_text != text:
            changes.append(f"  {field}: updated")
            text = new_text
    if changes and not dry_run:
        path.write_text(text, encoding="utf-8")
    return changes


def update_json_file(path: Path, updates: dict, dry_run: bool) -> list[str]:
    """Update specific keys in a JSON file. Returns list of change descriptions."""
    data = json.loads(path.read_text(encoding="utf-8"))
    changes = []
    for key, value in updates.items():
        if key in data and data[key] != value:
            changes.append(f"  {key}: {data[key]!r} → {value!r}")
            data[key] = value
        elif key not in data:
            print(f"  WARNING: Key '{key}' not found in {path.name}")
    if changes and not dry_run:
        path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return changes


def check_consistency():
    """Report current version/date values across all files."""
    print("Checking version consistency across files...\n")
    results = {}

    # CITATION.cff
    text = (REPO_ROOT / "CITATION.cff").read_text()
    m = re.search(r"^version: (.+)$", text, re.MULTILINE)
    d = re.search(r"^date-released: (.+)$", text, re.MULTILINE)
    results["CITATION.cff"] = (m.group(1).strip() if m else "?", d.group(1).strip() if d else "?")

    # README.md
    text = (REPO_ROOT / "README.md").read_text()
    m = re.search(r"^\*\*Current Version:\*\* (.+)$", text, re.MULTILINE)
    d = re.search(r"^\*\*Released:\*\* (.+)$", text, re.MULTILINE)
    results["README.md"] = (m.group(1).strip() if m else "?", d.group(1).strip() if d else "?")

    # DATA_DICTIONARY.md
    text = (REPO_ROOT / "DATA_DICTIONARY.md").read_text()
    m = re.search(r"^\*\*Version:\*\* (.+)$", text, re.MULTILINE)
    d = re.search(r"^\*\*Last Updated:\*\* (.+)$", text, re.MULTILINE)
    results["DATA_DICTIONARY.md"] = (m.group(1).strip() if m else "?", d.group(1).strip() if d else "?")

    # dataset_metadata.json
    data = json.loads((REPO_ROOT / "dataset_metadata.json").read_text())
    results["dataset_metadata.json"] = (data.get("version", "?"), data.get("date_published", "?"))

    # .zenodo.json
    data = json.loads((REPO_ROOT / ".zenodo.json").read_text())
    results[".zenodo.json"] = ("(no version field)", data.get("publication_date", "?"))

    # Print results
    print(f"{'File':<25} {'Version':<12} {'Date'}")
    print("-" * 55)
    for fname, (ver, date) in results.items():
        print(f"{fname:<25} {ver:<12} {date}")

    # Check consistency
    versions = {v for f, (v, d) in results.items() if f != ".zenodo.json"}
    dates_iso = set()
    for fname, (ver, date) in results.items():
        if re.match(r"\d{4}-\d{2}-\d{2}", date):
            dates_iso.add(date)
        elif re.match(r"\w+ \d+, \d{4}", date):
            try:
                dt = datetime.strptime(date, "%B %d, %Y")
                dates_iso.add(dt.strftime("%Y-%m-%d"))
            except ValueError:
                pass

    print()
    if len(versions) == 1:
        print("✓ Versions are consistent.")
    else:
        print(f"✗ VERSION MISMATCH: {versions}")

    if len(dates_iso) == 1:
        print("✓ Dates are consistent.")
    else:
        print(f"✗ DATE MISMATCH: {dates_iso}")


def bump(version: str, iso_date: str, dry_run: bool = False):
    """Update version and date across all metadata files."""
    try:
        long_date = iso_to_long_date(iso_date)
    except ValueError:
        print(f"Error: Invalid date format '{iso_date}'. Use YYYY-MM-DD.")
        sys.exit(1)

    prefix = "[DRY RUN] " if dry_run else ""
    print(f"{prefix}Updating to version {version}, date {iso_date} ({long_date})\n")

    all_changes = {}

    # Text files
    text_files = {
        "CITATION.cff": FILES["CITATION.cff"],
        "README.md": FILES["README.md"],
        "DATA_DICTIONARY.md": FILES["DATA_DICTIONARY.md"],
    }
    for fname, patterns in text_files.items():
        path = REPO_ROOT / fname
        changes = update_text_file(path, patterns, version, iso_date, long_date, dry_run)
        all_changes[fname] = changes

    # dataset_metadata.json
    path = REPO_ROOT / "dataset_metadata.json"
    changes = update_json_file(path, {"version": version, "date_published": iso_date}, dry_run)
    all_changes["dataset_metadata.json"] = changes

    # .zenodo.json (date only, no version field)
    path = REPO_ROOT / ".zenodo.json"
    changes = update_json_file(path, {"publication_date": iso_date}, dry_run)
    all_changes[".zenodo.json"] = changes

    # Print summary
    any_changes = False
    for fname, changes in all_changes.items():
        if changes:
            any_changes = True
            print(f"{fname}:")
            for c in changes:
                print(c)
        else:
            print(f"{fname}: no changes needed")

    if not any_changes:
        print("\nAll files already at the target version/date.")
    elif dry_run:
        print("\nDry run complete. Run without --dry-run to apply changes.")
    else:
        print(f"\nDone. Remember to:")
        print(f"  1. Add an entry to CHANGELOG.md for version {version}")
        print(f"  2. Verify record/field counts if the CSV changed")
        print(f"  3. Commit all changes before publishing to Zenodo")


if __name__ == "__main__":
    args = sys.argv[1:]

    if not args or args[0] in ("-h", "--help"):
        print(__doc__)
        sys.exit(0)

    if args[0] == "--check":
        check_consistency()
        sys.exit(0)

    dry_run = "--dry-run" in args
    args = [a for a in args if a != "--dry-run"]

    if len(args) != 2:
        print("Usage: python3 tools/bump_version.py NEW_VERSION DATE")
        print("       python3 tools/bump_version.py --check")
        print("       python3 tools/bump_version.py --dry-run NEW_VERSION DATE")
        sys.exit(1)

    version, iso_date = args
    bump(version, iso_date, dry_run=dry_run)
