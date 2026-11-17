# Changelog

All notable changes to this dataset will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.2] - 2026-09-16

Changes in this version came out of an independent reconciliation: a separate
publication list was compiled from OpenAlex, Crossref and Carlquist's own curated
bibliography (recovered from an Internet Archive snapshot of his now-parked
website), then matched record-for-record against v2.1. 343 of the 344 v2.1 records
matched; the differences are resolved below.

### Added
- Three publication records, each verified against Crossref (title, journal,
  volume, issue, pages, date, byline) rather than from a secondary citation:
  - "Vessels in Ferns: Structural, Ecological, and Evolutionary Significance"
    (Carlquist & Schneider, *American Journal of Botany* 88(1):1-13, 2001).
    A Wikidata item already existed (Q46126499) and was enriched rather than
    duplicated; its DOI was wrong (`10.1006/ANBO.2001.1430`, which belongs to a
    different paper in *Annals of Botany* sharing the volume and issue number) and
    is now deprecated in favour of `10.2307/2657121`.
  - "Terminology of Imperforate Tracheary Elements: A Reply" (Carlquist,
    *IAWA Bulletin* 7(2):168-170, 1986; Q141485296). Distinct from the existing
    7(1):75-81 record it replies to.
  - "Vestured Pits in Echium (Boraginaceae): Island Woodiness Revisited"
    (Carlquist, *Aliso* 35(1):28-40, 2017; Q141485298).
- `openalex-id` and `openalex-url` fields in `carlquist_publications.csv`
  (22 fields total). `openalex-id` is the OpenAlex work identifier, corresponding
  to Wikidata property P10283; `openalex-url` is derived from it, following the
  existing `wikidata-id`/`wikidata-url` convention. Coverage is 91% (315 of 346):
  275 resolved by exact DOI match against the OpenAlex API, 40 by verified
  title-and-year match. The 31 records without a value have no OpenAlex record at
  all — they are papers in pre-DOI journals (*Tropical Woods*, *Phytomorphology*,
  *Allertonia*, *Botaniska Notiser*, *Botanische Jahrbücher*, *Madroño*, *Memoirs
  of the New York Botanical Garden*, *University of California Publications in
  Botany*, *American Scientist*) plus nine chapters in edited volumes.
- `MAINTENANCE_NOTES.md` — a maintainer-facing record of the traps that no
  validation step catches: Wikidata QID rot and the redirect check, searching for an
  existing item before a CREATE, verifying that a QuickStatements batch landed, the
  OpenAlex records that must not be confused, the LibreOffice lock hazard on the CSV,
  line endings, `datapackage.json` regex escaping, and which source to trust when
  Carlquist's own bibliography disagrees with Crossref.
- `tools/qs_common.py` now emits a P10283 statement when a record carries an
  `openalex-id`, so newly created Wikidata items get the identifier at creation.
- P10283 was pushed to the pre-existing Wikidata items for records in this dataset
  via a QuickStatements batch of 313 statements. None of the 313 items carried the
  property beforehand (verified against the Wikidata API before the batch ran).
  Verified after the run: 312 of 313 landed with the expected value and none
  received a wrong one. The remaining statement was generated against Q139119348,
  which had since become a redirect to Q56211461 — QuickStatements does not write
  to redirected QIDs — and was reissued against Q56211461. Final state, verified
  against the Wikidata API: all 315 records with an `openalex-id` have a Wikidata
  item carrying that same value as P10283.

### Changed
- `Wood Anatomy of Dipsacaceae` (1982): volume corrected from 34 to 31. Taxon
  volume 31 is the 1982 volume — confirmed by a Crossref query on ISSN 0040-0262,
  and Carlquist's own bibliography also gives "Taxon 31:443-450".
- Record count updated from 344 to 346 publications in `README.md`,
  `DATA_DICTIONARY.md`, and `dataset_metadata.json`; field count from 20 to 22.
- "Vegetative Anatomy of the New Caledonian Endemic Amborella Trichopoda":
  `wikidata-id` updated from Q139119348 to **Q56211461**. The two items were merged
  on Wikidata and Q139119348 is now a redirect; Q56211461 is the surviving item and
  the richer record, carrying both authors as P50 rather than name strings. Its
  `issue` was also filled in as 3 (Pacific Science 55(3):305-312, confirmed in
  Crossref), which was previously blank. All 346 `wikidata-id` values plus the 48
  journal and 42 author QIDs in the lookup tables were checked for redirects and
  deletions; this was the only stale one.
