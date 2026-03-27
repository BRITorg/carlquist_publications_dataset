# Changelog

All notable changes to this dataset will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.6] - 2026-03-27

### Changed
- Removed subject fields from .zenodo.json

### Added
- tools/zenodo_add_subjects.py added, will be run by GitHub Action

### Note
No changes were made to the dataset, only supporting metadata files.


## [1.1.5] - 2026-03-27

### Changed
- Testing subject ingest as custom fields

### Note
No changes were made to the dataset, only supporting metadata files.


## [1.1.4] - 2026-03-27

### Changed
- Testing subject with different format using scheme:url

### Note
No changes were made to the dataset, only supporting metadata files.

## [1.1.3] - 2026-03-27

### Changed
- Testing subject with full format

### Note
No changes were made to the dataset, only supporting metadata files.

## [1.1.2] - 2026-03-27

### Changed
- Testing single subject with alternative format

### Note
No changes were made to the dataset, only supporting metadata files.

## [1.1.1] - 2026-03-27

### Fixed
- Corrected field count in README.md (18 → 19 standardized fields, missed when wikidata_id was added in v1.1)

### Added
- `tools/bump_version.py`: script to update version/date across all metadata files, with `--check`, `--dry-run`, and `--release` subcommands
- `CLAUDE.md`: project context and release checklist for use with Claude Code
- Added `.claude/` to `.gitignore`
- Testing alternative subject format in `.zenodo.json`

### Note
No changes were made to the dataset, only supporting metadata files.


## [1.1] - 2026-03-26

### Changed
- Updated relevant dataset metadata files

### Added
- New wikidata_id column, populated with QIDs of existing items

### Fixed
- Added some missing records
- Removed duplicate records
- Fixed author order for some records
- Fixed various ISSNs
- Added missing DOIs


## [1.0.4] - 2026-02-19

### Fixed
- Corrected .zenodo.json structure for proper Zenodo metadata handling
- Fixed field nesting (moved description, funding, languages, subjects to root level)
- Updated contributor format to match Zenodo's current schema

### Note
This version corrects metadata issues from v1.0.2 and v1.0.3. The dataset CSV and documentation remain unchanged.


## [1.0.3] - 2026-02-25

### Fixed
- Added more metadata to .zenodo.json to prevent loss of information when new version release is generated on GitHub.
- Corrected citation verbiage and removed explicit version number in DATA_DICTIONARY.md

### Changed
- Updated version metadata to 1.0.3 in CITATION.cff and dataset_metadata.json

### Note
This is a metadata-only update. The dataset CSV and field definitions remain unchanged from v1.0.


## [1.0.2] - 2026-02-25

### Changed
- Updated version metadata to 1.0.2 in CITATION.cff and dataset_metadata.json
- Updated publication date to 2026-02-25 in CITATION.cff and dataset_metadata.json
- Removed full change history and added reference to CHANGELOG.md in README.md DATA_DICTIONARY.md

### Added
- .zenodo.json file with contributors and subjects

### Note
This is a metadata-only update. The dataset CSV and field definitions remain unchanged from v1.0.

## [1.0.1] - 2026-02-19

### Changed
- Updated all DOI references from reserved placeholder (10.5281/zenodo.18624213) to published Zenodo DOI (10.5281/zenodo.18687469)
- Updated version metadata to 1.0.1 in CITATION.cff and dataset_metadata.json
- Updated publication date to 2026-02-19 in CITATION.cff and dataset_metadata.json
- Updated Zenodo record URL to https://zenodo.org/records/18687469

### Added
- DOI badge to README.md

### Fixed
- Corrected DOI in README.md
- Corrected DOI in CHANGELOG.md (v1.0 section)
- Corrected DOI in CITATION.cff
- Corrected DOI in DATA_DICTIONARY.md
- Corrected DOI in dataset_metadata.json

### Documentation
- Added version 1.0.1 entry to DATA_DICTIONARY.md version history

### Note
This is a metadata-only update. The dataset CSV and field definitions remain unchanged from v1.0.

---


## [1.0] - 2026-02-18

### Initial Public Release

This is the first public release of the Sherwin Carlquist Publications Dataset. The dataset underwent extensive internal review and refinement before this public release to ensure data quality standards, metadata consistency, and documentation completeness.

#### Dataset Contents
- 343 publication records spanning 1956-2021
- 18 standardized metadata fields
- Complete bibliographic metadata following CSL-JSON and Dublin Core standards

#### Key Features
- **Comprehensive coverage**: All known publications by Sherwin Carlquist
- **Standardized format**: CSL-JSON compliant field names and vocabulary
- **Rich metadata**: Includes DOIs, ISSNs, ISBNs, OCLC numbers where available
- **Book chapter support**: Separate editor field with proper metadata structure
- **Author standardization**: All author names in "Last, First" format
- **Quality validated**: Manual verification of all 343 records

#### Documentation
- Complete README with usage instructions and related resources
- Comprehensive DATA_DICTIONARY with field specifications
- CITATION.cff for machine-readable citation
- Technical metadata in JSON format
- TROUBLESHOOTING guide for common issues

#### Data Quality Standards
- All author names standardized to "Last, First; Last, First" format
- Publication types converted to CSL-JSON vocabulary (article-journal, book, chapter)
- Book chapter metadata properly separated (editors, container titles)
- DOI enrichment via CrossRef API
- Manual verification of dates, titles, and identifiers
- ISO 8601 date formatting
- ISO 639-1 language codes
- UTF-8 encoding throughout

#### Related Resources
- Sherwin Carlquist Collection at BRIT: https://fwbg.org/science-conservation/brit-library/the-sherwin-carlquist-collection/
- Sherwin Carlquist Collection - Portal to Texas History: https://texashistory.unt.edu/explore/collections/SJCC/
- California Botanic Garden Herbarium (RSA): https://www.cch2.org/portal/collections/misc/collprofiles.php?collid=17
- California Botanic Garden Xylarium: https://www.cch2.org/portal/collections/misc/collprofiles.php?collid=105
- Wikidata entry: https://www.wikidata.org/wiki/Q2251003

#### Technical Notes
- File format: CSV (UTF-8 encoding)
- Standards compliance: CSL-JSON, Dublin Core, ISO 8601, ISO 639-1
- License: CC0 1.0 Universal (Public Domain Dedication)
- DOI: 10.5281/zenodo.18687469

#### Tools Used
- Python 3 for data processing and standardization
- CrossRef API for DOI metadata enrichment
- OpenRefine for bibliographic data cleaning
- Claude.ai (Anthropic) for data quality refinement and documentation development

---

## Future Versions

Future versions of this dataset will document changes here, including:
- Additional publications discovered
- Corrections to existing records
- Metadata enhancements
- New fields or features

To report errors or suggest additions, please contact Jason H. Best (jbest@brit.org).
