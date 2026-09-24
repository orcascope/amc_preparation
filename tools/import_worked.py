"""Load every worked-solution JSON into the app database.

Usage:
    python tools/import_worked.py            # import all years
    python tools/import_worked.py --check    # validate only, write nothing

Content tables (problems, steps, wrong_choices) are rebuilt from scratch.
Student tables are never touched, so re-importing keeps everyone's progress.

A problem is skipped (and reported) when its answer does not match the
official key in amc_questions/<year>/answer_key.json, or when the file breaks
the format rules in tools/TUTOR_BRIEF.md.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "app"))
from db import QUESTIONS_DIR, connect  # noqa: E402

TOPICS = {"algebra", "geometry", "number_theory", "counting_probability", "arithmetic_logic"}
LETTERS = ["A", "B", "C", "D", "E"]


def load_and_check(worked_file, key):
    """Return (problem, errors); errors is empty when the file follows the rules."""
    p = json.loads(worked_file.read_text(encoding="utf-8"))
    errors = []
    src = p["source"]
    test_id = p["id"].rsplit("_P", 1)[0]
    official = key.get(test_id, {}).get(str(src["number"]))
    if official is None:
        errors.append("no official answer in answer_key.json")
    elif p["answer"]["choice"] != official:
        errors.append(f"answer {p['answer']['choice']} != official {official}")
    if p["topic"] not in TOPICS:
        errors.append(f"unknown topic {p['topic']}")
    if sorted(p["problem"]["choices"]) != LETTERS:
        errors.append("choices must be A-E")
    steps = p["steps"]
    if not 3 <= len(steps) <= 5:
        errors.append(f"{len(steps)} steps (want 3-5)")
    if not steps[-1].get("reveals_answer"):
        errors.append("last step must reveal the answer")
    for i, s in enumerate(steps[:-1], 1):
        if s.get("reveals_answer"):
            errors.append(f"step {i} reveals the answer early")
        if not s.get("your_turn"):
            errors.append(f"step {i} has no your_turn")
    if not steps[0]["title"].startswith("Where to start"):
        errors.append("step 1 must start with 'Where to start'")
    if p["answer"]["choice"] in p.get("wrong_choices", {}):
        errors.append("wrong_choices lists the correct answer")
    return p, errors


def main(check_only=False):
    conn = None if check_only else connect()
    if conn:
        conn.executescript("DELETE FROM wrong_choices; DELETE FROM steps; DELETE FROM problems;")
    loaded, skipped = 0, 0
    for year_dir in sorted(d for d in QUESTIONS_DIR.iterdir() if d.is_dir()):
        key_file = year_dir / "answer_key.json"
        key = json.loads(key_file.read_text()) if key_file.exists() else {}
        for f in sorted((year_dir / "worked").glob("*.json")):
            p, errors = load_and_check(f, key)
            if errors:
                skipped += 1
                print(f"SKIP {f.name}: " + "; ".join(errors))
                continue
            loaded += 1
            if not conn:
                continue
            s = p["source"]
            conn.execute(
                "INSERT INTO problems VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                (p["id"], s["year"], s["contest"], s.get("session"), s["number"],
                 p["topic"], p["subtopic"], p["difficulty"],
                 f"{year_dir.name}/{p['problem']['image']}", p["problem"]["text"],
                 json.dumps(p["problem"]["choices"]), p["answer"]["choice"],
                 p["answer"]["value"], json.dumps(p["verification"])))
            for i, st in enumerate(p["steps"], 1):
                yt = st.get("your_turn") or {}
                conn.execute(
                    "INSERT INTO steps VALUES (?,?,?,?,?,?,?)",
                    (p["id"], i, st["title"], st["body"], yt.get("prompt"),
                     yt.get("answer"), int(bool(st.get("reveals_answer")))))
            for letter, text in p.get("wrong_choices", {}).items():
                conn.execute("INSERT INTO wrong_choices VALUES (?,?,?)", (p["id"], letter, text))
    if conn:
        conn.commit()
    print(f"{'checked' if check_only else 'imported'} {loaded} problems, skipped {skipped}")
    return skipped == 0


if __name__ == "__main__":
    sys.exit(0 if main(check_only="--check" in sys.argv) else 1)
