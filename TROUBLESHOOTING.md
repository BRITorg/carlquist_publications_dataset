# Troubleshooting Guide

This guide addresses common issues when working with the Carlquist Publications dataset.

---

## Opening the Dataset in Microsoft Excel

Microsoft Excel has several known issues when opening CSV files that can affect data display and integrity.

### Issue 1: Date Formatting

**Problem:** Excel automatically converts ISO 8601 dates (like `1957-05-23`) to its own date format, which can alter the display and cause issues with data processing.

**Solution:** Import the CSV properly instead of double-clicking it.

#### Method 1: Import from Text/CSV (Recommended)

1. Open Excel (start with a blank workbook)
2. Go to **Data > Get Data > From Text/CSV** (or "From File" in older Excel versions)
3. Select the `carlquist_publications.csv` file
4. In the import wizard, set the `issued` column data type to **Text** (not Date)
5. Click **Load**

This preserves the original ISO 8601 date format.

#### Method 2: Use Power Query

1. Open Excel
2. Go to **Data > Get Data > From File > From Text/CSV**
3. In Power Query Editor:
   - Right-click the `issued` column header
   - Select **Change Type > Text**
4. Click **Close & Load**

### Issue 2: Diacritics and Special Characters

**Problem:** Excel may not correctly display diacritics (accented characters) in author names, titles, or other fields when opening CSV files directly. Characters like é, ñ, ü, ö may appear as garbled text.

**Example Issues:**
- "José" displays as "JosÃ©"
- "François" displays as "FranÃ§ois"
- "Müller" displays as "MÃ¼ller"

**Solution:** Use the proper import method described above (Data > From Text/CSV). This ensures Excel reads the UTF-8 encoding correctly.

**Alternative:** If characters still appear incorrect:
1. In the import wizard, ensure encoding is set to **UTF-8** (usually "65001: Unicode (UTF-8)")
2. If that option isn't available, try importing with encoding set to **Unicode**

### Issue 3: Leading Zeros in Identifiers

**Problem:** Excel may remove leading zeros from fields like OCLC numbers or ISSNs.

**Solution:** Use the import method above and set these columns as **Text** type.

---

## Alternative Tools (Excel Alternatives)

If Excel continues to cause problems, consider these alternatives:

### For Viewing/Editing:
- **Google Sheets** - Opens CSV files correctly by default, preserves UTF-8 encoding
- **LibreOffice Calc** - Free, open-source spreadsheet software with better CSV handling
- **Visual Studio Code** - With CSV extension for viewing/editing
- **CSVed** - Dedicated CSV editor for Windows

### For Analysis:
- **R** - Use `read.csv("carlquist_publications.csv", encoding="UTF-8")`
- **Python/Pandas** - Use `pd.read_csv("carlquist_publications.csv", encoding="utf-8")`
- **OpenRefine** - Excellent for data exploration and cleaning

---

## Other Common Issues

### Issue: File Won't Open

**Problem:** Error message when trying to open the CSV file.

**Possible Causes:**
1. File is corrupted during download
2. Wrong application is set as default for .csv files
3. File is still compressed (in a ZIP archive)

**Solutions:**
1. Re-download the file from Zenodo or GitHub
2. Right-click the file → Open With → Choose appropriate application
3. Extract the ZIP archive first if downloaded from Zenodo

### Issue: Missing or Incorrect Data

**Problem:** Some fields appear empty or have unexpected values.

**Check:**
1. Empty fields in the dataset are intentional - not all publications have all metadata (e.g., books don't have ISSN)
2. See [DATA_DICTIONARY.md](DATA_DICTIONARY.md) for which fields are expected for each publication type
3. The `language` field is "en" for all records (all publications are in English)

### Issue: Special Characters in File Paths

**Problem:** Error opening the file if it's saved in a path with special characters or non-English letters.

**Solution:** Move the file to a simpler path like `C:\Data\` or `~/Documents/`

---

## Getting Help

If you encounter issues not covered here:

1. **Check the README** - [README.md](README.md) has general usage information
2. **Check the Data Dictionary** - [DATA_DICTIONARY.md](DATA_DICTIONARY.md) explains all fields
3. **Report Issues** - If you find data errors or have questions, please contact:
   - Jason H. Best, Director of Biodiversity Informatics
   - Email: jbest@brit.org
   - GitHub Issues: (if viewing on GitHub)

---

## Quick Reference: Import Settings for Excel

| Column | Data Type |
|--------|-----------|
| title | Text |
| container-title | Text |
| year | Text (or Number) |
| issued | **Text** (important!) |
| author | Text |
| editor | Text |
| publisher | Text |
| volume | Text |
| issue | Text |
| page | Text |
| type | Text |
| ISSN | Text |
| eISSN | Text |
| ISBN | Text |
| OCLC-number | Text |
| DOI | Text |
| URL | Text |
| language | Text |

**Note:** While some fields contain numbers (year, volume, issue), importing them as Text prevents Excel from applying unwanted automatic formatting.
