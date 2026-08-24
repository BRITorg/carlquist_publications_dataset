# Adding or Editing a Publication Record

This is the checklist for adding a single new Carlquist publication to the dataset,
or correcting an existing one. For bulk reconciliation of many records against
Wikidata at once, OpenRefine remains the tool of choice (see `DATA_DICTIONARY.md`).
For batch-creating Wikidata items for existing multi-author CSV rows, see
`tools/generate_qs_multiauthor.py`. This checklist is for the common one-off case:
you've found a single publication that isn't in the dataset yet.

## Tools

| Tool | Purpose |
|---|---|
| `tools/add_publication.py` | Draft a Wikidata QuickStatements block for one new record, then produce the finished CSV row once the item exists |
| `tools/qs_common.py` | Shared QuickStatements-building logic used by `add_publication.py` and `generate_qs_multiauthor.py` — not run directly |
| `tools/bump_version.py` | Version/date/count consistency check and version bump |
| `tools/new_publication.example.json` | Template for the `--json` input to `add_publication.py` |

## Checklist

### 1. Verify the bibliographic facts

Confirm title, author(s), journal, volume, issue, pages, and publication date from
the primary source (BHL, the journal's own site, etc.), not just a secondary
citation. Note the source URL — it goes in the `URL` field.

### 2. Check it isn't already in the dataset or on Wikidata

- [ ] Search `carlquist_publications.csv` for the title (`add_publication.py draft`
  does an automatic substring/exact check and warns on stderr, but do a manual
  look too if the title might have been transcribed differently)
- [ ] Search Wikidata for an existing item before assuming one needs to be created

### 3. Confirm journal and author(s) have Wikidata QIDs

- [ ] Journal: look up `container-title` in `carlquist_journals.csv`. If missing,
  it needs its own Wikidata item / QID added to that lookup table first.
- [ ] Author(s): look up each `author-as-cited` value in `carlquist_authors.csv`.
  If a co-author has no QID, that's fine — the QuickStatements draft will use
  P2093 (author name string) instead of P50, same as existing records.

### 4. Draft the Wikidata QuickStatements block

```
cd tools
python3 add_publication.py draft --json new_record.json > qs_draft.txt
```

(copy `new_publication.example.json` as a starting point for `new_record.json`)

Review `qs_draft.txt` and the stderr warnings. Fix any missing journal QID,
unexpected duplicate-title warning, etc. before moving on.

### 5. Human review, then submit

**Do not let Claude submit this to Wikidata directly** — it's a public,
essentially-permanent edit. Review the draft yourself, then run it in your own
logged-in QuickStatements session (https://quickstatements.toolforge.org/). Note
the QID it returns for the new item.

### 6. Finalize the CSV row

```
python3 add_publication.py finalize --json new_record.json --wikidata-id Q12345678
```

This prints the exact row that will be appended — check it, then re-run with
`--write` to actually append it to `carlquist_publications.csv`.

- [ ] If the journal or an author was new (added to their lookup table in step 3),
  double check that row was added correctly too.

### 7. Update documentation and version

- [ ] Bump record count (343 -> N) in `README.md`, `DATA_DICTIONARY.md`,
  `dataset_metadata.json`
- [ ] Add a `CHANGELOG.md` entry describing the addition
- [ ] Decide the version bump (see `CLAUDE.md` — a new record is usually a
  **minor** bump) and run `python3 tools/bump_version.py NEW_VERSION YYYY-MM-DD`

### 8. Validate before committing

```
python3 tools/bump_version.py --check
source .venv/bin/activate && frictionless validate datapackage.json
```

Both must pass clean. Then commit.
