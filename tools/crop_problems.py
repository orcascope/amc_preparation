"""Crop each AMC problem out of a problems PDF into its own PNG.

Usage:
    python tools/crop_problems.py amc_questions/2022/questions/AMC_10A_2022_Problems.pdf

Images are written to amc_questions/<year>/images/<ID>_P<nn>.png, where <ID> is
the PDF name without the trailing "_Problems" (e.g. AMC_10A_2022).
"""
import re
import sys
from pathlib import Path

import fitz  # PyMuPDF

ZOOM = 2.5
NUM_RE = re.compile(r"^(\d{1,2})\.(\s|$)")


def problem_starts(doc):
    """Return [(page, y, number_rect)] for problems 1..25 in reading order.

    The instructions page also has a numbered list, so restart the run every
    time a "1." is seen and keep only the run that reaches 25. number_rect is
    where the printed "7." sits, so it can be blanked out: the app numbers
    problems within each topic instead.
    """
    run = []
    for pno, page in enumerate(doc):
        if len(run) == 25:
            break
        for block in page.get_text("dict")["blocks"]:
            for line in block.get("lines", []):
                text = "".join(s["text"] for s in line["spans"]).strip()
                m = NUM_RE.match(text)
                x0, y0, _, y1 = line["bbox"]
                if not m or x0 > 120:
                    continue
                n = int(m.group(1))
                hits = page.search_for(f"{n}.", clip=fitz.Rect(x0 - 2, y0 - 2, x0 + 30, y1 + 2))
                start = (pno, y0, hits[0] if hits else None)
                if n == 1:
                    run = [start]
                elif run and n == len(run) + 1:
                    run.append(start)
    if len(run) != 25:
        raise SystemExit(f"found {len(run)} problem starts, expected 25")
    return run


def page_frame(doc):
    """Return (left, right, header_y, footer_margin) for this PDF's layout.

    Older contests are printed as a small booklet (396 x 612) rather than on
    letter paper, so the margins come from the running header ("2022 AMC 10 A
    Problems  2") instead of being fixed. On a 2022 page this gives 60, 560, 53.
    """
    for page in doc:
        for x0, y0, x1, y1, text, *_ in page.get_text("blocks"):
            if re.search(r"AMC\s*10\s*[AB]?\s*Problems", text):
                return x0 - 12, x1 + 20, y1 + 4, y0 / 2
    raise SystemExit("could not find the page header")


def content_bottom(page, footer_margin):
    """Lowest y of real content on the page, ignoring the footer."""
    limit = page.rect.height - footer_margin
    ys = [b[3] for b in page.get_text("blocks") if b[3] < limit]
    ys += [d["rect"].y1 for d in page.get_drawings() if d["rect"].y1 < limit]
    ys += [i["bbox"][3] for i in page.get_image_info() if i["bbox"][3] < limit]
    return max(ys) if ys else limit


def main(pdf_path):
    pdf = Path(pdf_path)
    test_id = re.sub(r"_Problems$", "", pdf.stem)
    out_dir = pdf.parent.parent / "images"
    out_dir.mkdir(exist_ok=True)
    doc = fitz.open(pdf)
    left, right, header_y, footer_margin = page_frame(doc)
    starts = problem_starts(doc)
    for i, (pno, y0, number_rect) in enumerate(starts):
        page = doc[pno]
        if number_rect:
            # Only changes the in-memory copy; the PDF on disk is untouched.
            page.draw_rect(number_rect + (-1, -1, 1, 1), color=None, fill=(1, 1, 1), overlay=True)
        nxt = starts[i + 1] if i + 1 < len(starts) else None
        y1 = nxt[1] - 4 if nxt and nxt[0] == pno else content_bottom(page, footer_margin) + 6
        clip = fitz.Rect(left, max(y0 - 6, header_y), right, y1)
        pix = page.get_pixmap(matrix=fitz.Matrix(ZOOM, ZOOM), clip=clip)
        out = out_dir / f"{test_id}_P{i + 1:02d}.png"
        pix.save(out)
        print(out)


if __name__ == "__main__":
    main(sys.argv[1])
