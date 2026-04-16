# Claude Code Instructions: Carlquist Publications Dataset

## Project Overview

Bibliographic dataset of 343 publications by botanist Sherwin Carlquist (1930–2021).
Part of the Sherwin Carlquist Digital Extended Specimen Network (BRIT + California Botanic Garden).
Published on Zenodo: DOI 10.5281/zenodo.18687469

**Current version:** 2.0 (2026-04-17)

## Files

| File | Purpose |
|------|---------|
| `carlquist_publications.csv` | Main dataset (343 records, 20 fields) |
| `carlquist_journals.csv` | Journal lookup table (48 records) |
| `carlquist_authors.csv` | Co-author lookup table (73 records) |
| `datapackage.json` | Frictionless Data descriptor for all three CSVs |
| `README.md` | Human-readable overview |
| `DATA_DICTIONARY.md` | Field definitions and metadata documentation |
| `CHANGELOG.md` | Version history (Keep a Changelog format) |
| `CITATION.cff` | Machine-readable citation (CFF 1.2.0) |
| `dataset_metadata.json` | Technical metadata |
| `.zenodo.json` | Zenodo deposit metadata |
| `TROUBLESHOOTING.md` | Excel/import guidance for users |
| `tools/bump_version.py` | Script to update version/date across all files |

## Version-Tracked Fields

Every release requires updating these fields in sync:

| File | Field | Format | Example |
|------|-------|--------|---------|
| `CITATION.cff` | `version:` | `2.0` | `version: 2.1` |
| `CITATION.cff` | `date-released:` | `YYYY-MM-DD` | `date-released: 2026-04-17` |
| `README.md` | `**Current Version:**` | `2.0` | `**Current Version:** 2.1` |
| `README.md` | `**Released:**` | `Month DD, YYYY` | `**Released:** April 17, 2026` |
| `DATA_DICTIONARY.md` | `**Version:**` | `2.0` | `**Version:** 2.1` |
| `DATA_DICTIONARY.md` | `**Last Updated:**` | `Month DD, YYYY` | `**Last Updated:** April 17, 2026` |
| `dataset_metadata.json` | `"version":` | `"2.0"` | `"version": "2.1"` |
| `dataset_metadata.json` | `"date_published":` | `"YYYY-MM-DD"` | `"date_published": "2026-04-17"` |
| `datapackage.json` | `"version":` | `"2.0"` | `"version": "2.1"` |
| `.zenodo.json` | `"publication_date":` | `"YYYY-MM-DD"` | `"publication_date": "2026-04-17"` |

The `.zenodo.json` does **not** store a version number, only the date.

## Release Checklist

Use `bump_version.py` to handle steps 2–3 automatically.

### When updating the dataset (data changes or corrections):
1. Edit `carlquist_publications.csv`
2. Update record/field counts in `README.md`, `DATA_DICTIONARY.md`, and `dataset_metadata.json` if they changed
3. Add a CHANGELOG entry describing what changed

### When creating a new version:
1. Decide the new version number (follow semantic versioning: major.minor.patch)
   - Patch (1.1 → 1.1.1): corrections, metadata fixes, no structural changes
   - Minor (1.1 → 1.2): new fields, significant data additions, new records
   - Major (1.x → 2.0): breaking structural changes
2. Run: `python3 bump_version.py NEW_VERSION YYYY-MM-DD`
3. Verify the changes look correct across all files
4. Add a detailed entry to `CHANGELOG.md` under the new version heading

### Before publishing to Zenodo:
- [ ] All version-tracked fields are consistent (run `python3 bump_version.py --check`)
- [ ] `frictionless validate datapackage.json` passes with no errors
- [ ] `CHANGELOG.md` has an entry for this version with meaningful descriptions
- [ ] Record count in `README.md`, `DATA_DICTIONARY.md`, `dataset_metadata.json` matches CSV row count
- [ ] Field count in `README.md`, `DATA_DICTIONARY.md`, `dataset_metadata.json` matches CSV column count
- [ ] `.zenodo.json` has the correct `publication_date`
- [ ] `datapackage.json` version and resource schemas are current
- [ ] Git is clean (all changes committed)

## Data Structure Notes

- **Records:** 343 publications; 48 journals; 73 co-authors (as of v2.0)
- **Fields:** 20 in carlquist_publications.csv (as of v2.0)
- **Encoding:** UTF-8
- **Author format:** "Last, First; Last, First" (semicolon-separated)
- **Date format:** ISO 8601 (YYYY, YYYY-MM, or YYYY-MM-DD)
- **Type vocabulary:** `article-journal`, `book`, `chapter` (CSL-JSON)
- **Language codes:** ISO 639-1 (`en` for all records)
- **Wikidata IDs:** 100% coverage (343 of 343 records)

## Versioning

This project uses semantic versioning. The Zenodo DOI (10.5281/zenodo.18687469) is a concept DOI
that resolves to the latest version automatically.
