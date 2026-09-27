"""Database connection (PostgreSQL).

Two ways to connect:
- Locally: DATABASE_URL from the environment or from a .env file at the
  repository root, for example
      DATABASE_URL=postgresql://amc:secret@localhost:5432/amc
- Inside a Databricks App: DATABASE_URL (from app.yaml) names the Lakebase
  host, and the password is a short-lived OAuth token from the Databricks SDK.

Rows come back as dicts. Queries use %s placeholders (psycopg style). All
tables live in the amc_app schema.
"""
import os
import time
from pathlib import Path

import psycopg
from dotenv import load_dotenv
from psycopg.rows import dict_row

APP_DIR = Path(__file__).resolve().parent
ROOT = APP_DIR.parent
QUESTIONS_DIR = ROOT / "amc_questions"
SEARCH_PATH = "-c search_path=amc_app"

# Lakebase endpoint the app's tokens are issued for.
LAKEBASE_ENDPOINT = os.environ.get("LAKEBASE_ENDPOINT",
                                   "projects/hobby/branches/production/endpoints/primary")
# Tokens last at most 1 hour; get a new one well before that.
TOKEN_REUSE_SECONDS = 45 * 60

# DATABRICKS_APP_PORT is set only inside a running Databricks App. (DATABRICKS_HOST
# is not a safe signal: the Databricks CLI often sets it on developers' machines.)
ON_DATABRICKS_APP = bool(os.environ.get("DATABRICKS_APP_PORT"))

if not ON_DATABRICKS_APP:
    load_dotenv(ROOT / ".env")

_schema_ready = False
_workspace = None
_token = None           # (token, fetched_at)


def database_url():
    url = os.environ.get("DATABASE_URL", "").strip()
    if not url:
        raise RuntimeError(
            "DATABASE_URL is not set. Add a line like\n"
            "  DATABASE_URL=postgresql://user:password@localhost:5432/amc\n"
            f"to {ROOT / '.env'} (see .env.example).")
    return url


def lakebase_token():
    """An OAuth token for Lakebase, reused until it is close to expiring."""
    global _workspace, _token
    if _token and time.monotonic() - _token[1] < TOKEN_REUSE_SECONDS:
        return _token[0]
    if _workspace is None:
        from databricks.sdk import WorkspaceClient
        _workspace = WorkspaceClient()
    credential = _workspace.postgres.generate_database_credential(endpoint=LAKEBASE_ENDPOINT)
    _token = (credential.token, time.monotonic())
    print(f"Lakebase token refreshed (expires {credential.expire_time})")
    return _token[0]


def lakebase_connect():
    return psycopg.connect(
        database_url(),
        row_factory=dict_row,
        options=SEARCH_PATH,
        dbname="databricks_postgres",
        user=os.environ.get("DATABRICKS_CLIENT_ID") or "ars.1001@gmail.com",
        password=lakebase_token(),
        sslmode="require",
    )


def connect():
    """A new connection; the schema is created the first time in each process."""
    global _schema_ready
    if ON_DATABRICKS_APP:
        conn = lakebase_connect()
    else:
        conn = psycopg.connect(database_url(), row_factory=dict_row, options=SEARCH_PATH)
    if not _schema_ready:
        conn.execute((APP_DIR / "schema.sql").read_text(encoding="utf-8"))
        conn.commit()
        _schema_ready = True
    return conn
