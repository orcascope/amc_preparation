"""Merge the per-item statement files of one ACE book topic.

Usage:
    python tools/assemble_book.py number_theory

Reads amc_questions/ace-amc-book/<topic>/statements/items/*.json (one file per
item, written by the tutor step) and writes, in book order:
  statements/ACE_<topic>.json   every statement, as one list
  answer_key.json               {"ACE_2_2_07": "B", "ACE_2_3_10": "54", ...}
The answer key holds the book's own answers; app/import_worked.py checks each
lesson against it. Existing entries for other items are kept.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def book_order(item):
    return tuple(int(x) for x in item["number"].split("."))


def main(topic):
    folder = ROOT / "amc_questions" / "ace-amc-book" / topic
    items_dir = folder / "statements" / "items"
    new = [json.loads(f.read_text(encoding="utf-8")) for f in sorted(items_dir.glob("*.json"))]
    out = folder / "statements" / f"ACE_{topic}.json"
    old = json.loads(out.read_text(encoding="utf-8"))["items"] if out.exists() else []
    merged = {i["id"]: i for i in old}
    merged.update({i["id"]: i for i in new})
    items = sorted(merged.values(), key=book_order)
    out.write_text(json.dumps({"book": "ACE The AMC 10 and AMC 12", "topic": topic, "items": items},
                              indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    key_file = folder / "answer_key.json"
    key = json.loads(key_file.read_text()) if key_file.exists() else {}
    key.update({i["id"]: i["book_answer"] for i in items})
    key_file.write_text(json.dumps(dict(sorted(key.items(), key=lambda kv: book_order(merged[kv[0]])
                                               if kv[0] in merged else (99,))), indent=2) + "\n")
    print(f"{len(items)} items -> {out.relative_to(ROOT)} and answer_key.json")


if __name__ == "__main__":
    main(sys.argv[1])
