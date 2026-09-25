"""AMC 10 Practice: a small local web app.

Run:  python app/server.py      then open http://localhost:5000

Everything is served from this machine. The worked solutions were written
ahead of time (see tools/TUTOR_BRIEF.md), so no model is called while students
use the app. Answers and steps stay on the server until the student asks for
them.
"""
import json

from flask import Flask, abort, g, jsonify, request, send_from_directory

from answers import matches
from db import APP_DIR, QUESTIONS_DIR, connect

app = Flask(__name__, static_folder=str(APP_DIR / "static"), static_url_path="/static")

TOPIC_NAMES = {
    "algebra": "Algebra",
    "geometry": "Geometry",
    "number_theory": "Number theory",
    "counting_probability": "Counting & probability",
    "arithmetic_logic": "Arithmetic & logic",
}
SOLVED = ("solved_own", "solved_hints")
OUTCOMES = ("solved_own", "solved_hints", "shown")


def db():
    if "db" not in g:
        g.db = connect()
    return g.db


@app.teardown_appcontext
def close_db(_exc):
    conn = g.pop("db", None)
    if conn:
        conn.close()


def student_id():
    sid = request.args.get("student") or (request.get_json(silent=True) or {}).get("student")
    try:
        sid = int(sid)
    except (TypeError, ValueError):
        abort(400, "unknown student")
    row = db().execute("SELECT id FROM students WHERE id = %s", (sid,)).fetchone()
    if not row:
        abort(400, "unknown student")
    db().execute("UPDATE students SET last_seen = now() WHERE id = %s", (row["id"],))
    return row["id"]


def problem_row(pid):
    row = db().execute("SELECT * FROM problems WHERE id = %s", (pid,)).fetchone()
    if not row:
        abort(404)
    return row


def progress_row(sid, pid):
    db().execute("INSERT INTO progress (student_id, problem_id) VALUES (%s, %s) ON CONFLICT DO NOTHING", (sid, pid))
    return db().execute(
        "SELECT * FROM progress WHERE student_id = %s AND problem_id = %s", (sid, pid)).fetchone()


def update_progress(sid, pid, **fields):
    sets = ", ".join(f"{k} = %s" for k in fields)
    db().execute(
        f"UPDATE progress SET {sets}, updated_at = now() WHERE student_id = %s AND problem_id = %s",
        (*fields.values(), sid, pid))
    db().commit()


def year_filter():
    """The ?year= filter: a collection key ('2018', 'book', ...) or None for everything."""
    return request.args.get("year") or None


def collections():
    """[{key, label}] for every collection that has problems: contest years first, then the book."""
    keys = [r["collection"] for r in db().execute("SELECT DISTINCT collection FROM problems")]
    keys.sort(key=lambda k: (not k.isdigit(), k))
    return [{"key": k, "label": "ACE book" if k == "book" else k} for k in keys]


def topic_problems(topic, coll=None):
    """Problems of one type in study order: easiest first. coll=None means every collection."""
    return db().execute(
        "SELECT id, subtopic, difficulty FROM problems WHERE topic = %s AND (%s::text IS NULL OR collection = %s) "
        "ORDER BY difficulty, year, contest, session, number", (topic, coll, coll)).fetchall()


def step_dict(row):
    d = {"title": row["title"], "body": row["body"], "reveals_answer": bool(row["reveals_answer"])}
    if row["your_turn_prompt"]:
        d["your_turn"] = {"prompt": row["your_turn_prompt"], "answer": row["your_turn_answer"]}
    return d


def display_status(p):
    """What the student sees for one problem: new, trying, solved_own, solved_hints or shown."""
    if p is None:
        return "new"
    if p["completed"]:
        return p["status"]
    return "trying"


# ---------- pages ----------

@app.get("/")
def index():
    return send_from_directory(APP_DIR / "static", "index.html")


@app.get("/images/<path:path>")
def image(path):
    return send_from_directory(QUESTIONS_DIR, path)


# ---------- students ----------

@app.get("/api/students")
def list_students():
    total = db().execute("SELECT COUNT(*) AS n FROM problems").fetchone()["n"]
    rows = db().execute(
        "SELECT s.id, s.name, s.last_seen, "
        "  (SELECT COUNT(*) FROM progress p WHERE p.student_id = s.id AND p.completed = 1 "
        "     AND p.status IN ('solved_own', 'solved_hints')) AS solved, "
        "  (SELECT COUNT(*) FROM progress p WHERE p.student_id = s.id) AS touched "
        "FROM students s ORDER BY s.last_seen DESC").fetchall()
    return jsonify(total=total, students=[dict(r) for r in rows])


