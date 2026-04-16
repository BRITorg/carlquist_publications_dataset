# Data Dictionary: Sherwin Carlquist Publications Dataset

## Overview
This dataset contains bibliographic metadata for 343 scientific publications by botanist Sherwin Carlquist, spanning his career from 1956 through his later works. The dataset follows Citation Style Language (CSL) and Dublin Core metadata standards.

**Version:** 2.0
**Last Updated:** April 17, 2026
**Encoding:** UTF-8  
**Format:** CSV (Comma-Separated Values)  
**Files:** 3 (carlquist_publications.csv, carlquist_journals.csv, carlquist_authors.csv)  
**Records:** 343 publications; 48 journals; 73 co-authors  
**Fields:** 20 (carlquist_publications.csv)

## Field Definitions

### carlquist_publications.csv

##### title
- **Description:** Full title of the publication
- **Data Type:** String (text)
- **Required:** Yes
- **Example:** "On the Generic Limits of Eriophyllum (Compositae) and Related Genera"
- **CSL Mapping:** `title`
- **Dublin Core:** `dc:title`

#### container-title
- **Description:** Name of the journal, book, or other container publication in which the work appears
- **Data Type:** String (text)
- **Required:** For journal articles and book chapters
- **Example:** "American Journal of Botany", "Aliso"
- **CSL Mapping:** `container-title`
- **Dublin Core:** `dc:source`
- **Notes:** Empty for standalone books and monographs

#### year
- **Description:** Four-digit publication year
- **Data Type:** Integer (YYYY format)
- **Required:** Yes
- **Example:** 1965
- **Range:** 1956-2021
- **CSL Mapping:** Part of `issued` date
- **Dublin Core:** `dc:date`

#### issued
- **Description:** Full or partial publication date in ISO 8601 format
- **Data Type:** String (date)
- **Required:** Yes
- **Format:** YYYY, YYYY-MM, or YYYY-MM-DD
- **Example:** "1966-09", "1969-01"
- **CSL Mapping:** `issued`
- **Dublin Core:** `dc:date`
- **Notes:** Precision varies by available source information

#### author
- **Description:** Author name(s) in "Last, First" format; multiple authors separated by semicolons
- **Data Type:** String (text)
- **Required:** Yes
- **Format:** "Last, First; Last, First"
- **Example:** "Carlquist, S.", "Carlquist, S.; Peter H. Raven"
- **CSL Mapping:** `author`
- **Dublin Core:** `dc:creator`
- **Notes:** All publications in this dataset include Sherwin Carlquist as author or co-author

#### editor
- **Description:** Editor name(s) of the book (for book chapters only)
- **Data Type:** String (text)
- **Required:** For book chapters when applicable
- **Format:** "Last, First; Last, First"
- **Example:** "Ewan, J.", "Rundel, Philip W.; Smith, Alan P.; Meinzer, F. C."
- **CSL Mapping:** `editor`
- **Dublin Core:** `dc:contributor`
- **Notes:** Only populated for book chapters (type = chapter); empty for journal articles and standalone books

#### publisher
- **Description:** Name of the publishing organization
- **Data Type:** String (text)
- **Required:** For books and book chapters
- **Example:** "Holt, Rinehart & Winston", "Oxford University Press"
- **CSL Mapping:** `publisher`
- **Dublin Core:** `dc:publisher`
- **Notes:** Empty for journal articles unless specifically noted

#### volume
- **Description:** Volume number of the journal or book series
- **Data Type:** String (may include non-numeric characters)
- **Required:** For journal articles with volume numbers
- **Example:** "13", "29"
- **CSL Mapping:** `volume`
- **Notes:** Empty for publications without volume designation

#### issue
- **Description:** Issue or part number within a volume
- **Data Type:** String (may include non-numeric characters)
- **Required:** When applicable
- **Example:** "7", "3"
- **CSL Mapping:** `issue`
- **Notes:** Empty for books and publications without issue numbers

