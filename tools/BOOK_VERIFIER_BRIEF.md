# Book verifier brief: attack one ACE book lesson

Read `tools/VERIFIER_BRIEF.md` first: its rules, what to attack and the return
format all apply. This file lists what is different for lessons made from
*ACE The AMC 10 and AMC 12*.

There is no separate blind solver for book items, so you are the only
independent check. Treat the answer as unverified until you have re-derived it.

## Extra inputs
- The cropped statement image `images/<ID>.png`: the original problem.
- The rendered book page(s) holding the book's solution.

## Extra things to attack
1. **Faithfulness to the book page.** `problem.text` (and `choices`) must say the
   same thing as the cropped image: every number, exponent, condition and
   word that changes the meaning. The text layer of this PDF drops exponents,
   so check them against the image with particular care.
2. **Answer.** Re-derive it yourself. It must equal the book's final answer
   (`verification.book_answer`). If you believe the book itself is wrong, say
   so as a HOLE with your reasoning.
3. **Open-ended `accept` list** (when `choices` is null): it must contain the
   correct answer, and nothing in it may be wrong or accept a different value.
   Point out a common, clearly correct form that is missing (for example the
   bare exponent when the question asks for a power).
4. **Statement file.** The matching `statements/items/<ID>.json` must agree
   with the lesson (text, choices, topic, subtopic, book_answer).
