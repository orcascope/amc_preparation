"""Start the AMC 10 Practice app.

Usage:
    python app/run.py

Starts the local server at http://localhost:5000. Everything runs on this
machine; no internet connection is needed once the page has loaded once
(fonts and KaTeX are bundled under app/static/vendor).

This no longer loads content on startup. Content (problems/steps/wrong_choices)
is loaded separately and incrementally with app/content_loader.py — run it
yourself after adding or changing worked solutions:

    python -m app.content_loader <folder>   # e.g. 2019, or ace-amc-book/geometry
    python -m app.content_loader --all      # first-time load of everything
"""
import os

from app.db import connect  # noqa: E402
from app.server import app  # noqa: E402

URL = "http://127.0.0.1:5000"

if __name__ == "__main__":
    conn = connect()
    n = conn.execute("SELECT COUNT(*) AS n FROM problems").fetchone()["n"]
    conn.close()
    if n == 0:
        print("No problems loaded yet — run: python -m app.content_loader --all")
    else:
        print(f"{n} problems loaded")
    on_databricks = bool(os.environ.get("DATABRICKS_APP_PORT"))
    host = "0.0.0.0" if on_databricks else "127.0.0.1"
    port = int(os.environ.get("DATABRICKS_APP_PORT", 5000))
    print(f"Starting server on {host}:{port} (Ctrl+C to stop)")
    app.run(host=host, port=port, debug=False)
