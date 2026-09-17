# Maintenance Notes

Operational gotchas for maintaining this dataset — things that cost real time to
discover and that no validation step catches. Field definitions live in
`DATA_DICTIONARY.md`; the release procedure lives in `CLAUDE.md` and
`CONTRIBUTING.md`. This file is only for the traps.

---

## Wikidata

### QIDs rot — check for redirects before every release

Items get merged upstream and the old QID becomes a redirect. A stored
`wikidata-id` then silently points at a redirect, and **QuickStatements refuses to
write to a redirected QID** — the statement is skipped with no error you will
notice in a long batch.

Detect it in bulk through the API, 50 ids per call:

```
https://www.wikidata.org/w/api.php?action=wbgetentities&format=json
    &props=info&redirects=yes&ids=Q1|Q2|...
```

Each entity in the response carries a `redirects: {from, to}` field when it is a
redirect, and deleted items come back flagged `missing`. Run it over
`carlquist_publications.csv` plus both lookup tables; all 346 + 48 + 72 ids scan in
about 15 seconds.

Seen in v2.2: `Q139119348` had been merged into `Q56211461` (Amborella
trichopoda, Pacific Science 55(3):305-312). The merge target was the better record
— both authors as P50 rather than name strings — so the fix is to repoint the row,
not to recreate anything.

### Search for an existing item before any CREATE

`CONTRIBUTING.md` step 2 is load-bearing and `add_publication.py`'s duplicate check
does **not** satisfy it — that check only scans the CSV, so a paper absent from this
dataset but already on Wikidata passes it and you create a duplicate.

Search three ways, because a title search alone misses items whose title differs in
punctuation or capitalisation:

```
haswbstatement:P356="<doi>"
haswbstatement:P10283="<openalex-id>"
"<exact title>"
```

These go through the search index, not SPARQL, so they are unaffected by the graph
split (below). Caught in v2.2: `Q46126499` already existed for the 2001 *Vessels in
Ferns* paper.

### An existing item's DOI may be wrong

`Q46126499` carried `10.1006/ANBO.2001.1430`, which resolves to Foreman et al.,
*Root Hairs as a Model System for Studying Plant Cell Growth*, **Annals of Botany**
88(1):1-7 — a different paper that shares the volume and issue number with the
*American Journal of Botany* paper. Same-volume/issue collisions between journals
are an easy way for a bot or a hurried edit to attach the wrong identifier, so
verify a DOI found on an item rather than trusting it.

Prefer **deprecating** a wrong external identifier over deleting it: the rank keeps
it out of queries while preserving the record that the claim was made.

### Verify that a batch actually landed

A long QuickStatements batch can partially fail without saying so. The v2.2 P10283
batch reported success but landed 312 of 313 statements. Re-read the items
afterwards and compare values — do not trust the run report.

### API access

- Wikimedia rejects a default HTTP-library user-agent with **403** citing their
  robot policy. Send a descriptive `User-Agent`.
- Rapid successive queries get **429**. Pace batches; a second or two between calls
  is enough for this dataset's size.

### Graph split affects queries, not edits

Since 2025-05-09 the query service is split. An item declaring
`P31 = Q13442814` (*scholarly article*) — which is every publication item this
workflow creates — lives in the **scholarly graph** and must be queried at
`query-scholarly.wikidata.org`, not `query.wikidata.org`; spanning both needs
federation. The saved queries in `wikidata/wikidata_queries.txt` already use the
scholarly endpoint. Editing is unaffected: QuickStatements writes through the API,
and there is no scholarly-specific edit tool.

Consequence worth knowing: SPARQL-backed duplicate detection and constraint checks
can be blind across the split, which is why the pre-create search above uses the
search index instead.

### P10283 (OpenAlex ID)

Datatype `external-id`, format regex `[ACIWTSPFaciwtspf][1-9]\d{3,9}`, formatter URL
`https://openalex.org/$1`. `tools/qs_common.py` emits it when a record carries an
`openalex-id`. Batches generated for existing items are bare statements — add a
P248 reference block first if that is your convention.

---

## OpenAlex

### The 31 blank `openalex-id` values are unresolvable, not unresolved

They have no OpenAlex record at all — confirmed by probe searches, not merely by a
failed match. They are papers in pre-DOI venues (*Tropical Woods*,
*Phytomorphology*, *Allertonia*, *Botaniska Notiser*, *Botanische Jahrbücher*,
*Madroño*, *Memoirs of the New York Botanical Garden*, *University of California
Publications in Botany*, *American Scientist*) plus nine chapters in edited volumes.
Do not spend time re-resolving them; re-check only if OpenAlex backfills those
venues.

### Two OpenAlex records to keep straight

