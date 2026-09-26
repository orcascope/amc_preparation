"""Start the AMC 10 Practice app.

Usage:
    python app/run.py

Imports the latest worked-solution JSON files, then starts the local server
at http://localhost:5000. Everything runs on this machine; no internet
connection is needed once the page has loaded once (fonts and KaTeX are
bundled under app/static/vendor).
"""
import sys, os
import webbrowser
from pathlib import Path
from threading import Timer


from app.import_worked import main as import_worked  # noqa: E402
from app.server import app  # noqa: E402

URL = "http://127.0.0.1:5000"

if __name__ == "__main__":
    print("Importing worked solutions...")
    import_worked()
    on_databricks = bool(os.environ.get("DATABRICKS_APP_PORT"))
    host = "0.0.0.0" if on_databricks else "127.0.0.1"
    port = int(os.environ.get("DATABRICKS_APP_PORT", 5000))
    print(f"Starting server on {host}:{port} (Ctrl+C to stop)")
    app.run(host=host, port=port, debug=False)
