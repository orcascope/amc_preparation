"""Load worked-solution JSON files into the app database.

Content lives under amc_questions/: contest years directly
(amc_questions/<year>/), and the ACE book under
amc_questions/ace-amc-book/<topic>/; both have a worked/ directory and an
answer_key.json.

This is a manual, backend-only step — nothing calls it automatically anymore.
Run it yourself whenever you add a paper or change worked solutions, naming
the folder(s) that changed:

    python -m app.content_loader 2019                     # just that year
    python -m app.content_loader ace-amc-book/geometry     # just that book topic
    python -m app.content_loader 2018 2022                 # several folders
    python -m app.content_loader --all                      # every folder (first-time load)
    python -m app.content_loader 2019 --check               # validate only, write nothing

(python -m tools.content_loader does the same; tools/ is not deployed with the
Databricks app, so the real code lives here in app/.)

Problems are upserted by id: existing rows are updated in place, new ones are
inserted, and folders you don't name are left untouched — nothing is deleted
first. Student tables (students, attempts, progress) are never touched.

A problem is skipped (and reported, its existing DB row left as-is) when its
answer does not match the official key in amc_questions/<folder>/answer_key.json,
or when the file breaks the format rules in tools/TUTOR_BRIEF.md.
"""
import argparse
import json
import sys

from app.answers import matches  # noqa: E402
from app.db import QUESTIONS_DIR, connect  # noqa: E402

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


def all_content_dirs():
    """Every folder that holds a worked/ directory and an answer_key.json."""
    for d in sorted(x for x in QUESTIONS_DIR.iterdir() if x.is_dir()):
        if d.name == BOOK_DIR:
            yield from sorted(x for x in d.iterdir() if x.is_dir())
        else:
            yield d


def content_dirs(folders=None):
    """Folders to load: everything under amc_questions/, or just the ones named
    (paths relative to amc_questions/, e.g. "2019" or "ace-amc-book/geometry")."""
    if not folders:
        yield from all_content_dirs()
        return
    for name in folders:
        d = QUESTIONS_DIR / name
        if not (d / "worked").is_dir():
            raise SystemExit(f"{d} has no worked/ directory — check the folder name")
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


def upsert_problem(conn, folder, p):
    """Insert or update one problem's row, and rebuild its steps and wrong_choices."""
    year, contest, session, number, collection, label = row_meta(p)
    choices = p["problem"].get("choices") or None
    conn.execute(
        "INSERT INTO problems (id, year, contest, session, number, topic, subtopic, difficulty, "
        "image, text, choices_json, answer_choice, answer_value, verification_json, "
        "collection, source_label, accept_json) VALUES (" + ", ".join(["%s"] * 17) + ") "
        "ON CONFLICT (id) DO UPDATE SET "
        "year = EXCLUDED.year, contest = EXCLUDED.contest, session = EXCLUDED.session, "
        "number = EXCLUDED.number, topic = EXCLUDED.topic, subtopic = EXCLUDED.subtopic, "
        "difficulty = EXCLUDED.difficulty, image = EXCLUDED.image, text = EXCLUDED.text, "
        "choices_json = EXCLUDED.choices_json, answer_choice = EXCLUDED.answer_choice, "
        "answer_value = EXCLUDED.answer_value, verification_json = EXCLUDED.verification_json, "
        "collection = EXCLUDED.collection, source_label = EXCLUDED.source_label, "
        "accept_json = EXCLUDED.accept_json",
        (p["id"], year, contest, session, number, p["topic"], p["subtopic"], p["difficulty"],
         f"{folder.relative_to(QUESTIONS_DIR).as_posix()}/{p['problem']['image']}",
         p["problem"]["text"], json.dumps(choices), p["answer"].get("choice") or "",
         p["answer"]["value"], json.dumps(p["verification"]),
         collection, label, json.dumps(p["answer"].get("accept") or [])))
    # steps/wrong_choices have no natural id of their own — rebuild them for this
    # one problem rather than trying to diff row by row.
    conn.execute("DELETE FROM steps WHERE problem_id = %s", (p["id"],))
    for i, st in enumerate(p["steps"], 1):
        yt = st.get("your_turn") or {}
        conn.execute(
            "INSERT INTO steps VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (p["id"], i, st["title"], st["body"], yt.get("prompt"),
             yt.get("answer"), int(bool(st.get("reveals_answer")))))
    conn.execute("DELETE FROM wrong_choices WHERE problem_id = %s", (p["id"],))
    for letter, text in p.get("wrong_choices", {}).items():
        conn.execute("INSERT INTO wrong_choices VALUES (%s, %s, %s)", (p["id"], letter, text))


def load_content(folders=None, check_only=False):
    """Upsert every worked/*.json under the given folders (or all folders, if
    folders is falsy). Returns True if nothing was skipped."""
    conn = None if check_only else connect()
    existing = {r["id"] for r in conn.execute("SELECT id FROM problems").fetchall()} if conn else set()
    added, updated, skipped = 0, 0, 0
    for folder in content_dirs(folders):
        key_file = folder / "answer_key.json"
        key = json.loads(key_file.read_text()) if key_file.exists() else {}
        for f in sorted((folder / "worked").glob("*.json")):
            p, errors = load_and_check(f, key)
            if errors:
                skipped += 1
                print(f"SKIP {f.name}: " + "; ".join(errors))
                continue
            if p["id"] in existing:
                updated += 1
            else:
                added += 1
            if conn:
                upsert_problem(conn, folder, p)
    if conn:
        conn.commit()
        conn.close()
    verb = "checked" if check_only else "loaded"
    print(f"{verb}: {added} new, {updated} updated, {skipped} skipped")
    return skipped == 0


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Upsert worked-solution JSON files into the app database.")
    parser.add_argument("folders", nargs="*",
                         help="folder(s) under amc_questions/ to load, e.g. 2019 or "
                              "ace-amc-book/geometry (omit and pass --all to load everything)")
    parser.add_argument("--all", action="store_true", help="load every content folder")
    parser.add_argument("--check", action="store_true", help="validate only, write nothing")
    args = parser.parse_args(argv)
    if not args.folders and not args.all:
        parser.error("name at least one folder under amc_questions/ (e.g. 2019), or pass --all")
    ok = load_content(folders=args.folders or None, check_only=args.check)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
