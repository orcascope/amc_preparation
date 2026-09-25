"""Copy student progress from the old SQLite database into PostgreSQL.

Usage:
    python tools/sqlite_to_postgres.py [path/to/amc.db]     (default: app/data/amc.db)

Copies the students, attempts and progress tables, keeping their ids, into the
database named by DATABASE_URL (.env). Content tables are not copied: run
tools/import_worked.py for those. Rows that already exist are left alone, so
running it twice is harmless.
"""
import sqlite3
import sys
from pathlib import Path

from app.db import APP_DIR, connect  # noqa: E402

TABLES = {
    "students": ("id", "name", "created_at", "last_seen"),
    "attempts": ("id", "student_id", "problem_id", "choice", "correct", "created_at"),
    "progress": ("student_id", "problem_id", "status", "hints_used", "attempts",
                 "solution_viewed", "completed", "updated_at"),
}
TIMESTAMPS = {"created_at", "last_seen", "updated_at"}


def main(path):
    src = sqlite3.connect(path)
    src.row_factory = sqlite3.Row
    dst = connect()
    for table, cols in TABLES.items():
        rows = src.execute(f"SELECT {', '.join(cols)} FROM {table}").fetchall()
        sql = (f"INSERT INTO {table} ({', '.join(cols)}) VALUES ({', '.join(['%s'] * len(cols))}) "
               "ON CONFLICT DO NOTHING")
        added = 0
        for r in rows:
            # SQLite stored UTC times as 'YYYY-MM-DD HH:MM:SS' text.
            vals = [f"{r[c]}+00" if c in TIMESTAMPS else r[c] for c in cols]
            added += dst.execute(sql, vals).rowcount
        print(f"{table}: {added} of {len(rows)} rows copied")
    for table in ("students", "attempts"):  # continue ids after the copied ones
        dst.execute(f"SELECT setval(pg_get_serial_sequence('{table}', 'id'), "
                    f"COALESCE((SELECT MAX(id) FROM {table}), 0) + 1, false)")
    dst.commit()
    dst.close()


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else APP_DIR / "data" / "amc.db")
