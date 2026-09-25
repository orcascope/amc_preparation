"""Database connection (PostgreSQL).

The connection string comes from DATABASE_URL, read from the environment or
from a .env file at the repository root, for example:

    DATABASE_URL=postgresql://amc:secret@localhost:5432/amc

Rows come back as dicts. Queries use %s placeholders (psycopg style).
"""
import os
from pathlib import Path

import psycopg
from dotenv import load_dotenv
from psycopg.rows import dict_row

APP_DIR = Path(__file__).resolve().parent
ROOT = APP_DIR.parent
QUESTIONS_DIR = ROOT / "amc_questions"

load_dotenv(ROOT / ".env")

_schema_ready = False


def database_url():
    url = os.environ.get("DATABASE_URL", "").strip()
    if not url:
        raise RuntimeError(
            "DATABASE_URL is not set. Add a line like\n"
            "  DATABASE_URL=postgresql://user:password@localhost:5432/amc\n"
            f"to {ROOT / '.env'} (see .env.example).")
    return url


def connect():
    """A new connection; the schema is created the first time in each process."""
    global _schema_ready
    conn = psycopg.connect(database_url(), row_factory=dict_row)
    if not _schema_ready:
        conn.execute((APP_DIR / "schema.sql").read_text(encoding="utf-8"))
        conn.commit()
        _schema_ready = True
    return conn
