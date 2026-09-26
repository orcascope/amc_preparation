---
name: make-guided-lessons
description:
  "Turn a math problem source into guided step-by-step lessons for this repo's
  AMC practice app: produces images/, statements/, worked/ and answer_key.json
  under amc_questions/. Works for a contest (a questions PDF plus a solutions
  PDF or answer key, e.g. AMC 10A 2019) and for a math book whose problems come
  with worked solutions (e.g. the ACE book). Use when asked to 'add the 2019
  AMC 10B', 'convert this contest/PDF into lessons', 'do the worked solutions
  for <year>', 'add the book problems for <chapter/section>', 'continue the
  next batch of the book', or to make the app's step-by-step format for any
  new question/solution PDF or math book."
version: 1.0.0
---

# Make guided lessons from a problem PDF or a math book

The app teaches with **worked lessons**: 3 to 5 small steps, a "Your turn"
question on each, and the answer only in the last step. This skill turns a
source PDF into the four things the app needs, checks every lesson with a
fresh adversarial reviewer, and loads the result.

```
amc_questions/<source>/
  images/          one cropped PNG per problem (the original statement)
  statements/      problem text, choices, topic, subtopic (+ verified notes)
  worked/          one lesson JSON per problem  <- what the app shows
  answer_key.json  the official (or book) answers the importer checks against
```

The rules for a lesson live in the repo and are the single source of truth.
Read them before starting and point every subagent at them:

| File | What it is |
|---|---|
| `tools/TUTOR_BRIEF.md` | lesson JSON shape and the step rules |
| `tools/VERIFIER_BRIEF.md` | what the adversarial reviewer attacks, and its return format |
| `tools/BOOK_TUTOR_BRIEF.md`, `tools/BOOK_VERIFIER_BRIEF.md` | the differences for book items (open-ended answers, `accept` lists) |

## Step 0: pick the mode and agree the scope

| Source | Mode | Where the answer comes from |
|---|---|---|
| Contest: questions PDF + solutions PDF (or a printed key) | **A. Contest** | official key; the method comes from 2 blind `math-olympiad` solvers |
| Book or handout whose items have worked solutions | **B. Book** | the book's own solution; one reviewer re-derives it |

Before any work, confirm with the user (use AskUserQuestion when unclear):
- **Which items**: which tests, or which chapters/sections. For a book, read
  the table of contents and propose batches of about 30 items of similar
  size. Flag content outside the app's level (e.g. AMC 12-only topics) and
  ask whether to skip it.
- **Pilot first** for anything new: do one batch end to end, commit, and
  stop for the user to review in the app before continuing.
- For a book: include worked Examples as well as Problems? Keep items that
  duplicate contest problems the app already has?

Topic keys are fixed by the importer: `algebra`, `geometry`, `number_theory`,
`counting_probability`, `arithmetic_logic`. Map the source's chapters onto
these (e.g. Combinatorics -> `counting_probability`).

## Step 1: crop the statements (images/)

- AMC-style booklet (numbered 1..25):
  `python tools/crop_problems.py amc_questions/<year>/questions/<TEST_ID>_Problems.pdf`
- ACE-style book (framed "Problem X.Y.Z" / "Example X.Y.Z" boxes):
  `python tools/crop_book.py <book.pdf> <topic> <first_section> <last_section>`
  It also prints an index (id, kind, source line, page) for the batch.
- Any other layout: write a new cropper, `tools/crop_<source>.py`, with the
  same output contract. See `references/new_layouts.md`.

**Open every crop and look at it.** Check that nothing is cut off at the top
or bottom, that it doesn't include the next problem or the solution, and that
boxes split across pages were stitched together. Fix the cropper, not
individual images.

Render the pages the agents will need to read:
`python tools/render_pages.py <pdf> <scratchpad>/pages [first] [last]`.
PDF text layers often drop exponents (2^3 becomes "23"), so statements are
always checked against images, never against extracted text alone.

## Step 2: answer key

- Contest: `python tools/extract_answers.py amc_questions/<year>/solutions/<TEST_ID>_Solutions.pdf`
  writes `{"<TEST_ID>": {"1": "B", ...}}`. A scanned solutions PDF has no text
  layer: type the key from the rendered pages and double-check every entry.
- Book: produced in Step 5 by `tools/assemble_book.py` from each item's
  `book_answer`.

## Step 3: statements

- **Contest**: write `amc_questions/<year>/statements/<TEST_ID>.json` yourself
  from the page images: `{"test_id", "source": {year, contest, session},
  "problems": [{number, topic, subtopic, text, choices, figure?}]}`. Text and
  choices go in LaTeX (`$…$`). A `figure` is a plain-English description of any
  diagram, used by solvers, never shown in the lesson text.