@app.post("/api/students")
def add_student():
    name = " ".join(((request.get_json(silent=True) or {}).get("name") or "").split())
    if not 1 <= len(name) <= 40:
        abort(400, "name must be 1-40 characters")
    db().execute("INSERT INTO students (name) VALUES (%s) ON CONFLICT DO NOTHING", (name,))
    db().commit()
    row = db().execute("SELECT id, name FROM students WHERE lower(name) = lower(%s)", (name,)).fetchone()
    return jsonify(dict(row))


def student_or_404(sid):
    if not db().execute("SELECT 1 FROM students WHERE id = %s", (sid,)).fetchone():
        abort(404)


@app.post("/api/students/<int:sid>/reset")
def reset_student(sid):
    """Forget everything a student has done, but keep their name."""
    student_or_404(sid)
    db().execute("DELETE FROM attempts WHERE student_id = %s", (sid,))
    db().execute("DELETE FROM progress WHERE student_id = %s", (sid,))
    db().commit()
    return jsonify(ok=True)


@app.delete("/api/students/<int:sid>")
def delete_student(sid):
    student_or_404(sid)
    db().execute("DELETE FROM attempts WHERE student_id = %s", (sid,))
    db().execute("DELETE FROM progress WHERE student_id = %s", (sid,))
    db().execute("DELETE FROM students WHERE id = %s", (sid,))
    db().commit()
    return jsonify(ok=True)


# ---------- topics and problem lists ----------

@app.get("/api/topics")
def topics():
    sid = student_id()
    years = collections()
    year = year_filter()
    if year not in [c["key"] for c in years]:
        year = None
    prog = {r["problem_id"]: r for r in db().execute(
        "SELECT * FROM progress WHERE student_id = %s", (sid,))}
    out, totals = [], {"total": 0, "solved_own": 0, "solved_hints": 0, "shown": 0}
    for key, name in TOPIC_NAMES.items():
        rows = topic_problems(key, year)
        if not rows:
            continue
        counts = {"solved_own": 0, "solved_hints": 0, "shown": 0, "trying": 0, "new": 0}
        for r in rows:
            counts[display_status(prog.get(r["id"]))] += 1
        subtopics = list(dict.fromkeys(r["subtopic"] for r in rows))
        out.append({"key": key, "name": name, "total": len(rows), "counts": counts,
                    "subtopics": subtopics[:4]})
        totals["total"] += len(rows)
        for k in ("solved_own", "solved_hints", "shown"):
            totals[k] += counts[k]

    cont = db().execute(
        "SELECT p.problem_id, pr.topic, pr.subtopic, p.attempts FROM progress p "
        "JOIN problems pr ON pr.id = p.problem_id "
        "WHERE p.student_id = %s AND p.completed = 0 AND (%s::text IS NULL OR pr.collection = %s) "
        "ORDER BY p.updated_at DESC LIMIT 1",
        (sid, year, year)).fetchone()
    resume = None
    if cont:
        ids = [r["id"] for r in topic_problems(cont["topic"], year)]
        resume = {"id": cont["problem_id"], "topic": cont["topic"],
                  "topic_name": TOPIC_NAMES[cont["topic"]], "subtopic": cont["subtopic"],
                  "number": ids.index(cont["problem_id"]) + 1, "attempts": cont["attempts"]}
    return jsonify(topics=out, totals=totals, resume=resume, years=years, year=year)


@app.get("/api/topics/<topic>")
def topic_detail(topic):
    if topic not in TOPIC_NAMES:
        abort(404)
    sid = student_id()
    prog = {r["problem_id"]: r for r in db().execute(
        "SELECT * FROM progress WHERE student_id = %s", (sid,))}
    problems = [{"id": r["id"], "number": i, "subtopic": r["subtopic"],
                 "difficulty": r["difficulty"], "status": display_status(prog.get(r["id"]))}
                for i, r in enumerate(topic_problems(topic, year_filter()), 1)]
    return jsonify(key=topic, name=TOPIC_NAMES[topic], problems=problems)


# ---------- one problem ----------

