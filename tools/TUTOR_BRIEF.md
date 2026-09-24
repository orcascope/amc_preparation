# Tutor brief: writing a worked-solution JSON file

You turn a verified solution into a guided, step-by-step lesson for a student
preparing for the AMC 10 (usually ages 13–16). The app shows the steps one at a
time. The student can stop after any step and finish the problem alone, so
every step must teach something and must not give away more than it needs to.

## Inputs you will be given
- The problem statement, choices, topic and subtopic, and any figure
  description: `amc_questions/<year>/statements/<TEST_ID>.json`
- The verified method and answer (checked against the official key):
  `amc_questions/<year>/statements/<TEST_ID>_verified.md`
- The official answer letter: `amc_questions/<year>/answer_key.json`

## Output
One file per problem: `amc_questions/<year>/worked/<TEST_ID>_P<nn>.json`
(`nn` is two digits). It must be valid JSON. Check every file with
`python -c "import json,sys; json.load(open(sys.argv[1], encoding='utf-8'))" <file>`.
Use Bash only for that check. Do not look anything up on the web.

```json
{
  "id": "AMC_10A_2022_P07",
  "source": { "year": 2022, "contest": "10A", "session": null, "number": 7 },
  "topic": "number_theory",
  "subtopic": "LCM and GCD",
  "difficulty": 1,
  "problem": {
    "image": "images/AMC_10A_2022_P07.png",
    "text": "<copy EXACTLY from the statements file>",
    "choices": { "A": "...", "B": "...", "C": "...", "D": "...", "E": "..." }
  },
  "answer": { "choice": "B", "value": "$6$" },
  "steps": [
    {
      "title": "Where to start: ...",
      "body": "...",
      "your_turn": { "prompt": "...", "answer": "..." }
    },
    { "title": "...", "body": "...", "your_turn": { "prompt": "...", "answer": "..." } },
    { "title": "Put it together", "body": "... The answer is **(B)**.", "reveals_answer": true }
  ],
  "wrong_choices": {
    "C": "Short, kind explanation of the likely mistake that leads to (C)."
  },
  "verification": {
    "official_answer": "B",
    "solver_answer": "B",
    "matches_official": true,
    "verifier_verdict": "pending",
    "confidence": "high",
    "reviewed_by_teacher": false,
    "generated_with": "math-olympiad skill",
    "generated_at": "2026-09-24"
  }
}
```

Field rules:
- `difficulty`: 1 for problems 1–10, 2 for 11–20, 3 for 21–25.
- `problem.text`, `problem.choices`, `topic`, `subtopic`: copy them exactly from
  the statements file. Do not include the figure description in `text`; the app
  shows the original image.
- `answer.value`: the value of the correct choice, written as LaTeX in `$…$`.
- `verification.verifier_verdict` stays `"pending"`. A separate verifier sets it.

## How to write the steps

1. **3 to 5 steps.** Each step has one idea. Steps get more specific as they go.
2. **Step 1 always starts with "Where to start:"**. It names the key observation or
   strategy and explains *why* a student would think of it: what in the problem
   is the clue. It does not do the whole computation.
3. **No spoilers before the last step.** Only the final step may state the final
   value or the answer letter, and only the final step has
   `"reveals_answer": true`. Earlier steps may state intermediate results, but
   none from which the final answer can be read off directly.
4. **Every step except the last has `your_turn`.** It is a short question the
   student can answer in their head or on paper in under two minutes, and it
   moves them toward the next step. `answer` is the short correct response,
   with a few words of reason.
5. **Tone:** clear, encouraging, and plain. Write for a strong 8th–10th grader.
   Keep sentences short and do not use jargon unless you explain it
   ("Vieta's formulas say…"). Use no emoji. Do not say "simply" or "obviously".
6. **Name the trap.** If the verified notes mention a common trap, warn about it
   inside the relevant step ("Careful: …").
7. **Math formatting:** Markdown plus KaTeX LaTeX in `$…$` (inline) or `$$…$$`
   (display). Only use commands KaTeX supports. In JSON every backslash must be
   doubled (`\\frac`, `\\sqrt`). Use `**bold**` sparingly.
8. **`body` length:** 1–4 sentences plus at most one display equation.
9. The math must match the verified method exactly. If you find anything in the
   verified notes that looks wrong, do not guess. Report it in your final
   message.

## wrong_choices
Include 1–3 wrong letters that a student could plausibly reach by a specific,
common mistake (the traps in the verified notes are the best source). Each
entry is 1–2 sentences: say what mistake leads there and how to spot it. Never
invent a mistake that does not really produce that value. If you are not sure
a wrong choice comes from a real mistake, leave it out.
