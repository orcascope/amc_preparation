# New layouts and new sources

## A PDF the existing croppers don't handle

The croppers are written for two layouts: the AMC booklet
(`tools/crop_problems.py`) and the ACE book's framed boxes
(`tools/crop_book.py`). For anything else, write `tools/crop_<source>.py`
with the same contract:

- **Output**: one PNG per item in `amc_questions/<dir>/images/`, named by the
  item's ID, rendered at `ZOOM = 2.5` and cropped to the statement only
  (no item number, no solution, no running header or footer).
- **Print**: a JSON index `[{id, kind, number, source, page, image}]`, so tutors
  can be given their pages.

How to find the items (PyMuPDF, `import pymupdf as fitz`):
1. `page.get_text("dict")` gives lines with bounding boxes. Find the label
   pattern ("1.", "Problem 3", "Exercise 4.2") and require it at the left
   margin (`x0` below a threshold), so references inside the text don't match.
2. An item ends where the next label starts, at a drawn frame's bottom
   (`page.get_drawings()`), at a "Solution" heading (`page.search_for`), or at
   the footer.
3. For an item that runs across a page, stack the pieces with
   `show_pdf_page` on a blank page (see `render()` in `crop_book.py`).
4. Measure the page frame (header and footer y-coordinates) from real pages
   instead of guessing.

Run it on the whole batch and **view every PNG**. Also run it on an earlier
source to prove nothing changed there. When `crop_problems.py` was changed
for 2018, the 2022 images stayed byte-identical.

A scanned PDF (no text layer): render the pages and find the item boundaries
by eye (or by the whitespace gaps between rows). Write the crop rectangles to a
small JSON file and crop from that, so the step can be repeated.

## A new contest year or contest

This needs no code changes. Put the PDFs in `amc_questions/<year>/questions/`
and `amc_questions/<year>/solutions/`, then run Mode A. Each contest year
(`source.year` in the lessons) becomes a filter chip in the app automatically.

## A second book

Book support is currently written for one book. For another book:
1. Folder: `amc_questions/<book-dir>/<topic>/` with the same subfolders.
2. `app/import_worked.py` (the importer; `tools/import_worked.py` only forwards
   to it): `BOOK_DIR` names the one book folder, and
   `content_dirs()` treats **every other folder as a contest year**, so a second
   book folder breaks the import until this is changed. Turn `BOOK_DIR`
   into a list (or detect book folders, e.g. by a `book.json` marker), and in `row_meta()` give each book
   its own `collection` key and label (currently `"book"` and
   `"ACE book …"`).
3. `app/server.py` `collections()`: label the new collection key for the
   filter chips (currently only `"book"` is labelled as "ACE book").
4. `tools/assemble_book.py`: the book title is written into the
   assembled file.
5. The solution footer in `app/static/app.js` treats IDs starting with `ACE_`
   as book items. Extend that check to the new prefix.
6. `answer_key.json` for a book maps `{ID: answer}` (flat), unlike a
   contest's `{TEST_ID: {number: letter}}`. Keep that shape.

Run `python -m tools.import_worked --check`, then look at the new chip in the app.
