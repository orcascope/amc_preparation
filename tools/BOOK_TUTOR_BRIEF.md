# Book tutor brief: turn an ACE book problem into a guided lesson

You convert one Problem or Example from *ACE The AMC 10 and AMC 12* (Ritvik
Rustagi) into the same step-by-step lesson format the app uses for contest
problems. The book already has a worked solution for every item: your lesson
follows the book's method, rewritten as a guided lesson in your own words.

First read `tools/TUTOR_BRIEF.md`. Every rule there about **steps** applies here
unchanged: 3 to 5 steps, step 1 titled "Where to start: …" with the reason,
no spoilers before the last step, `your_turn` on every step but the last,
tone, KaTeX math with doubled backslashes in JSON, body length. This brief only
covers what is different for the book.

## Inputs you will be given
- The cropped statement image: `amc_questions/ace-amc-book/<topic>/images/<ID>.png`
- Rendered book pages that hold the item and its solution (PNG). Read the math
  from these images, not from any text extraction: the PDF's text layer loses
  exponents (2^3 comes out as "23").

## Output: two files per item
`<ID>` is `ACE_<chapter>_<section>_<nn>` (Problem 2.2.7 is `ACE_2_2_07`).

### 1. `amc_questions/ace-amc-book/<topic>/statements/items/<ID>.json`
```json
{
  "id": "ACE_2_2_07",
  "number": "2.2.7",
  "kind": "problem",
  "section": "Multiples, Divisors, Prime Factorization",
  "original_source": "2022 AMC",
  "topic": "number_theory",
  "subtopic": "LCM and GCD",
  "text": "The least common multiple of a positive integer $n$ and $18$ is $180$, …",
  "choices": { "A": "$3$", "B": "$6$", "C": "$8$", "D": "$9$", "E": "$12$" },
  "figure": "Only if the item has a diagram: a plain-English description of it.",
  "book_answer": "B",
  "book_pages": [13]
}
```
- `text`: the statement exactly as printed, in LaTeX (`$…$`). Leave out the
  "Problem 2.2.7 —" label and the "Source:" line. Numbers go in math mode as in
  the contest files (`$18$`).
- `choices`: the five choices if the book prints them, otherwise `null`.
- `original_source`: the "Source:" line (e.g. "2019 AIME"), or `null` if none
  (Examples usually have none).
- `book_answer`: the book's final answer: the letter for a multiple-choice item,
  otherwise the value as plain text (e.g. `"585"`, `"3/4"`, `"5^{38}"`).
- `subtopic`: a short name for the idea, in the style of the contest files
  ("LCM and GCD", "Number of divisors", "Legendre's formula", "Base conversion").

### 2. `amc_questions/ace-amc-book/<topic>/worked/<ID>.json`
The same shape as a contest lesson (see `TUTOR_BRIEF.md`), with these changes:
```json
{
  "id": "ACE_2_2_07",
  "source": { "book": "ACE The AMC 10 and AMC 12", "number": "2.2.7", "kind": "problem",
              "section": "Multiples, Divisors, Prime Factorization", "original_source": "2022 AMC" },
  "topic": "number_theory",
  "subtopic": "LCM and GCD",
  "difficulty": 2,
  "problem": { "image": "images/ACE_2_2_07.png", "text": "<same as statements>", "choices": { … } or null },
  "answer": { "choice": "B", "value": "$6$" },
  "steps": [ … ],
  "wrong_choices": { … },
  "verification": {
    "book_answer": "B",
    "matches_book": true,
    "verifier_verdict": "pending",
    "confidence": "high",
    "reviewed_by_teacher": false,
    "generated_with": "ACE book solution",
    "generated_at": "<today>"
  }
}
```
- **Open-ended items** (`choices` is `null`): `answer` is
  `{ "choice": null, "value": "$585$", "accept": ["585"] }`. `accept` lists the
  answers the app should mark correct, as plain text. The app already treats
  `3/4`, `0.75` and `\frac{3}{4}` as equal, and ignores spaces, `$` and
  thousands commas, so list only genuinely different forms (for example
  `["5^{38}", "38"]` when the question asks for "the greatest power of 5" and a
  student may reasonably type just the exponent). The book's answer must be one
  of them. Open-ended items have no `wrong_choices` (leave the key out).
- **Multiple-choice items**: `answer` and `wrong_choices` exactly as in
  `TUTOR_BRIEF.md`. Only include a wrong choice when the book's solution, or
  your own careful check, shows a specific common mistake that produces exactly
  that value. An empty `{}` is fine.
- **difficulty**: 1 for an Example; 2 for a Problem from an AMC contest (or with
  no source); 3 for a Problem from the AIME or any other contest (HMMT, PUMaC,
  SMT, CMIMC, CHMMC, BMT, Purple Comet, …).
- **Examples** are short warm-ups. Three steps is usually right.
- Follow the book's method. If the book's solution skips a step, fill it in.
  If a step of the book's solution, or its final answer, looks wrong to you, do
  not silently change it: report it in your final message and say what you
  believe is correct.
- The app's markdown supports only paragraphs and `**bold**` (no italics, no lists).

Validate every file you write with
`python3 -c "import json,sys; json.load(open(sys.argv[1], encoding='utf-8'))" <file>`.
Use Bash only for that check. Do not use the web.
