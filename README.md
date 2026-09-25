# AMC 10 Practice

A local, offline practice app for the AMC 10. Students pick their own name,
work through real contest problems grouped by type, and can ask for a
step-by-step guided hint or the full solution whenever they get stuck.
Nothing calls a model while a student is using the app — every hint and
solution was written and checked ahead of time.

## Running it

```
python app/run.py
```

This imports the latest worked solutions into the database, starts a local
server, and opens `http://localhost:5000` in your browser. Everyone on this
computer uses the same server and shares one progress database
(`app/data/amc.db`), but each student's progress is kept separate by name.

Stop the server with Ctrl+C. Nothing else needs to run — no internet
connection is required once the page has loaded once, since KaTeX and the
fonts are bundled under `app/static/vendor/`.

## Project layout

```
amc_questions/<year>/
  questions/    official problem PDFs
  solutions/    official solution PDFs
  images/       one cropped PNG per problem (tools/crop_problems.py)
  answer_key.json                       official answer letters
  statements/<TEST_ID>.json             problem text, choices, topic, figure notes
  statements/<TEST_ID>_verified.md      solving method, checked by 2 blind solvers
                                         + the official key
  worked/<TEST_ID>_P<nn>.json           the guided lesson shown in the app

amc_questions/ace-amc-book/<topic>/     practice problems from the ACE book
  images/ACE_<ch>_<sec>_<nn>.png        cropped statement (tools/crop_book.py)
  statements/ACE_<topic>.json           text, choices (or null), source, book answer
  answer_key.json                       the book's answers
  worked/ACE_<ch>_<sec>_<nn>.json       the guided lesson (Problem 2.2.7 -> ACE_2_2_07)

app/
  server.py       Flask API (answers/steps stay server-side until asked for)
  schema.sql       SQLite schema: content tables + student tables
  static/          the whole front end (plain HTML/CSS/JS, no build step)
  data/amc.db      the database (created on first run)

tools/
  crop_problems.py    cut each problem out of a questions PDF into a PNG
  extract_answers.py  read the official answer key from a solutions PDF
  import_worked.py    load worked/*.json into the database (content only —
                       never touches student progress)
  check_math.js       render every formula in every lesson with KaTeX
  crop_book.py        cut each ACE book Problem/Example into a PNG
  assemble_book.py    merge per-item book statements into one file + answer key
  TUTOR_BRIEF.md       instructions for writing a worked-solution JSON file
  VERIFIER_BRIEF.md    instructions for adversarially checking one
  BOOK_TUTOR_BRIEF.md, BOOK_VERIFIER_BRIEF.md   the same, for ACE book items
```

## Adding a new test (year/contest)

1. `python tools/crop_problems.py amc_questions/<year>/questions/<TEST_ID>_Problems.pdf`
2. `python tools/extract_answers.py amc_questions/<year>/solutions/<TEST_ID>_Solutions.pdf`
   (only works on PDFs with a text layer — some official solution PDFs are
   scanned images and need the key entered by hand instead)
3. Write `amc_questions/<year>/statements/<TEST_ID>.json` — one entry per
   problem, with LaTeX text, the 5 choices, a topic/subtopic, and a plain-
   English figure description for any problem with a diagram.
4. Use `/math-olympiad` to solve and verify every problem (2+ independent
   solvers per problem, checked against the official key), and write the
   method notes to `amc_questions/<year>/statements/<TEST_ID>_verified.md`.
5. Follow `tools/TUTOR_BRIEF.md` to turn each verified method into a guided
   lesson at `amc_questions/<year>/worked/<TEST_ID>_P<nn>.json`.
6. Follow `tools/VERIFIER_BRIEF.md` to adversarially check each lesson file
   with a fresh reviewer, and fix anything it finds.
7. `node tools/check_math.js` to confirm every formula renders.
8. `python tools/import_worked.py` to load it into the app.

## Adding an ACE book section

The book (`ace-the-amc-book/references/`) has a worked solution for every
item, so there is no blind-solver step: the lesson follows the book's method,
and a fresh reviewer re-derives the answer and checks it against the book page.
Problems without answer choices are open-ended: the student types an answer,
and the app accepts equivalent forms (`3/4`, `0.75`, `\frac{3}{4}`).

1. `python tools/crop_book.py ace-the-amc-book/references/ACE_The_AMC_10_and_12.pdf <topic> <first_section> <last_section>`
2. Render the book pages as PNGs (the PDF text layer drops exponents).
3. Follow `tools/BOOK_TUTOR_BRIEF.md` for each item: it writes
   `statements/items/<ID>.json` and `worked/<ID>.json`.
4. Follow `tools/BOOK_VERIFIER_BRIEF.md` with a fresh reviewer per lesson; fix
   anything it finds and re-check.
5. `python tools/assemble_book.py <topic>` to build `statements/ACE_<topic>.json`
   and `answer_key.json`.
6. `node tools/check_math.js`, then `python tools/import_worked.py`.

In the app, book problems appear under the **ACE book** filter on the topics page.

## Status

| Year/contest | Worked lessons |
|---|---|
| 2022 10A | ✅ 25 of 25 |
| 2018 10A | ✅ 25 of 25 |
| 2018 10B | ✅ 25 of 25 |
| ACE book: Number theory 2.1–2.6 | ✅ 32 of 32 (27 problems + 5 examples) |
| ACE book: rest of Number theory, Algebra, Combinatorics, Geometry | not yet worked (chapter 6 and 3.4 Logarithms skipped: AMC 12 only) |
| 2019 10A, 2019 10B, 2021 10A Spring, 2021 10A Fall | PDFs downloaded, not yet worked |
