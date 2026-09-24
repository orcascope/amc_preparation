"""AMC 10 Practice: a small local web app.

Run:  python app/server.py      then open http://localhost:5000

Everything is served from this machine. The worked solutions were written
ahead of time (see tools/TUTOR_BRIEF.md), so no model is called while students
use the app. Answers and steps stay on the server until the student asks for
them.
"""
import json

from flask import Flask, abort, g, jsonify, request, send_from_directory

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
    row = db().execute("SELECT id FROM students WHERE id = ?", (sid,)).fetchone()
    if not row:
        abort(400, "unknown student")
    db().execute("UPDATE students SET last_seen = datetime('now') WHERE id = ?", (row["id"],))
    return row["id"]


def problem_row(pid):
    row = db().execute("SELECT * FROM problems WHERE id = ?", (pid,)).fetchone()
    if not row:
        abort(404)
    return row


def progress_row(sid, pid):
    db().execute("INSERT OR IGNORE INTO progress (student_id, problem_id) VALUES (?, ?)", (sid, pid))
    return db().execute(
        "SELECT * FROM progress WHERE student_id = ? AND problem_id = ?", (sid, pid)).fetchone()


def update_progress(sid, pid, **fields):
    sets = ", ".join(f"{k} = ?" for k in fields)
    db().execute(
        f"UPDATE progress SET {sets}, updated_at = datetime('now') WHERE student_id = ? AND problem_id = ?",
        (*fields.values(), sid, pid))
    db().commit()


def topic_problems(topic):
    """Problems of one type in study order: easiest first."""
    return db().execute(
        "SELECT id, subtopic, difficulty FROM problems WHERE topic = ? "
        "ORDER BY difficulty, year, contest, session, number", (topic,)).fetchall()


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
    total = db().execute("SELECT COUNT(*) FROM problems").fetchone()[0]
    rows = db().execute(
        "SELECT s.id, s.name, s.last_seen, "
        "  (SELECT COUNT(*) FROM progress p WHERE p.student_id = s.id AND p.completed "
        "     AND p.status IN ('solved_own', 'solved_hints')) AS solved, "
        "  (SELECT COUNT(*) FROM progress p WHERE p.student_id = s.id) AS touched "
        "FROM students s ORDER BY s.last_seen DESC").fetchall()
    return jsonify(total=total, students=[dict(r) for r in rows])


@app.post("/api/students")
def add_student():
    name = " ".join(((request.get_json(silent=True) or {}).get("name") or "").split())
    if not 1 <= len(name) <= 40:
        abort(400, "name must be 1-40 characters")
    db().execute("INSERT OR IGNORE INTO students (name) VALUES (?)", (name,))
    db().commit()
    row = db().execute("SELECT id, name FROM students WHERE name = ?", (name,)).fetchone()
    return jsonify(dict(row))


# ---------- topics and problem lists ----------

@app.get("/api/topics")
def topics():
    sid = student_id()
    prog = {r["problem_id"]: r for r in db().execute(
        "SELECT * FROM progress WHERE student_id = ?", (sid,))}
    out, totals = [], {"total": 0, "solved_own": 0, "solved_hints": 0, "shown": 0}
    for key, name in TOPIC_NAMES.items():
        rows = topic_problems(key)
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
        "WHERE p.student_id = ? AND NOT p.completed ORDER BY p.updated_at DESC LIMIT 1",
        (sid,)).fetchone()
    resume = None
    if cont:
        ids = [r["id"] for r in topic_problems(cont["topic"])]
        resume = {"id": cont["problem_id"], "topic": cont["topic"],
                  "topic_name": TOPIC_NAMES[cont["topic"]], "subtopic": cont["subtopic"],
                  "number": ids.index(cont["problem_id"]) + 1, "attempts": cont["attempts"]}
    return jsonify(topics=out, totals=totals, resume=resume)


@app.get("/api/topics/<topic>")
def topic_detail(topic):
    if topic not in TOPIC_NAMES:
        abort(404)
    sid = student_id()
    prog = {r["problem_id"]: r for r in db().execute(
        "SELECT * FROM progress WHERE student_id = ?", (sid,))}
    problems = [{"id": r["id"], "number": i, "subtopic": r["subtopic"],
                 "difficulty": r["difficulty"], "status": display_status(prog.get(r["id"]))}
                for i, r in enumerate(topic_problems(topic), 1)]
    return jsonify(key=topic, name=TOPIC_NAMES[topic], problems=problems)


# ---------- one problem ----------

@app.get("/api/problems/<pid>")
def problem(pid):
    sid = student_id()
    p = problem_row(pid)
    ids = [r["id"] for r in topic_problems(p["topic"])]
    i = ids.index(pid)
    prog = db().execute("SELECT * FROM progress WHERE student_id = ? AND problem_id = ?",
                        (sid, pid)).fetchone()
    tried = [r["choice"] for r in db().execute(
        "SELECT DISTINCT choice FROM attempts WHERE student_id = ? AND problem_id = ? AND NOT correct",
        (sid, pid))]
    n_steps = db().execute("SELECT COUNT(*) FROM steps WHERE problem_id = ?", (pid,)).fetchone()[0]
    data = {
        "id": pid, "topic": p["topic"], "topic_name": TOPIC_NAMES[p["topic"]],
        "subtopic": p["subtopic"], "difficulty": p["difficulty"],
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
    choice = (request.get_json(silent=True) or {}).get("choice")
    if choice not in json.loads(p["choices_json"]):
        abort(400, "choice must be A-E")
    correct = choice == p["answer_choice"]
    prog = progress_row(sid, pid)
    db().execute("INSERT INTO attempts (student_id, problem_id, choice, correct) VALUES (?,?,?,?)",
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
        row = db().execute("SELECT explanation FROM wrong_choices WHERE problem_id = ? AND choice = ?",
                           (pid, choice)).fetchone()
        out["explanation"] = row["explanation"] if row else None
    return jsonify(out)


@app.get("/api/problems/<pid>/steps")
def steps(pid):
    """Steps 1..upto. The final (answer) step is only sent with ?upto=all."""
    sid = student_id()
    problem_row(pid)
    rows = db().execute("SELECT * FROM steps WHERE problem_id = ? ORDER BY idx", (pid,)).fetchall()
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
