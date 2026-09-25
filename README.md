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
  TUTOR_BRIEF.md       instructions for writing a worked-solution JSON file
  VERIFIER_BRIEF.md    instructions for adversarially checking one
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

## Status

| Year/contest | Worked lessons |
|---|---|
| 2022 10A | ✅ 25 of 25 |
| 2018 10A | ✅ 25 of 25 |
| 2018 10B | ✅ 25 of 25 |
| 2019 10A, 2019 10B, 2021 10A Spring, 2021 10A Fall | PDFs downloaded, not yet worked |
