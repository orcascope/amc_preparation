# Lessons learned: what went wrong before, and how to prevent it

## Holes the verifiers actually found

Put the matching warnings into the tutor prompt so the first draft avoids them.

| Hole | Example | Prevention |
|---|---|---|
| A `your_turn` answer gives away the final answer | 2.5.2: step 2 asked "smallest valid base?" and answered "b = 4", which was the answer | Ask for the *condition* ("b > 3"), and let the last step name the value |
| "Largest/smallest" ruled out only the next case | 2.4.6: showed n = 720 fails but never n > 720 | Say why every case beyond the bound fails |
| A case dismissed without a reason | 2.2.10: "a fractional ratio is just the sequence backwards", with no proof | Either prove the dismissal in a sentence or check the cases explicitly |
| The method finds *a* solution but doesn't show it is the only one | 2.2.11: another factor pair also fits the first equation | Use every given condition before picking a candidate, and say that other candidates fail |
| Step 1's "why" doesn't match the problem | "the question is about size", when it asks about cubes | Step 1 names the clue that is really in the statement |
| A made-up `wrong_choices` story | A trap whose value is close to a choice but not equal | Contest: only traps from the verified notes. Book: only when the value matches exactly |
| A spoiler in the answer to an intermediate step | A list of all terms of a sequence given two steps early | Give only what the next step needs |

A fix can create a new hole. That is why every fix gets a **new** verifier.
The 2.2.10 fix needed two rounds: the first fix left the case check
unproven and listed a spoiler.

## Source and tooling traps

- **Exponents vanish from the PDF text layer.** Transcribe from the page
  image and have the verifier compare exponents with the crop.
- **The book's page numbers are off by one** from the PDF's. Record PDF page
  numbers (`book_pages`) and name rendered pages after them.
- **Book solutions have typos** (e.g. "1/19" for "1/10", "a = 4" for "a = 5",
  swapped variables, a wrong sum that still reaches the right answer).
  Tutors fix the working in the lesson and report the error. Never copy a
  wrong line.
- **A mislabelled source line** (e.g. "Solution: 1995 AIME"): record the true
  source in `original_source`.
- **Typos in statements** (e.g. "|a4a2|"): transcribe the intended meaning
  when the book's solution makes it clear. Tell the verifier which reading
  was used and why.
- **Crop edge cases**: an Example's solution sits inside the same box as its
  statement (end the crop at the "Solution:" word), and a box can break
  across a page (stitch the parts). A tall formula on the "Solution:" line
  can leave a thin sliver in the crop, which is acceptable.
- **The instructions page of an AMC booklet also has a numbered list.** The
  cropper keeps only the run of numbers that reaches 25.
- **Scanned solutions PDFs have no text**: type the key by hand from the
  rendered pages and check it twice.

## App and database

- The importer rebuilds the content tables only. Student progress is never
  touched, so re-importing is always safe.
- `import_worked.py --check` needs no database. A full import needs
  `DATABASE_URL` (PostgreSQL) in `.env`.
- Book rows sort by a zero-padded section (`02.10` after `02.09`), and the
  app lists each topic easiest first (difficulty, then source order).
- Playwright: a hash-only navigation doesn't re-render the page. After
  `goto(url#/…)`, call `reload()` before reading the page, or you may read
  the previous page's content.
- Kill the test server by its PID. `pkill -f "python3 server.py"` also
  matched the shell running it and killed the session's command.