- The 1998 *Microgramma nitida* paper exists twice: use **W1507851166** (Spanish
  title, dated 1998). **W1933495356** is the same paper under an English title and
  misdated 2009.
- **W179140364** carries only the truncated title *"SEM studies of vessels in
  ferns"* but is specifically the *Ceratopteris* paper (Aquatic Botany, 2000,
  `10.1016/s0304-3770(99)00023-6`). Because that string is the common prefix of the
  whole numbered series, it will fuzzy-match other members — never let it attach to
  one.

### Requests need an API key

`api.openalex.org` rejects anonymous calls. Batch DOI lookups with the `doi:` filter,
50 per request.

---

## The CSV

### Close it in LibreOffice before editing programmatically

A `.~lock.carlquist_publications.csv#` file in the repo root means the CSV is open in
a spreadsheet application. Appending to the file on disk underneath it is silently
lost: the next save from that window writes its in-memory copy over your change.
Check for the lock first. Its contents name the user, host and open time, so a stale
lock left by a crash is distinguishable from a live one — and a crash leaves the
file itself untouched.

The lock pattern is gitignored as of v2.2, but the hazard is the overwrite, not the
commit.

### Line endings

The file is LF throughout. `csv.writer` defaults to `\r\n`, which is how the v2.1
row became the only CRLF line in the file; `tools/add_publication.py` now passes
`lineterminator="\n"` explicitly. Check with:

```
python3 -c "print(open('carlquist_publications.csv','rb').read().count(b'\r'))"   # expect 0
```

### Inserting a column is safe

`add_publication.py --write` builds each row from the CSV's own header, not from the
`FIELDS` list, so a column inserted mid-file does not misalign appended rows. Keep
`FIELDS` in sync anyway — it drives the draft preview and the CLI flags.

### `datapackage.json` regex escaping

Field `pattern` constraints are JSON-escaped regex with a single backslash pair in
the file text, e.g. `"^Q\\d+$"`. Generating one from Python with an extra escape
level yields a pattern matching a literal backslash, and `frictionless` then fails
**every populated row** in that column — a loud failure with a misleading cause.

---

## Tooling

- The venv in this repo is **`env/`**, not the `.venv/` that `CONTRIBUTING.md` names.
  `frictionless` lives there: `env/bin/frictionless validate datapackage.json`.
- Run the tools from inside `tools/` so `qs_common` imports. If the interpreter has
  `PYTHONSAFEPATH=1` set (some sandboxed environments do), the script's own
  directory is not added to `sys.path` and you need `PYTHONPATH=. python3
  add_publication.py …`.
- `tools/bump_version.py`'s `FILES` dict covers `CITATION.cff`, `README.md`,
  `DATA_DICTIONARY.md`, `dataset_metadata.json`, `.zenodo.json` and
  `datapackage.json`. It does **not** touch `CLAUDE.md`, `DATASET_PROFILE.md` or this
  file, so their version and count lines drift unless updated by hand. `CLAUDE.md`
  was two releases stale when v2.2 was prepared.

---

## Provenance of the data itself

Useful when a value looks wrong and you are deciding which source to trust.

- **Carlquist's own bibliography is unreliable on pagination and volumes.** It prints
  impossible descending page ranges (four were corrected in v2.2: Aliso 12,
  *American Fern Journal* 90, *International Journal of Plant Sciences* 161, *Botany*
  90) and at least one wrong volume. Where it disagrees with Crossref on pagination
  or volume, Crossref wins. It is authoritative on *what he considered his work* —
  it deliberately omits shorter articles, popular articles, reviews and abstracts.
  The source page is gone; it survives only as an Internet Archive snapshot of
  `sherwincarlquist.com/biography-publications.html`.
- **JSTOR-era records list the reviewed author alongside the reviewer**, so reviews
  *of* Carlquist's books are widely misattributed *to* him in aggregators. The test
  is whether the title matches one of his books and he is not the first author.
- **Two 1966 *Aliso* papers are dated 1996 in OpenAlex.** Publication years follow
  his own list where the sources disagree.
- **Dual-registered DOIs are normal, not duplicates.** Botanical Journal of the
  Linnean Society and IJPS articles carry a legacy Academic Press DOI
  (`10.1006/bojl.*`, 4 rows here) alongside a Wiley one
  (`10.1111/j.1095-8339.*`, 21 rows here). Both resolve. Only one is stored; a merge
  with another dataset should expect either.
- **`carlquist_authors.csv` has 72 rows and one of them is Carlquist himself** — so
  72 author records, 71 co-authors, 42 carrying a QID. The "73 co-authors" figure
  repeated from v2.0 through v2.1 was wrong.
