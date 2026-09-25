"""Load every worked-solution JSON into the app database.

Contest years live in amc_questions/<year>/ and the ACE book in
amc_questions/ace-amc-book/<topic>/; both have worked/ and answer_key.json.

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
from answers import matches  # noqa: E402
from db import QUESTIONS_DIR, connect  # noqa: E402

BOOK_DIR = "ace-amc-book"

TOPICS = {"algebra", "geometry", "number_theory", "counting_probability", "arithmetic_logic"}
LETTERS = ["A", "B", "C", "D", "E"]


def official_answer(p, key):
    """The answer key entry for this problem: a letter, or for open-ended book problems the value."""
    if "book" in p["source"]:
        return key.get(p["id"])
    test_id = p["id"].rsplit("_P", 1)[0]
    return key.get(test_id, {}).get(str(p["source"]["number"]))


def load_and_check(worked_file, key):
    """Return (problem, errors); errors is empty when the file follows the rules."""
    p = json.loads(worked_file.read_text(encoding="utf-8"))
    errors = []
    choices = p["problem"].get("choices")
    official = official_answer(p, key)
    if official is None:
        errors.append("no official answer in answer_key.json")
    elif choices:
        if p["answer"]["choice"] != official:
            errors.append(f"answer {p['answer']['choice']} != official {official}")
    elif not matches(official, p["answer"].get("accept") or []):
        errors.append(f"accepted answers {p['answer'].get('accept')} do not include the key {official!r}")
    if p["topic"] not in TOPICS:
        errors.append(f"unknown topic {p['topic']}")
    if choices and sorted(choices) != LETTERS:
        errors.append("choices must be A-E")
    if not choices and p.get("wrong_choices"):
        errors.append("open-ended problems have no wrong_choices")
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
    if choices and p["answer"]["choice"] in p.get("wrong_choices", {}):
        errors.append("wrong_choices lists the correct answer")
    return p, errors


def content_dirs():
    """Folders that hold a worked/ directory and an answer_key.json."""
    for d in sorted(x for x in QUESTIONS_DIR.iterdir() if x.is_dir()):
        if d.name == BOOK_DIR:
            yield from sorted(x for x in d.iterdir() if x.is_dir())
        else:
            yield d


def row_meta(p):
    """(year, contest, session, number, collection, source_label) for the problems table."""
    s = p["source"]
    if "book" in s:
        ch, sec, num = (int(x) for x in s["number"].split("."))
        label = f"ACE book {s['number']}" + (f" · {s['original_source']}" if s.get("original_source") else "")
        # session is only a sort key: zero-padded so section 2.10 sorts after 2.9
        return 0, "book", f"{ch:02d}.{sec:02d}", num, "book", label
    label = f"{s['year']} AMC {s['contest']}" + (f" {s['session']}" if s.get("session") else "")
    return s["year"], s["contest"], s.get("session"), s["number"], str(s["year"]), label


def main(check_only=False):
    conn = None if check_only else connect()
    if conn:
        conn.executescript("DELETE FROM wrong_choices; DELETE FROM steps; DELETE FROM problems;")
    loaded, skipped = 0, 0
    for folder in content_dirs():
        key_file = folder / "answer_key.json"
        key = json.loads(key_file.read_text()) if key_file.exists() else {}
        for f in sorted((folder / "worked").glob("*.json")):
            p, errors = load_and_check(f, key)
            if errors:
                skipped += 1
                print(f"SKIP {f.name}: " + "; ".join(errors))
                continue
            loaded += 1
            if not conn:
                continue
            year, contest, session, number, collection, label = row_meta(p)
            choices = p["problem"].get("choices") or None
            conn.execute(
                "INSERT INTO problems (id, year, contest, session, number, topic, subtopic, difficulty, "
                "image, text, choices_json, answer_choice, answer_value, verification_json, "
                "collection, source_label, accept_json) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                (p["id"], year, contest, session, number, p["topic"], p["subtopic"], p["difficulty"],
                 f"{folder.relative_to(QUESTIONS_DIR).as_posix()}/{p['problem']['image']}",
                 p["problem"]["text"], json.dumps(choices), p["answer"].get("choice") or "",
                 p["answer"]["value"], json.dumps(p["verification"]),
                 collection, label, json.dumps(p["answer"].get("accept") or [])))
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
