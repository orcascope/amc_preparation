import sqlite3
from pathlib import Path

APP_DIR = Path(__file__).resolve().parent
ROOT = APP_DIR.parent
QUESTIONS_DIR = ROOT / "amc_questions"
DB_PATH = APP_DIR / "data" / "amc.db"


def connect(path=DB_PATH):
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    conn.executescript((APP_DIR / "schema.sql").read_text(encoding="utf-8"))
    # Databases made before these columns existed: add them (content is re-imported anyway).
    have = {r[1] for r in conn.execute("PRAGMA table_info(problems)")}
    for col, decl in (("collection", "TEXT NOT NULL DEFAULT ''"),
                      ("source_label", "TEXT NOT NULL DEFAULT ''"),
                      ("accept_json", "TEXT NOT NULL DEFAULT '[]'")):
        if col not in have:
            conn.execute(f"ALTER TABLE problems ADD COLUMN {col} {decl}")
    return conn
