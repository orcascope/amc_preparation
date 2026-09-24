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
    return conn
