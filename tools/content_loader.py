"""Wrapper so the content tools can keep calling tools/content_loader.

The loader itself lives in app/content_loader.py, because it's part of the
deployed app; tools/ is not deployed to Databricks (.dbkignore). Keep all
loader code there; this file only forwards to it.

Usage (from the repo root):
    python -m tools.content_loader 2019              # upsert just that folder
    python -m tools.content_loader --all              # upsert every folder
    python -m tools.content_loader 2019 --check       # validate only, write nothing
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))  # also works as python tools/content_loader.py

from app.content_loader import main  # noqa: E402

if __name__ == "__main__":
    sys.exit(main())
