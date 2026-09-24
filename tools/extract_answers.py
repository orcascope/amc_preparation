"""Read the official answer letters from an AMC solutions PDF.

Usage:
    python tools/extract_answers.py amc_questions/2022/solutions/AMC_10A_2022_Solutions.pdf

Merges the result into amc_questions/<year>/answer_key.json as
{"AMC_10A_2022": {"1": "D", ...}}. Scanned PDFs have no text layer; for those
the script says so and the key has to be entered by hand from the PDF.
"""
import json
import re
import sys
from pathlib import Path

import fitz  # PyMuPDF

ANSWER_RE = re.compile(r"Answer\s*\(([A-E])\)")


def main(pdf_path):
    pdf = Path(pdf_path)
    test_id = re.sub(r"_Solutions$", "", pdf.stem)
    text = "".join(page.get_text() for page in fitz.open(pdf))
    letters = ANSWER_RE.findall(text)
    if len(letters) != 25:
        raise SystemExit(f"{pdf.name}: found {len(letters)} answers, expected 25 "
                         "(scanned PDF? enter the key by hand)")
    key_file = pdf.parent.parent / "answer_key.json"
    keys = json.loads(key_file.read_text()) if key_file.exists() else {}
    keys[test_id] = {str(i + 1): letter for i, letter in enumerate(letters)}
    key_file.write_text(json.dumps(keys, indent=2) + "\n")
    print(test_id, "".join(letters))


if __name__ == "__main__":
    main(sys.argv[1])
