# Sherwin Carlquist Publications Dataset

## Description

This dataset contains comprehensive bibliographic metadata for 343 scientific publications by renowned botanist Sherwin Carlquist (1930-2021). The collection spans from 1956 through his later career and documents his extensive contributions to plant systematics, wood anatomy, island biogeography, and evolutionary biology.

Carlquist's work was foundational in understanding plant evolution on Pacific islands, wood anatomy across flowering plant families (particularly Compositae/Asteraceae), and the mechanisms of long-distance plant dispersal. This bibliographic compilation serves as a comprehensive record of his scholarly output and provides structured metadata for integration with botanical collections, specimen records, and digital humanities research.

## Contents

This dataset includes the following files:

- **carlquist_publications.csv** - Main bibliographic data in CSV format (343 records)
- **DATA_DICTIONARY.md** - Complete field definitions and metadata documentation
- **README.md** - This file
- **CITATION.cff** - Machine-readable citation format
- **dataset_metadata.json** - Technical metadata in JSON format

## Technical Details

- **Format:** CSV (Comma-Separated Values)
- **Encoding:** UTF-8
- **Standards:** Citation Style Language (CSL-JSON), Dublin Core
- **Records:** 343 publications
- **Date Range:** 1956-2021
- **Version:** 1.0.1

## Dataset Structure

The CSV contains 18 standardized fields following Citation Style Language (CSL-JSON) and Dublin Core metadata conventions:

- **title** - Publication title (100%)
- **container-title** - Journal or book name (95%, N/A for standalone books)
- **year** - Publication year, YYYY format (100%)
- **issued** - Full publication date, ISO 8601 (100%)
- **author** - Author name(s) in "Last, First" format, separated by semicolons (100%)
- **editor** - Book editor name(s) in "Last, First" format (book chapters only)
- **publisher** - Publisher name (100% for books)
- **volume** - Volume number (~90% for journals)
- **issue** - Issue number (~85% for journals)
- **page** - Page range (~95%)
- **type** - Publication type: article-journal, book, chapter (100%)
- **ISSN** - Print ISSN (~80% for journals)
- **eISSN** - Electronic ISSN (~40% for journals)
- **ISBN** - Book identifier (100% for books)
- **OCLC-number** - WorldCat control number (~50% for books)
- **DOI** - Digital Object Identifier (~40%)
- **URL** - Web address (~60%)
- **language** - ISO 639-1 language code (100%)

See **DATA_DICTIONARY.md** for complete field specifications.

## Working with the Dataset

### Opening in Spreadsheet Applications

**Note for Excel Users:** Microsoft Excel may automatically reformat dates and special characters when opening CSV files. This can affect the display of publication dates and author names with diacritics. 

For proper import instructions and solutions, see **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)**.

**Recommended alternatives:**
- Google Sheets (preserves formatting automatically)
- LibreOffice Calc
- R, Python/Pandas, or other programmatic tools

## Publication Breakdown

- **Journal Articles:** 329 records (~96%)
- **Books:** 7 records (~2%)
- **Book Chapters:** 7 records (~2%)

### Major Publication Venues

Most frequent journals:
- *Aliso* (journal of Rancho Santa Ana Botanic Garden, now California Botanic Garden)
- *American Journal of Botany*
- *Brittonia*
- *Pacific Science*
- *Phytomorphology*

### Thematic Coverage

Publications primarily address:
- Wood anatomy of flowering plants (particularly Compositae family)
- Plant systematics and taxonomy
- Island biogeography and biogeography theory
- Evolution in island ecosystems
- Long-distance plant dispersal mechanisms
- Pacific island flora
- Comparative plant anatomy

## Data Quality

### Strengths
- Comprehensive coverage of Carlquist's peer-reviewed publications
- Standardized metadata following international standards (CSL-JSON, Dublin Core)
- Enriched with DOIs, ISSNs, and persistent identifiers where available
- Language codes following ISO 639-1 standard
- Author names standardized to "Last, First" format

### Limitations
- DOI coverage varies by publication era (stronger for post-2000 publications)
- Some older publications lack electronic identifiers (eISSN, DOI)
- URL stability depends on external publisher and repository policies
- Date precision varies (some records only include year)

## Related Projects

