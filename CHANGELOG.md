# Changelog

All notable changes to this dataset will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