#### page
- **Description:** Page range or page numbers
- **Data Type:** String
- **Required:** For journal articles and book chapters
- **Format:** "start-end" or single page
- **Example:** "226-239", "49-57"
- **CSL Mapping:** `page`
- **Notes:** Empty for complete books

#### type
- **Description:** Publication type using controlled vocabulary
- **Data Type:** String (controlled vocabulary)
- **Required:** Yes
- **Controlled Values:**
  - `article-journal` - Peer-reviewed journal article
  - `book` - Complete book or monograph
  - `chapter` - Chapter within an edited volume
- **CSL Mapping:** `type`
- **Dublin Core:** `dc:type`
- **Notes:** Follows CSL-JSON naming conventions

#### container-ISSN
- **Description:** International Standard Serial Number for the journal (print version)
- **Data Type:** String
- **Required:** When available for journal publications
- **Format:** ####-####
- **Example:** "0067-1924", "0030-8870"
- **CSL Mapping:** `container-ISSN`
- **Notes:** Empty for books and publications without assigned ISSN

#### container-eISSN
- **Description:** Electronic International Standard Serial Number (online version)
- **Data Type:** String
- **Required:** When available for journal publications
- **Format:** ####-####
- **Example:** "1444-9862", "1534-6188"
- **CSL Mapping:** `container-eISSN`
- **Notes:** Many older publications lack eISSN

#### container-ISBN
- **Description:** International Standard Book Number
- **Data Type:** String
- **Required:** For books and book chapters when available
- **Format:** 10 or 13 digits (may include hyphens)
- **Example:** "9780028443607"
- **CSL Mapping:** `container-ISBN`
- **Notes:** Empty for journal articles

#### container-OCLC-number
- **Description:** OCLC (WorldCat) control number for library catalog identification
- **Data Type:** String (numeric)
- **Required:** When available
- **Example:** "327635", "765549"
- **Notes:** Primarily available for books; useful for library lookups

#### DOI
- **Description:** Digital Object Identifier - persistent identifier for the publication
- **Data Type:** String
- **Required:** When available
- **Format:** 10.####/suffix
- **Example:** "10.1002/j.1537-2197.1956.tb10512.x"
- **CSL Mapping:** `DOI`
- **Dublin Core:** `dc:identifier`
- **Notes:** Many older publications (pre-2000) lack DOIs; some DOIs added retrospectively

#### URL
- **Description:** Web address for accessing the publication
- **Data Type:** String (valid URL)
- **Required:** When available
- **Format:** Full URL including protocol
- **Example:** "www.jstor.org/stable/10.2307/41422881", "https://www.biodiversitylibrary.org/part/247292"
- **CSL Mapping:** `URL`
- **Dublin Core:** `dc:identifier`
- **Notes:** May include JSTOR links, publisher links, or institutional repositories; not normalized to include "https://" prefix in all cases

#### language
- **Description:** Language of the publication using ISO 639-1 codes
- **Data Type:** String
- **Required:** Yes
- **Format:** Two-letter ISO 639-1 code
- **Example:** "en" (English)
- **CSL Mapping:** `language`
- **Dublin Core:** `dc:language`
- **Notes:** All publications in this dataset are in English

#### wikidata-id
- **Description:** Wikidata identifier (QID) for the publication
- **Data Type:** String
- **Required:** When available
- **Format:** Q followed by digits (Wikidata QID format)
- **Example:** "Q93973579", "Q100376810"
- **CSL Mapping:** N/A (extension field)
- **Dublin Core:** `dc:identifier`
- **Notes:** Links to the Wikidata item for this publication. Obtained through OpenRefine reconciliation and manual curation against Wikidata. Coverage: 100% of records (343 of 343 publications). Can be used to construct full Wikidata URL: https://www.wikidata.org/wiki/{wikidata-id}