- **Book**: the tutor agents write `statements/items/<ID>.json` per item (see
  `tools/BOOK_TUTOR_BRIEF.md`). Items with no choices are open-ended:
  `choices: null`.

## Step 4: lessons, then adversarial review

Run agents in parallel, in the background, in batches. The exact prompts
are in `references/contest_pipeline.md` and `references/book_pipeline.md`.
Copy them and fill in the paths.

**Mode A (contest)**
1. **Blind solvers**: 2 independent `math-olympiad` solvers per group of 5
   problems (solver A and solver B, with different angles). They get only a
   text file of the statements: no key, no solutions, no tools.
2. **Reconcile** against the official key. If both solvers agree with the
   key, keep that method. If they disagree, or a solver disagrees with the
   key, run a third solver on that problem and work out why before
   continuing. Write `statements/<TEST_ID>_verified.md`: per problem, the
   answer, the method, one check, and **traps with the exact choice each one
   produces** (these become `wrong_choices`).
3. **Tutors**: one agent per 5 problems writes `worked/<TEST_ID>_P<nn>.json`
   from the statements, the verified notes and the key.
4. **Verifiers**: one fresh verifier per lesson (`tools/VERIFIER_BRIEF.md`).

**Mode B (book)**
1. **Tutors**: one agent per about 5 items. Each gets the crops and the
   rendered pages that hold the items and their solutions, and writes
   `statements/items/<ID>.json` + `worked/<ID>.json`. Tutors must report book
   typos or wrong steps and must not silently copy them.
2. **Verifiers**: one fresh verifier per lesson (`VERIFIER_BRIEF.md` then
   `BOOK_VERIFIER_BRIEF.md`). There is no blind solver in this mode, so the
   verifier is the only independent check and must re-derive the answer.

**Fix loop (both modes)**: for every HOLE FOUND, apply the fix yourself.
Check the math of the suggested fix before applying it; for anything
countable, a quick brute-force script in the scratchpad is fine. Then run a
**new** verifier on the fixed file. Repeat until it HOLDS. Never mark a
lesson as passing because it is "close enough". When it holds, set
`verification.verifier_verdict` to `"pass"` and add a one-line
`verifier_notes` saying what was fixed, if anything.

Common holes and how to prevent them: `references/lessons_learned.md`.
Put the relevant warnings in the tutor prompt up front.

## Step 5: assemble, check, load

Run everything from the repository root. `app` and `tools` are packages, so
scripts that import the app use `python -m` (the cropping and assembling
scripts can still be run directly). The importer's code is in
`app/import_worked.py`, because the Databricks app runs it at startup and
`tools/` is not deployed. `tools.import_worked` only forwards to it. Change the
importer only in `app/`.

```
python tools/assemble_book.py <topic>        # book only: statements/ACE_<topic>.json + answer_key.json
python -m tools.import_worked --check        # format + answer-key check, needs no database
node tools/check_math.js                     # every formula renders in KaTeX
python -m tools.import_worked                # load into PostgreSQL (DATABASE_URL in .env)
```
`--check` must report `skipped 0`. After assembling a book batch, delete
`statements/items/`, because the assembled file is now the source.

Then look at it in the app: start it with `python -m app.run` and use Playwright (Chromium is at
`/opt/pw-browsers`) to:
- open a new problem with its collection filter
- submit a wrong answer, then the right one (for open-ended items, try an
  equivalent form such as `0.75` for `3/4`)
- open the guide and the full solution

Look at the screenshots. Delete the test student afterwards.

## Step 6: finish

- A new source (a new year, or a new book) needs its collection to appear
  in the app. Years work automatically. A second book needs small code
  changes: see `references/new_layouts.md` ("A second book").
- Update the Status table in `README.md` only if the user wants it.
- Commit on the working branch with a message that lists the items, the
  holes that were fixed, and any source errors found. Push. Open or merge a
  PR only when asked.
- Report back briefly: what was added, which lessons needed fixes, and any
  mistakes found in the source. For a pilot, stop there and wait for
  the user's review.

## Non-negotiables

- The answer in every lesson matches the official key (contest) or the
  book's final answer (book). If you believe the source itself is wrong,
  stop and tell the user. Never change an answer quietly.
- Nothing before the last step gives away the final answer.
- Every lesson gets its own fresh verifier, and every fix gets a new one.
- Statements are checked against the images, not the PDF text layer.
