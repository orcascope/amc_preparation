# Mode A: contest (questions PDF + official key)

Prompts that produced the 2018 AMC 10A/10B lessons. Replace `<…>` and keep
everything else word for word: the wording is what makes the agents behave.

`<SCRATCH>` is the session scratchpad directory. `<REPO>` is the repository
root. `<TEST_ID>` looks like `AMC_10B_2018`.

## 1. Statement files for the solvers

For each group of 5 problems, write `<SCRATCH>/<test>/problems_01-05.txt` etc.
Put in only the statements and choices (and the `figure` description if
there is a diagram), and nothing that hints at an answer:

```
The following are AMC 10 (2018) multiple-choice problems. Solve each one independently.

Problem 1: <text in LaTeX>
Choices: (A) $90$   (B) $100$   (C) $180$   (D) $200$   (E) $360$
Figure: <plain-English description, only if the problem has a diagram>
```

## 2. Blind solver (launch 2 per group: A and B)

This is the `math-olympiad` skill's attempt-agent prompt. Two solvers with
different angles make it unlikely that both make the same mistake.

```
NO COMPUTATION. Do not use Bash, Python, WebSearch, Read, Write, or any tool that runs code or fetches data. Numerical verification is not a proof step. "I computed n=1..10 and the pattern holds" is not a proof.

(If your agent harness requires a StructuredOutput or similar return-mechanism tool call, that is NOT a computation tool — call it to return your answer. The restriction is on tools that DO work, not tools that REPORT work.)

Your internal process (iterate until done):
- Solve: Complete rigorous solution.
- Self-improve: Reread. Fix gaps before a grader sees it.
- Self-verify: Strict grader mode. Every step justified?
- Correct: Fix and re-verify. Up to 5 rounds.
- Stop: Self-verify passes twice clean, OR 5 rounds, OR approach fundamentally wrong.

A correct answer from flawed reasoning is a failure. If incomplete, say so honestly. Never hide gaps.

PROBLEM: The problem statements are in one text file. The single exception to the tool rule above: use the Read tool exactly once, on <SCRATCH>/<test>/problems_01-05.txt (it contains only the problem statements and choices). Read nothing else.
ANGLE: <solver A or solver B angle, below>

For EACH problem return exactly:
### Problem N
**Verdict**: complete solution | partial result | no progress
**Rounds**: [how many verify→correct cycles]
**Interpretation**: [any possible misreading, and which reading you solved and why]
**Method**: [key idea, one short paragraph, clear enough for a teacher to turn into a lesson]
**Detailed Solution**: [full step-by-step, every step justified]
**Answer**: [letter and value]
**Traps**: [1–3 specific, common mistakes a strong 8th–10th grader could make. For each, state the exact value it produces and which answer choice it matches, if any. Only list a match if the mistake really gives exactly that value.]
**Alternative method**: [a second route, if one exists]
**Self-verification notes**: [what you caught and fixed; remaining concerns]
```

Angles:
- **Solver A**: `Work each problem directly and carefully, then confirm the result by a second, independent route (substitution back into the conditions, a special case, a small analogous case, or estimation).`
- **Solver B**: `Look for structure first (symmetry, complementary counting, working backwards, invariants, the extremal case); then test your answer against the conditions and against the other answer choices to see why they fail.`

## 3. Reconcile → `statements/<TEST_ID>_verified.md`

For each problem, compare solver A, solver B and the official key.
- All three agree: keep the clearer method.
- Any disagreement: find the cause. Common causes are a misread statement
  (check the crop), a missing figure detail, or a solver error. If still
  unclear, run a third solver on that problem alone. Never write a lesson
  until the method provably reaches the key's answer.
- Keep only traps whose value really equals a listed choice.

Format (the header records how it was verified):
```
# 2018 AMC 10B — verified solution methods

Each problem was solved by 2 independent blind solvers using the
math-olympiad skill (reasoning only, no tools). The official answer key was
the third vote. Every problem was unanimous (3 of 3) unless noted.

## P1 — (A) 90
<method in 2–4 lines>
<one check>
Trap: <mistake> gives <value>, which is (<letter>).
```

## 4. Tutor (one agent per 5 problems)

```
You are writing guided worked-solution lessons for an offline AMC 10 practice app. Repository root: <REPO>

First read these files completely:
1. <REPO>/tools/TUTOR_BRIEF.md — your instructions. Follow every rule exactly.
2. <REPO>/amc_questions/<year>/statements/<TEST_ID>.json — problem text, choices, topic, subtopic, figure descriptions.
3. <REPO>/amc_questions/<year>/statements/<TEST_ID>_verified.md — the verified method and traps.
4. <REPO>/amc_questions/<year>/answer_key.json — official answers (key "<TEST_ID>").
5. Style reference (finished lessons; match their voice and detail): <REPO>/amc_questions/2018/worked/AMC_10A_2018_P06.json and <REPO>/amc_questions/2018/worked/AMC_10A_2018_P12.json

Your problems: <year> AMC <contest> problems <n1>, …, <n5>.

Write one file per problem at <REPO>/amc_questions/<year>/worked/<TEST_ID>_P<nn>.json (nn two digits). Specifics:
- "id": "<TEST_ID>_P01" etc.; "source": {"year": <year>, "contest": "<contest>", "session": <null or "Spring"/"Fall">, "number": N}; "problem.image": "images/<TEST_ID>_P<nn>.png".
- Copy "problem.text", "problem.choices", "topic", "subtopic" EXACTLY from the statements file (never include the "figure" description in text).
- "verification": official_answer and solver_answer = the key letter, matches_official true, verifier_verdict "pending", confidence "high", reviewed_by_teacher false, generated_with "math-olympiad skill", generated_at "<today>".
- The math must match the verified method.
- wrong_choices: use ONLY traps listed in the verified notes (each already states which choice it produces). Do not invent new mistake stories. An empty {} is fine.
- Only the final step may state the final value or letter, and no earlier step or your_turn answer may make it immediate (one trivial operation away).
- Any case split or "the largest/smallest is" claim must rule out every other case explicitly, not just the next one.
- The app's markdown supports only paragraphs and **bold** (no italics, no lists).

Validate each file with: python3 -c "import json,sys; json.load(open(sys.argv[1], encoding='utf-8'))" <file>
Use Bash only for that check. No web. Do not edit any other files.

Final message: list the files written, and report anything in the verified notes that looked wrong to you (or "none").
```

## 5. Verifier (one fresh agent per lesson, and again after every fix)

```
Read <REPO>/tools/VERIFIER_BRIEF.md and follow it exactly. You are the adversarial verifier.

The file to attack: <REPO>/amc_questions/<year>/worked/<TEST_ID>_P<nn>.json
The statements file (for faithfulness check; use the entry with "number": <N>): <REPO>/amc_questions/<year>/statements/<TEST_ID>.json
The cropped original problem: <REPO>/amc_questions/<year>/images/<TEST_ID>_P<nn>.png

Read only these files. Do not run code or use Bash/Python/web. Do not edit anything. Return the exact format the brief specifies.
```

## Difficulty and IDs
- `difficulty`: 1 for problems 1–10, 2 for 11–20, 3 for 21–25.
- A contest with two sittings in one year (e.g. 2021 Spring/Fall) needs the
  session in the TEST_ID and in `source.session`, so IDs stay unique.