#### wikidata-url
- **Description:** Full URL to the Wikidata item for this publication
- **Data Type:** String (URL)
- **Required:** When available
- **Format:** https://www.wikidata.org/wiki/Q#####
- **Example:** "https://www.wikidata.org/wiki/Q93973579"
- **CSL Mapping:** N/A (extension field)
- **Dublin Core:** `dc:identifier`
- **Notes:** Derived from wikidata-id. Provided as a convenience field for users who prefer a directly clickable URL.

---

### carlquist_journals.csv

Lookup table of all journals represented in the publications dataset. 48 records.

#### journal-title
- **Description:** Full journal title
- **Data Type:** String (text)
- **Required:** Yes
- **Unique:** Yes
- **Example:** "American Journal of Botany", "Aliso"
- **Notes:** Matches values appearing in the `container-title` field of carlquist_publications.csv

#### wikidata-url
- **Description:** Full URL to the Wikidata item for this journal
- **Data Type:** String (URL)
- **Required:** When available
- **Format:** https://www.wikidata.org/wiki/Q#####
- **Example:** "https://www.wikidata.org/wiki/Q3456931"

#### wikidata-id
- **Description:** Wikidata QID for this journal
- **Data Type:** String
- **Required:** When available
- **Format:** Q followed by digits
- **Example:** "Q3456931"

#### ISSN
- **Description:** Print International Standard Serial Number for the journal
- **Data Type:** String
- **Required:** When available
- **Format:** ####-####
- **Example:** "0002-9122"

#### eISSN
- **Description:** Electronic International Standard Serial Number for the journal
- **Data Type:** String
- **Required:** When available
- **Format:** ####-####
- **Example:** "1537-2197"
- **Notes:** Not available for all journals, particularly older publications

---

### carlquist_authors.csv

Lookup table of all co-authors appearing in the publications dataset, with name variants and Wikidata identifiers. 73 records. Sherwin Carlquist himself is not included as he is the subject of the dataset.

#### author-as-cited
- **Description:** Author name exactly as it appears in the `author` field of carlquist_publications.csv
- **Data Type:** String (text)
- **Required:** Yes
- **Format:** "Last, First" (as cited in publication)
- **Example:** "Zona, S.", "Wilson, Carol A."
- **Notes:** May reflect abbreviated or variant forms used in original publications

#### author-full
- **Description:** Expanded author name with full or more complete given name where known
- **Data Type:** String (text)
- **Required:** Yes
- **Format:** "First Middle Last"
- **Example:** "Scott Zona", "Carol A. Wilson"

#### author-full-reconciled
- **Description:** If the author name could be reconciled with Wikidata, the full/canonical name is included here, otherwise it is the same as `author-full`.
- **Data Type:** String (text)
- **Required:** Yes
- **Notes:** Represents the preferred form of the name for identity resolution purposes

#### wikidata-url
- **Description:** Full URL to the Wikidata item for this person
- **Data Type:** String (URL)
- **Required:** When available
- **Format:** https://www.wikidata.org/wiki/Q#####
- **Example:** "https://www.wikidata.org/wiki/Q1234567"

#### wikidata-id
- **Description:** Wikidata QID for this person
- **Data Type:** String
- **Required:** When available
- **Format:** Q followed by digits
- **Example:** "Q1234567"
- **Notes:** Multiple rows may share a QID when the same person is cited under variant name forms

---

## Data Quality Notes

### Completeness
- All records include: title, author, year, issued date, type, and language
- DOIs are present for approximately 40% of records (varies by publication era)
- Wikidata IDs are present for 100% of publication records (343 of 343)
- Wikidata IDs are present for all 48 journals and a subset of the 73 co-authors
- ISBNs and OCLC numbers primarily available for books (14 book records)
- URLs available for many but not all publications

### Known Limitations
1. **Date precision:** Some older publications only have year-level precision
2. **Retrospective DOIs:** Some DOIs were assigned years after original publication
3. **URL stability:** External URLs (especially journal publisher sites) may change over time
4. **ISSN coverage:** Electronic ISSNs not available for all journals, particularly older publications
5. **Author name format:** Minor variations in formatting may exist for co-authors

