# Mode B: book with worked solutions

This is how the ACE book pilot (Number theory 2.1–2.6, 32 items) was made. The
book already solves every item, so there is no blind solver. The lesson
follows the book's method, and one fresh reviewer per lesson re-derives the
answer and checks the lesson against the book page.

## Plan the batches

1. Read the table of contents from the rendered pages. List each section's
   page range and its number of Problems and Examples.
2. Group sections into batches of about 30 items that fit inside one
   chapter (= one app topic).
3. Show the plan to the user. Ask which sections to skip, whether Examples
   are included, and whether to pilot the first batch.

## Per batch

```
python tools/crop_book.py <book.pdf> <topic> <first_section> <last_section>   # crops + index
python tools/render_pages.py <book.pdf> <SCRATCH>/book/pages <first_page> <last_page>
```
Use the index (id, kind, source, page) to hand each tutor about 5 items,
together with the page range that holds those items and their solutions.
The book's printed page number is usually 1 lower than the PDF page. Always
use the PDF page, which is the page_NNN.png file name.

IDs: `ACE_<chapter>_<section>_<nn>` (Problem 2.2.7 -> `ACE_2_2_07`). For a
different book, pick a new short prefix (see new_layouts.md, "A second book").

## Tutor prompt (one agent per about 5 items)

```
You are converting items from the <BOOK NAME> into guided lessons for an offline practice app. Repository root: <REPO>

Read completely, in this order:
1. <REPO>/tools/TUTOR_BRIEF.md (step rules — they all apply)
2. <REPO>/tools/BOOK_TUTOR_BRIEF.md (what is different for the book; follow it exactly)
3. Style reference (a finished contest lesson): <REPO>/amc_questions/2018/worked/AMC_10A_2018_P07.json

Topic folder: <REPO>/amc_questions/<book-dir>/<topic>  (topic key "<topic>")
Today's date for generated_at: <today>

Your items (ID — book number — kind — section):
- <ID> — <x.y.z> — <problem|example> — <section title>
…

For each item, view its cropped statement image: <REPO>/amc_questions/<book-dir>/<topic>/images/<ID>.png
The book pages holding these items and their solutions are rendered at: <SCRATCH>/book/pages/page_<NNN>.png through page_<MMM>.png (file name = PDF page number; view the ones you need).

Write both output files per item as the book brief describes (statements/items/<ID>.json and worked/<ID>.json), and validate each with the JSON check. Do not edit any other files.

Final message: list the files written with each item's answer, and report anything in the book's solutions that looked wrong (or "none").
```

Keep the tutors' reports of book errors (typos, a wrong intermediate line,
swapped letters) and include them in your final summary to the user. The
lesson uses the corrected working. The final answer must still equal the
book's. If the book's final answer itself looks wrong, stop and ask the user.

## Verifier prompt (one fresh agent per lesson, and again after every fix)

```
You are an adversarial verifier. Read <REPO>/tools/VERIFIER_BRIEF.md and then <REPO>/tools/BOOK_VERIFIER_BRIEF.md and follow both exactly.

Item ID: <ID>. Files (read only these):
- Lesson: <REPO>/amc_questions/<book-dir>/<topic>/worked/<ID>.json
- Statement file: <REPO>/amc_questions/<book-dir>/<topic>/statements/items/<ID>.json
- Cropped original problem: <REPO>/amc_questions/<book-dir>/<topic>/images/<ID>.png
- Book page(s) with the solution: <SCRATCH>/book/pages/page_<NNN>.png (and page_<NNN+1>.png if the solution continues)
<Optional "Note:" line about a known book typo and how the lesson reads it.>

Do not run code or use Bash/Python/web. Do not edit anything. Return the exact format VERIFIER_BRIEF.md specifies.
```

The statement file's `book_pages` lists the pages each item needs.

## After all lessons hold

```
python tools/assemble_book.py <topic>     # statements/ACE_<topic>.json + answer_key.json (merges with earlier batches)
rm -r amc_questions/<book-dir>/<topic>/statements/items
python -m tools.import_worked --check
node tools/check_math.js
```

## Open-ended answers

Book items without choices have `answer: {"choice": null, "value": "$585$",
"accept": ["585"]}`. The app normalizes typed answers (`app/answers.py`):
`3/4`, `0.75` and `\frac{3}{4}` are equal. Spaces, `$` and thousands commas
are ignored. `5^{38}` and `5^38` are equal. So `accept` lists only genuinely
different forms:
- the bare exponent when the question asks for "the greatest power of 5"
  (`["5^{38}", "38"]`)
- a leading-zero AIME form (`["69", "069"]`)
- every ordering and separator for a multi-value answer
  (`["0 and 1890", "0, 1890", "1890 and 0", "0 or 1890"]`)

Test one of these in the browser before you finish.