- Corrected the author-table count in `README.md` and `DATA_DICTIONARY.md`, which
  said "73 co-authors" from v2.0 onward. `carlquist_authors.csv` has 72 rows and one
  of them is Carlquist himself, so it is 72 author records — Carlquist plus 71
  co-authors — of which 42 carry a Wikidata QID. The v2.0 changelog entry is left
  as originally published.
- "Stylidium in Arnhem Land: New Species, Modes of Speciation on the Sandstone
  Plateau, and Comments on Floral Mimicry" (*Aliso* 9(3), 1979): title typo
  "Arnherm" corrected to "Arnhem". The misspelling originates in the publisher's
  (Claremont Scholarship) metadata, not in the printed article.
- Normalized the line terminator on the final CSV row, which was the only CRLF
  line in an otherwise LF file.

### Removed
- `Vernon Irvine Cheadle 1910-1995` (Schneider & Carlquist, *Madroño*, 1995,
  Q93957716) — a tribute rather than peer-reviewed output, and therefore outside
  the dataset's stated scope. Removing it makes the scope internally consistent
  with the already-omitted *Philip A. Munz* tribute (*Aliso*, 1975) and *Peter H.
  Raven — Asa Gray Award* citation (*Systematic Botany*, 1997). The Wikidata item
  is unaffected; only this dataset's scope changed.

### Fixed
- `tools/add_publication.py` appended rows with `csv.writer`'s default `\r\n`
  terminator, leaving each added row as the only CRLF line in the file. Now writes
  `\n`.
- `tools/add_publication.py` carries `openalex-id` through `FIELDS`, accepts
  `--openalex-id`, and derives `openalex-url` on `finalize`.

## [2.1] - 2026-08-24

### Added
- New publication record: "Anatomy of the Guayana Mutisieae. Part II" (Carlquist,
  Memoirs of the New York Botanical Garden, 10(1):157-184, 1958), the companion
  piece to the existing 1957 "Anatomy of Guayana mutisieae" (Part I) record.
  Wikidata item created (Q141167197); no changes needed to the journal or author
  lookup tables, as both were already represented.

### Changed
- Record count updated from 343 to 344 publications throughout `README.md`,
  `DATA_DICTIONARY.md`, `dataset_metadata.json`, `datapackage.json`,
  `CITATION.cff`, and `.zenodo.json`.

## [2.0] - 2026-04-17

### ⚠ Breaking Changes
- Renamed `ISSN` → `container-ISSN` in `carlquist_publications.csv` for CSL-JSON alignment
- Renamed `eISSN` → `container-eISSN` in `carlquist_publications.csv` for CSL-JSON alignment
- Renamed `ISBN` → `container-ISBN` in `carlquist_publications.csv` for CSL-JSON alignment
- Renamed `OCLC-number` → `container-OCLC-number` in `carlquist_publications.csv` for CSL-JSON alignment
- Renamed `wikidata_id` → `wikidata-id` in `carlquist_publications.csv` for CSL-JSON alignment
- Removed `Wikibase editing results` column from `carlquist_publications.csv`

### Added
- `carlquist_journals.csv`: new companion lookup table of 48 journals represented in the dataset, with Wikidata QIDs, ISSNs, and eISSNs
- `carlquist_authors.csv`: new companion lookup table of 73 co-authors, with name variants (`author-as-cited`, `author-full`, `author-full-reconciled`) and Wikidata QIDs
- `wikidata-url` field added to `carlquist_publications.csv`, providing full Wikidata item URLs alongside existing `wikidata-id` QIDs
- `datapackage.json`: Frictionless Data descriptor covering all three CSVs with field types, constraints, and foreign key relationships between publications and journals
- Frictionless Data validation support for dataset integrity checking

### Changed
- `carlquist_publications.csv` now contains 20 standardized fields (previously 18 in v1.1)
- Wikidata QID coverage for publications is now 100% following extensive Wikidata reconciliation work

### Note
The primary publications dataset retains all 343 records. Column renames in this version are breaking changes; consumers of v1.x will need to update field references.

---

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
