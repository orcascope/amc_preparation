"""Entry point for the Databricks Job that loads content into Lakebase.

Lives at the repo root (not tools/, which is excluded from the bundle sync in
databricks.yml) so the load_content job resource can point at it.

Serverless job tasks don't reliably get environment variables set the way a
Databricks App does — the one mechanism guaranteed to reach any job task,
serverless or classic, is its own parameters (plain argv). So databricks.yml
passes the Lakebase connection details as parameters, and this file turns
them into the env vars app/db.py expects *before* importing app.content_loader
(app/db.py reads LAKEBASE_ENDPOINT at import time). Everything else forwards
straight to app/content_loader.py's main().

Usage (as the job runs it):
    python run_content_loader.py --database-url <url> --lakebase-endpoint <endpoint> --all
"""
import os
import sys


def _pop_arg(argv, flag):
    """Remove `flag value` from argv in place and return value, or None if absent."""
    if flag in argv:
        i = argv.index(flag)
        value = argv[i + 1]
        del argv[i:i + 2]
        return value
    return None


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    database_url = _pop_arg(argv, "--database-url")
    lakebase_endpoint = _pop_arg(argv, "--lakebase-endpoint")
    if database_url:
        os.environ["DATABASE_URL"] = database_url
        os.environ["USE_LAKEBASE"] = "1"
    if lakebase_endpoint:
        os.environ["LAKEBASE_ENDPOINT"] = lakebase_endpoint

    from app.content_loader import main as load_main  # noqa: E402 (import after env vars are set)
    return load_main(argv)


if __name__ == "__main__":
    # Databricks runs spark_python_task scripts through an IPython-style wrapper
    # that treats ANY sys.exit() — even sys.exit(0) — as a failed run. So: raise
    # only on a genuine error (something was skipped); let a clean run just finish.
    status = main()
    if status:
        raise RuntimeError(f"content loader exited with status {status} — see output above")
