"""Wrapper so the content tools can keep calling tools/import_worked.

The importer itself lives in app/import_worked.py, because the app runs it at
startup and tools/ is not deployed with the Databricks app (.dbkignore).
Keep all importer code there; this file only forwards to it.

Usage (from the repo root):
    python -m tools.import_worked            # import everything
    python -m tools.import_worked --check    # validate only, write nothing
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))  # also works as python tools/import_worked.py

from app.import_worked import main  # noqa: E402

if __name__ == "__main__":
    sys.exit(0 if main(check_only="--check" in sys.argv) else 1)
