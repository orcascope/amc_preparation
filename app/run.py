"""Start the AMC 10 Practice app.

Usage:
    python app/run.py

Imports the latest worked-solution JSON files, then starts the local server
at http://localhost:5000. Everything runs on this machine; no internet
connection is needed once the page has loaded once (fonts and KaTeX are
bundled under app/static/vendor).
"""
import sys
import webbrowser
from pathlib import Path
from threading import Timer

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))

from import_worked import main as import_worked  # noqa: E402
from server import app  # noqa: E402

URL = "http://127.0.0.1:5000"

if __name__ == "__main__":
    print("Importing worked solutions...")
    import_worked()
    Timer(1.0, lambda: webbrowser.open(URL)).start()
    print(f"Starting server at {URL} (Ctrl+C to stop)")
    app.run(host="127.0.0.1", port=5000, debug=False)
