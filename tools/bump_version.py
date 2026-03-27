#!/usr/bin/env python3
"""
bump_version.py - Update version and date across all metadata files.

Usage:
  python3 tools/bump_version.py NEW_VERSION DATE      # bump version in all files
  python3 tools/bump_version.py --dry-run NEW_VERSION DATE
  python3 tools/bump_version.py --check               # verify all files are consistent
  python3 tools/bump_version.py --release VERSION     # create git tag + GitHub release

Examples:
  python3 tools/bump_version.py 1.2 2026-06-01
  python3 tools/bump_version.py --check
  python3 tools/bump_version.py --release 1.2
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


def check_csv_counts():
    """Check actual CSV record/field counts against documented values."""
    import csv
    csv_path = REPO_ROOT / "carlquist_publications.csv"
    with csv_path.open(encoding="utf-8", newline="") as f:
        reader = csv.reader(f)
        headers = next(reader)
        actual_fields = len(headers)
        actual_records = sum(1 for _ in reader)

    print(f"\nChecking record/field counts (actual CSV: {actual_records} records, {actual_fields} fields)...\n")

    ok = True

    # dataset_metadata.json
    meta = json.loads((REPO_ROOT / "dataset_metadata.json").read_text())
    doc_records = meta.get("records", "?")
    doc_fields = meta.get("fields", "?")
    records_ok = doc_records == actual_records
    fields_ok = doc_fields == actual_fields
    print(f"dataset_metadata.json:  records={doc_records} {'✓' if records_ok else f'✗ (CSV has {actual_records})'}  "
          f"fields={doc_fields} {'✓' if fields_ok else f'✗ (CSV has {actual_fields})'}")
    if not records_ok or not fields_ok:
        ok = False

    # README.md
    text = (REPO_ROOT / "README.md").read_text()
    for pattern, label in [
        (r"\((\d+) records\)", "records"),
        (r"(\d+) standardized fields", "fields"),
    ]:
        matches = re.findall(pattern, text)
        unique = set(int(m) for m in matches)
        expected = actual_records if label == "records" else actual_fields
        if not unique:
            print(f"README.md:              {label} — pattern not found")
        elif unique == {expected}:
            print(f"README.md:              {label}={expected} ✓")
        else:
            print(f"README.md:              {label} ✗ — found {unique}, CSV has {expected}")
            ok = False

    # DATA_DICTIONARY.md
    text = (REPO_ROOT / "DATA_DICTIONARY.md").read_text()
    for pattern, label in [
        (r"\*\*Records:\*\*\s+(\d+)", "records"),
        (r"\*\*Fields:\*\*\s+(\d+)", "fields"),
    ]:
        m = re.search(pattern, text)
        expected = actual_records if label == "records" else actual_fields
        if not m:
            print(f"DATA_DICTIONARY.md:     {label} — pattern not found")
        elif int(m.group(1)) == expected:
            print(f"DATA_DICTIONARY.md:     {label}={expected} ✓")
        else:
            print(f"DATA_DICTIONARY.md:     {label} ✗ — found {m.group(1)}, CSV has {expected}")
            ok = False

    print()
    if ok:
        print("✓ Record and field counts are consistent.")
    else:
        print("✗ Count mismatches found — update the files listed above.")

    return ok


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

    check_csv_counts()


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


def extract_changelog_notes(version: str) -> str | None:
    """Extract the release notes for a given version from CHANGELOG.md."""
    text = (REPO_ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
    pattern = rf"## \[{re.escape(version)}\][^\n]*\n(.*?)(?=\n## \[|\Z)"
    m = re.search(pattern, text, re.DOTALL)
    return m.group(1).strip() if m else None


def run(cmd: str) -> tuple[int, str]:
    """Run a shell command, return (returncode, output)."""
    import subprocess
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=REPO_ROOT)
    return result.returncode, (result.stdout + result.stderr).strip()


def release(version: str, yes: bool = False):
    """Create a git tag and GitHub release for the given version."""
    tag = f"v{version}"

    # 1. Pre-flight checks
    print("Running pre-flight checks...\n")

    code, out = run("git status --porcelain")
    # Ignore untracked files (??); only block on tracked changes
    tracked_changes = [l for l in out.splitlines() if not l.startswith("??")]
    if tracked_changes:
        print(f"✗ Uncommitted changes to tracked files detected:")
        for line in tracked_changes:
            print(f"  {line}")
        print("\nCommit or stash all changes before releasing.")
        sys.exit(1)
    print("✓ Git working tree is clean.")

    code, out = run("git rev-parse --abbrev-ref HEAD")
    branch = out.strip()
    if branch != "main":
        print(f"✗ Not on main branch (currently on '{branch}').")
        print("  Switch to main and ensure it's up to date before releasing.")
        sys.exit(1)
    print(f"✓ On main branch.")

    # Check tag doesn't already exist
    code, out = run(f"git tag -l {tag}")
    if out.strip():
        print(f"✗ Tag {tag} already exists.")
        sys.exit(1)
    print(f"✓ Tag {tag} does not yet exist.")

    # Run consistency check (warnings only, don't abort)
    print()
    check_consistency()

    # 2. Extract CHANGELOG notes
    print()
    notes = extract_changelog_notes(version)
    if not notes:
        print(f"WARNING: No entry found in CHANGELOG.md for version [{version}].")
        print("  The release will be created without notes.")
        notes = f"Version {version}"
    else:
        print(f"Release notes from CHANGELOG.md:\n")
        print("-" * 40)
        print(notes)
        print("-" * 40)

    # 3. Confirm
    print(f"\nThis will:")
    print(f"  1. Create annotated git tag: {tag}")
    print(f"  2. Push tag to origin")
    print(f"  3. Create GitHub release: {tag}")
    if yes:
        print("\n--yes flag set, proceeding.")
    else:
        answer = input("\nProceed? [y/N] ").strip().lower()
        if answer != "y":
            print("Aborted.")
            sys.exit(0)

    # 4. Create and push tag
    title = f"Version {version}"
    code, out = run(f'git tag -a {tag} -m "{title}"')
    if code != 0:
        print(f"✗ Failed to create tag:\n{out}")
        sys.exit(1)
    print(f"✓ Created tag {tag}")

    code, out = run(f"git push origin {tag}")
    if code != 0:
        print(f"✗ Failed to push tag:\n{out}")
        sys.exit(1)
    print(f"✓ Pushed tag {tag} to origin")

    # 5. Create GitHub release
    import tempfile, os
    with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
        f.write(notes)
        notes_file = f.name

    try:
        code, out = run(f'gh release create {tag} --title "{title}" --notes-file "{notes_file}"')
    finally:
        os.unlink(notes_file)

    if code != 0:
        print(f"✗ Failed to create GitHub release:\n{out}")
        sys.exit(1)

    print(f"✓ GitHub release created.")
    # Extract URL from output
    url_match = re.search(r"https://\S+", out)
    if url_match:
        print(f"\n{url_match.group(0)}")


if __name__ == "__main__":
    args = sys.argv[1:]

    if not args or args[0] in ("-h", "--help"):
        print(__doc__)
        sys.exit(0)

    if args[0] == "--check":
        check_consistency()
        sys.exit(0)

    if args[0] == "--release":
        yes = "--yes" in args
        args = [a for a in args if a != "--yes"]
        if len(args) != 2:
            print("Usage: python3 tools/bump_version.py --release VERSION [--yes]")
            sys.exit(1)
        release(args[1], yes=yes)
        sys.exit(0)

    dry_run = "--dry-run" in args
    args = [a for a in args if a != "--dry-run"]

    if len(args) != 2:
        print("Usage: python3 tools/bump_version.py NEW_VERSION DATE")
        print("       python3 tools/bump_version.py --check")
        print("       python3 tools/bump_version.py --release VERSION")
        print("       python3 tools/bump_version.py --dry-run NEW_VERSION DATE")
        sys.exit(1)

    version, iso_date = args
    bump(version, iso_date, dry_run=dry_run)