### Data Sources
- CrossRef API for DOI metadata
- JSTOR and publisher websites
- Institutional repository records
- Original publication examination
- Biodiversity Heritage Library for historical botanical literature
- Plant Discoveries Sherwin Carlquist website (formerly at https://sherwincarlquist.com)

### Tools and Software Used
- Python 3 for data processing and standardization
- CrossRef API for DOI metadata enrichment
- OpenRefine for bibliographic data cleaning
- Claude.ai (Anthropic) for data quality refinement and documentation development

## Controlled Vocabularies

### Publication Type (`type` field)
- `article-journal` - Journal article or paper
- `book` - Monograph or complete book
- `chapter` - Chapter in an edited volume

### Language (`language` field)
- `en` - English (all publications in this dataset)

## Related Resources

### Wikibase Extended Specimen Network
This dataset is part of the Sherwin Carlquist Digital Extended Specimen Network, which links these publications to physical botanical specimens, field notes, and archival materials.

### Sherwin Carlquist in Wikidata
Sherwin Carlquist (1930-2021) has a Wikidata entry at:
- **Wikidata QID:** Q2251003
- **URL:** https://www.wikidata.org/wiki/Q2251003

### Subject Coverage
Publications primarily focus on:
- Wood anatomy
- Plant systematics and taxonomy
- Compositae (Asteraceae) family
- Island biogeography
- Pacific island flora
- Plant evolution
- Long-distance dispersal

## Usage Guidelines

### Citation
When using this dataset, please use format as recommended on publishing platform or refer to the CITATION.cff file.

### License
CC0 1.0 Universal (Public Domain Dedication)

### Data Reuse
This dataset may be:
- Integrated into bibliographic databases
- Used for bibliometric analysis
- Linked to specimen records
- Used in history of science research
- Referenced in botanical research

### Contact
For questions, corrections, additions, or additional information:

**Corresponding Author:**  
Jason H. Best  
Director of Biodiversity Informatics  
Botanical Research Institute of Texas  
Email: jbest@brit.org  
ORCID: 0000-0002-7414-5523

**Please contact the corresponding author for:**
- Corrections to dataset entries
- Additions or updates to publication records
- Questions about data quality or provenance
- General inquiries about the dataset

**Co-Author:**  
Amanda Gomez  
Texas Christian University  
ORCID: 0009-0003-3105-735X

**Institution:** Fort Worth Botanic Garden / Botanical Research Institute of Texas  
**Related Project:** Sherwin Carlquist Digital Extended Specimen Network  
**DOI:** 10.5281/zenodo.18687469

## Version History

For complete version history, see [CHANGELOG.md](CHANGELOG.md).

**Current Version:** 2.0 (April 17, 2026)

### Version 2.0 (April 17, 2026)
- Added two companion lookup tables: carlquist_journals.csv (48 records) and carlquist_authors.csv (73 records)
- Added `wikidata-url` field to carlquist_publications.csv (20 fields total)
- Renamed `ISSN` → `container-ISSN`, `eISSN` → `container-eISSN`, `ISBN` → `container-ISBN`, `OCLC-number` → `container-OCLC-number` for CSL-JSON alignment
- Renamed `wikidata_id` → `wikidata-id` for CSL-JSON alignment
- Removed `Wikibase editing results` column
- Wikidata QID coverage for publications now 100% (343 of 343)
- Added Frictionless Data descriptor (datapackage.json) covering all three CSVs

### Version 1.1 (March 26, 2026)
- Added wikidata-id field (19 fields total)
- Wikidata identifiers added for 107 publications (~31% coverage)
- Obtained through OpenRefine reconciliation against Wikidata
- No changes to other field definitions or data structure

### Version 1.0 (February 18, 2026)
- Initial public release
- 343 publication records spanning 1956-2021
- 18 standardized fields following CSL-JSON and Dublin Core
- Complete field documentation
- Includes book chapter metadata with editor field
- DOI enrichment from CrossRef API
- All publications in English (language code: en)
