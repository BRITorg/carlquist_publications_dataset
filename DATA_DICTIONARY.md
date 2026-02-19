# Data Dictionary: Sherwin Carlquist Publications Dataset

## Overview
This dataset contains bibliographic metadata for 343 scientific publications by botanist Sherwin Carlquist, spanning his career from 1956 through his later works. The dataset follows Citation Style Language (CSL) and Dublin Core metadata standards.

**Version:** 1.0  
**Last Updated:** February 18, 2026  
**Encoding:** UTF-8  
**Format:** CSV (Comma-Separated Values)  
**Records:** 343 publications  
**Fields:** 18

## Field Definitions

### title
- **Description:** Full title of the publication
- **Data Type:** String (text)
- **Required:** Yes
- **Example:** "On the Generic Limits of Eriophyllum (Compositae) and Related Genera"
- **CSL Mapping:** `title`
- **Dublin Core:** `dc:title`

### container-title
- **Description:** Name of the journal, book, or other container publication in which the work appears
- **Data Type:** String (text)
- **Required:** For journal articles and book chapters
- **Example:** "American Journal of Botany", "Aliso"
- **CSL Mapping:** `container-title`
- **Dublin Core:** `dc:source`
- **Notes:** Empty for standalone books and monographs

### year
- **Description:** Four-digit publication year
- **Data Type:** Integer (YYYY format)
- **Required:** Yes
- **Example:** 1965
- **Range:** 1956-2021
- **CSL Mapping:** Part of `issued` date
- **Dublin Core:** `dc:date`

### issued
- **Description:** Full or partial publication date in ISO 8601 format
- **Data Type:** String (date)
- **Required:** Yes
- **Format:** YYYY, YYYY-MM, or YYYY-MM-DD
- **Example:** "1966-09", "1969-01"
- **CSL Mapping:** `issued`
- **Dublin Core:** `dc:date`
- **Notes:** Precision varies by available source information

### author
- **Description:** Author name(s) in "Last, First" format; multiple authors separated by semicolons
- **Data Type:** String (text)
- **Required:** Yes
- **Format:** "Last, First; Last, First"
- **Example:** "Carlquist, S.", "Carlquist, S.; Peter H. Raven"
- **CSL Mapping:** `author`
- **Dublin Core:** `dc:creator`
- **Notes:** All publications in this dataset include Sherwin Carlquist as author or co-author

### editor
- **Description:** Editor name(s) of the book (for book chapters only)
- **Data Type:** String (text)
- **Required:** For book chapters when applicable
- **Format:** "Last, First; Last, First"
- **Example:** "Ewan, J.", "Rundel, Philip W.; Smith, Alan P.; Meinzer, F. C."
- **CSL Mapping:** `editor`
- **Dublin Core:** `dc:contributor`
- **Notes:** Only populated for book chapters (type = chapter); empty for journal articles and standalone books

### publisher
- **Description:** Name of the publishing organization
- **Data Type:** String (text)
- **Required:** For books and book chapters
- **Example:** "Holt, Rinehart & Winston", "Oxford University Press"
- **CSL Mapping:** `publisher`
- **Dublin Core:** `dc:publisher`
- **Notes:** Empty for journal articles unless specifically noted

### volume
- **Description:** Volume number of the journal or book series
- **Data Type:** String (may include non-numeric characters)
- **Required:** For journal articles with volume numbers
- **Example:** "13", "29"
- **CSL Mapping:** `volume`
- **Notes:** Empty for publications without volume designation

### issue
- **Description:** Issue or part number within a volume
- **Data Type:** String (may include non-numeric characters)
- **Required:** When applicable
- **Example:** "7", "3"
- **CSL Mapping:** `issue`
- **Notes:** Empty for books and publications without issue numbers

### page
- **Description:** Page range or page numbers
- **Data Type:** String
- **Required:** For journal articles and book chapters
- **Format:** "start-end" or single page
- **Example:** "226-239", "49-57"
- **CSL Mapping:** `page`
- **Notes:** Empty for complete books

### type
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

### ISSN
- **Description:** International Standard Serial Number for the journal (print version)
- **Data Type:** String
- **Required:** When available for journal publications
- **Format:** ####-####
- **Example:** "0067-1924", "0030-8870"
- **CSL Mapping:** `ISSN`
- **Notes:** Empty for books and publications without assigned ISSN

### eISSN
- **Description:** Electronic International Standard Serial Number (online version)
- **Data Type:** String
- **Required:** When available for journal publications
- **Format:** ####-####
- **Example:** "1444-9862", "1534-6188"
- **CSL Mapping:** `ISSN` (electronic variant)
- **Notes:** Many older publications lack eISSN

### ISBN
- **Description:** International Standard Book Number
- **Data Type:** String
- **Required:** For books and book chapters when available
- **Format:** 10 or 13 digits (may include hyphens)
- **Example:** "9780028443607"
- **CSL Mapping:** `ISBN`
- **Notes:** Empty for journal articles

### OCLC-number
- **Description:** OCLC (WorldCat) control number for library catalog identification
- **Data Type:** String (numeric)
- **Required:** When available
- **Example:** "327635", "765549"
- **Notes:** Primarily available for books; useful for library lookups

### DOI
- **Description:** Digital Object Identifier - persistent identifier for the publication
- **Data Type:** String
- **Required:** When available
- **Format:** 10.####/suffix
- **Example:** "10.1002/j.1537-2197.1956.tb10512.x"
- **CSL Mapping:** `DOI`
- **Dublin Core:** `dc:identifier`
- **Notes:** Many older publications (pre-2000) lack DOIs; some DOIs added retrospectively

### URL
- **Description:** Web address for accessing the publication
- **Data Type:** String (valid URL)
- **Required:** When available
- **Format:** Full URL including protocol
- **Example:** "www.jstor.org/stable/10.2307/41422881", "https://www.biodiversitylibrary.org/part/247292"
- **CSL Mapping:** `URL`
- **Dublin Core:** `dc:identifier`
- **Notes:** May include JSTOR links, publisher links, or institutional repositories; not normalized to include "https://" prefix in all cases

### language
- **Description:** Language of the publication using ISO 639-1 codes
- **Data Type:** String
- **Required:** Yes
- **Format:** Two-letter ISO 639-1 code
- **Example:** "en" (English)
- **CSL Mapping:** `language`
- **Dublin Core:** `dc:language`
- **Notes:** All publications in this dataset are in English

## Data Quality Notes

### Completeness
- All records include: title, author, year, issued date, type, and language
- DOIs are present for approximately 40% of records (varies by publication era)
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
When using this dataset, please cite:

> Gomez, Amanda; Best, Jason H. (2026). Sherwin Carlquist Publications Dataset (Version 1.0-alpha.1) [Data set]. Zenodo. https://doi.org/10.5281/zenodo.18624213

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

### Version 1.0.1 (February 19, 2026)
- Updated DOI references to published Zenodo DOI (10.5281/zenodo.18687469)
- No changes to field definitions or data structure

### Version 1.0 (February 18, 2026)
- Initial public release
- 343 publication records spanning 1956-2021
- 18 standardized fields following CSL-JSON and Dublin Core
- Complete field documentation
- Includes book chapter metadata with editor field
- DOI enrichment from CrossRef API
- All publications in English (language code: en)