@app.get("/api/problems/<pid>")
def problem(pid):
    sid = student_id()
    p = problem_row(pid)
    ids = [r["id"] for r in topic_problems(p["topic"], year_filter())]
    if pid not in ids:  # opened from outside the current year filter
        ids = [r["id"] for r in topic_problems(p["topic"])]
    i = ids.index(pid)
    prog = db().execute("SELECT * FROM progress WHERE student_id = %s AND problem_id = %s",
                        (sid, pid)).fetchone()
    tried = [r["choice"] for r in db().execute(
        "SELECT DISTINCT choice FROM attempts WHERE student_id = %s AND problem_id = %s AND correct = 0",
        (sid, pid))]
    n_steps = db().execute("SELECT COUNT(*) AS n FROM steps WHERE problem_id = %s", (pid,)).fetchone()["n"]
    data = {
        "id": pid, "topic": p["topic"], "topic_name": TOPIC_NAMES[p["topic"]],
        "subtopic": p["subtopic"], "difficulty": p["difficulty"], "source_label": p["source_label"],
        "number": i + 1, "of": len(ids),
        "next": ids[i + 1] if i + 1 < len(ids) else None,
        "image": f"/images/{p['image']}", "text": p["text"],
        "choices": json.loads(p["choices_json"]),
        "steps_total": n_steps, "wrong_tried": tried,
        "status": display_status(prog),
        "hints_used": prog["hints_used"] if prog else 0,
        "attempts": prog["attempts"] if prog else 0,
    }
    if prog and (prog["completed"] or prog["solution_viewed"]):
        data["answer"] = {"choice": p["answer_choice"], "value": p["answer_value"]}
    return jsonify(data)


@app.post("/api/problems/<pid>/attempt")
def attempt(pid):
    sid = student_id()
    p = problem_row(pid)
    body = request.get_json(silent=True) or {}
    choices = json.loads(p["choices_json"])
    if choices:
        choice = body.get("choice")
        if choice not in choices:
            abort(400, "choice must be A-E")
        correct = choice == p["answer_choice"]
    else:  # open-ended: a typed answer
        choice = " ".join(str(body.get("answer") or "").split())[:60]
        if not choice:
            abort(400, "answer is required")
        correct = matches(choice, json.loads(p["accept_json"]))
    prog = progress_row(sid, pid)
    db().execute("INSERT INTO attempts (student_id, problem_id, choice, correct) VALUES (%s,%s,%s,%s)",
                 (sid, pid, choice, int(correct)))
    fields = {"attempts": prog["attempts"] + 1}
    if correct and not prog["completed"]:
        if prog["solution_viewed"]:
            fields["status"] = "shown"
        else:
            fields["status"] = "solved_hints" if prog["hints_used"] else "solved_own"
        fields["completed"] = 1
    update_progress(sid, pid, **fields)
    out = {"correct": correct}
    if correct:
        out["answer"] = {"choice": p["answer_choice"], "value": p["answer_value"]}
        out["status"] = fields.get("status", prog["status"])
        out["hints_used"] = prog["hints_used"]
    else:
        row = db().execute("SELECT explanation FROM wrong_choices WHERE problem_id = %s AND choice = %s",
                           (pid, choice)).fetchone()
        out["explanation"] = row["explanation"] if row else None
    return jsonify(out)


@app.get("/api/problems/<pid>/steps")
def steps(pid):
    """Steps 1..upto. The final (answer) step is only sent with ?upto=all."""
    sid = student_id()
    problem_row(pid)
    rows = db().execute("SELECT * FROM steps WHERE problem_id = %s ORDER BY idx", (pid,)).fetchall()
    last_hint = len(rows) - 1  # every step before the answer step
    upto = request.args.get("upto", "1")
    n = len(rows) if upto == "all" else max(1, min(int(upto), last_hint))
    prog = progress_row(sid, pid)
    fields = {"hints_used": max(prog["hints_used"], min(n, last_hint))}
    if n == len(rows):
        fields["solution_viewed"] = 1
    update_progress(sid, pid, **fields)
    out = {"steps": [step_dict(r) for r in rows[:n]], "total": len(rows)}
    if n == len(rows):
        p = problem_row(pid)
        out["answer"] = {"choice": p["answer_choice"], "value": p["answer_value"]}
    return jsonify(out)


@app.post("/api/problems/<pid>/complete")
def complete(pid):
    sid = student_id()
    problem_row(pid)
    outcome = (request.get_json(silent=True) or {}).get("outcome")
    if outcome not in OUTCOMES:
        abort(400, "outcome must be one of " + ", ".join(OUTCOMES))
    progress_row(sid, pid)
    update_progress(sid, pid, status=outcome, completed=1)
    return jsonify(ok=True, status=outcome)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
