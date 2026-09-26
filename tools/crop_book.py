"""Crop each Problem/Example statement out of the ACE book into its own PNG.

Usage:
    python tools/crop_book.py <book.pdf> <topic> <first_section> <last_section>
    python tools/crop_book.py .claude/skills/ace-the-amc-book/references/ACE_The_AMC_10_and_12.pdf number_theory 2.1 2.6

Writes amc_questions/ace-amc-book/<topic>/images/ACE_<ch>_<sec>_<nn>.png (for
example Problem 2.2.7 -> ACE_2_2_07.png) and prints an index of what it found:
id, kind, source line and the PDF pages that hold the item and its solution.

Each item sits in a framed box. The crop runs from the top of the box to the
end of the statement: the bottom of the box for a Problem, or the
"Solution:" line for an Example (whose solution is inside the box). A box
that breaks across a page is stitched back together.
"""
import json
import re
import sys
from pathlib import Path

import pymupdf as fitz

ROOT = Path(__file__).resolve().parent.parent
HEADER_Y = 66     # running header line sits above this
FOOTER_Y = 775    # page number sits below this
ZOOM = 2.5
ITEM_RE = re.compile(r"^(Problem|Example) (\d+)\.(\d+)\.(\d+)")


def lines(page):
    for b in page.get_text("dict")["blocks"]:
        for l in b.get("lines", []):
            yield "".join(s["text"] for s in l["spans"]).strip(), fitz.Rect(l["bbox"])


def box_around(page, y):
    """The framed box (a drawn rectangle) that contains height y, if any."""
    best = None
    for d in page.get_drawings():
        r = d["rect"]
        if r.x0 < 100 and r.width > 300 and r.height > 12 and r.y0 - 3 <= y <= r.y1:
            if best is None or r.height > best.height:
                best = r
    return best


def statement_pieces(doc, pno, y):
    """[(page, clip)] from the item label at height y down to the end of its statement."""
    pieces = []
    while True:
        page = doc[pno]
        box = box_around(page, y + 2)
        top = (box.y0 if box else y) - 3
        # Search for the word itself: a "Solution:" line holding a tall formula has a taller box.
        sol = min((r.y0 for r in page.search_for("Solution:") if r.y0 > y + 2), default=None)
        if box and sol is not None and sol < box.y1:        # Example: solution inside the box
            # The solution line may hold a tall formula that starts above the word
            # "Solution:", so end tight under the last left-margin line above it.
            above = [r.y1 for t, r in lines(page) if r.x0 < 103 and y - 2 <= r.y0 and r.y1 <= sol + 1]
            bottom = (max(above) + 2) if above else sol - 3
        elif box:
            bottom = box.y1 + 3
        else:
            bottom = (sol - 3) if sol is not None else FOOTER_Y
        pieces.append((pno, fitz.Rect(80, max(top, HEADER_Y), 516, min(bottom, FOOTER_Y))))
        # A box that runs to the foot of the page continues on the next page.
        if box and box.y1 > FOOTER_Y - 25 and sol is None and pno + 1 < doc.page_count:
            pno, y = pno + 1, HEADER_Y + 8
            continue
        return pieces


def render(doc, pieces, out):
    """Stack the pieces vertically on one blank page and save it as a PNG."""
    width = pieces[0][1].width
    height = sum(c.height for _, c in pieces)
    tmp = fitz.open()
    page = tmp.new_page(width=width, height=height)
    y = 0
    for pno, clip in pieces:
        page.show_pdf_page(fitz.Rect(0, y, width, y + clip.height), doc, pno, clip=clip)
        y += clip.height
    page.get_pixmap(matrix=fitz.Matrix(ZOOM, ZOOM)).save(out)


def section_key(s):
    a, b = s.split(".")
    return int(a), int(b)


def main(pdf, topic, first, last):
    doc = fitz.open(pdf)
    lo, hi = section_key(first), section_key(last)
    out_dir = ROOT / "amc_questions" / "ace-amc-book" / topic / "images"
    out_dir.mkdir(parents=True, exist_ok=True)
    found, seen = [], set()
    for pno in range(doc.page_count):
        for text, rect in lines(doc[pno]):
            m = ITEM_RE.match(text)
            if not m or rect.x0 > 110:
                continue
            ch, sec, num = int(m.group(2)), int(m.group(3)), int(m.group(4))
            if not lo <= (ch, sec) <= hi or (ch, sec, num) in seen:
                continue
            seen.add((ch, sec, num))
            item_id = f"ACE_{ch}_{sec}_{num:02d}"
            pieces = statement_pieces(doc, pno, rect.y0)
            render(doc, pieces, out_dir / f"{item_id}.png")
            src = ""
            for p, clip in pieces:
                for t, r in lines(doc[p]):
                    if t.startswith("Source:") and clip.y0 <= r.y0 <= clip.y1:
                        src = t.removeprefix("Source:").strip()
                        if not src:  # "Source:" alone; the text is on the next line
                            nxt = [t2 for t2, r2 in lines(doc[p]) if 0 < r2.y0 - r.y0 < 16]
                            src = nxt[0] if nxt else ""
            found.append({"id": item_id, "kind": m.group(1).lower(), "number": f"{ch}.{sec}.{num}",
                          "source": src, "page": pno + 1, "image": f"images/{item_id}.png"})
    print(json.dumps(found, indent=1))
    print(f"{len(found)} items -> {out_dir.relative_to(ROOT)}", file=sys.stderr)


if __name__ == "__main__":
    main(*sys.argv[1:5])