This dataset is part of the **Sherwin Carlquist Digital Extended Specimen Network**, a collaborative project between:
- Botanical Research Institute of Texas (BRIT)
- California Botanic Garden
  
### Sherwin Carlquist Collection at BRIT

The physical collection and additional information about the Extended Specimen Network project are available at:  
https://fwbg.org/science-conservation/brit-library/the-sherwin-carlquist-collection/

### Sherwin Carlquist Collection - Portal to Texas History

Digital materials from the Sherwin Carlquist Collection are available through The Portal to Texas History:  
https://texashistory.unt.edu/explore/collections/SJCC/

### California Botanic Garden Collections (formerly Rancho Santa Ana Botanic Garden)

**Herbarium (RSA-VascularPlants):**  
https://www.cch2.org/portal/collections/misc/collprofiles.php?collid=17

**Xylarium (RSA-Wood):**  
https://www.cch2.org/portal/collections/misc/collprofiles.php?collid=105

### Sherwin Carlquist in Wikidata

Sherwin Carlquist (1930-2021) has a Wikidata entry at:
- **Wikidata QID:** Q2251003
- **URL:** https://www.wikidata.org/wiki/Q2251003

## Usage

### Academic Research
- Bibliometric analysis of botanical research
- History of science studies
- Understanding development of wood anatomy and island biogeography as fields
- Citation analysis

### Collections Management
- Linking publications to herbarium specimens
- Enhanced specimen data through published research
- Creating extended specimen records

### Data Integration
- Import into reference management systems (Zotero, Mendeley, EndNote)
- Integration with Wikidata and other linked open data platforms
- Connection to botanical databases and specimen repositories

### Example Use Cases

1. **Specimen annotation:** Link herbarium specimens to published research describing those specimens
2. **Research trajectory analysis:** Examine evolution of Carlquist's research interests over time
3. **Collaborative network mapping:** Identify co-authors and institutional collaborations
4. **Geographic research patterns:** Map research focus by geographic region (Pacific islands, California flora, etc.)

## How to Cite

When using this dataset, please cite as recommended in Zenodo.

## License

**CC0 1.0 Universal (Public Domain Dedication)**

This work has been dedicated to the public domain. You can copy, modify, distribute and perform the work, even for commercial purposes, all without asking permission.

## Contributors

**Dataset Compilation and Curation:**
- Amanda Gomez, Texas Christian University (ORCID: 0009-0003-3105-735X)
- Jason H. Best, Botanical Research Institute of Texas (ORCID: 0000-0002-7414-5523) - *Corresponding Author*

**Collaborative Partners:**
- California Botanic Garden
- Botanical Research Institute of Texas

## Data Sources

Bibliographic metadata compiled from:
- CrossRef DOI database
- JSTOR digital library
- Publisher websites and repositories
- Biodiversity Heritage Library
- Plant Discoveries Sherwin Carlquist website (formerly at https://sherwincarlquist.com)
- Original publication examination

## Contact

**For corrections, additions, or inquiries about this dataset, please contact:**

**Jason H. Best** (Corresponding Author)  
Director of Biodiversity Informatics  
Botanical Research Institute of Texas at the  
Fort Worth Botanic Garden  
Email: jbest@brit.org  
ORCID: 0000-0002-7414-5523

The corresponding author welcomes:
- Corrections to dataset entries
- Additions or updates to publication records
- Questions about data quality or provenance
- General inquiries about the dataset or Extended Specimen Network project

**Amanda Gomez**  
Texas Christian University  
ORCID: 0009-0003-3105-735X

## Acknowledgments

This work builds upon the extraordinary scientific legacy of Dr. Sherwin Carlquist, whose contributions to botanical science continue to influence research in plant systematics, anatomy, and biogeography. We are grateful to California Botanic Garden for their partnership in the Extended Specimen Network project and for their stewardship of the Carlquist research archive.

Dataset preparation was assisted by Claude.ai (Anthropic) for data standardization, quality control, and documentation development.

## Version History

**Version 1.0** (February 18, 2026)
- Initial public release
- 343 bibliographic records spanning 1956-2021
- 18 standardized metadata fields (CSL-JSON and Dublin Core compliant)
- Complete documentation and related resource links

---

*For technical documentation of field definitions, data types, and controlled vocabularies, please consult DATA_DICTIONARY.md*
