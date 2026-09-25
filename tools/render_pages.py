"""Render PDF pages as PNGs, so agents can read the math from the image.

Usage:
    python tools/render_pages.py <pdf> <out_dir> [first_page] [last_page]

Pages are 1-based and inclusive (default: every page). Files are named
page_<NNN>.png after the PDF page number, e.g. page_017.png. Many PDFs have a
text layer that drops exponents (2^3 comes out as "23"), so agents writing or
checking statements should look at these images, not at extracted text.
"""
import sys
from pathlib import Path

import pymupdf as fitz

ZOOM = 2.0


def main(pdf, out_dir, first=1, last=None):
    doc = fitz.open(pdf)
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    last = min(last or doc.page_count, doc.page_count)
    for pno in range(first, last + 1):
        doc[pno - 1].get_pixmap(matrix=fitz.Matrix(ZOOM, ZOOM)).save(out / f"page_{pno:03d}.png")
    print(f"pages {first}-{last} -> {out}")


if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) < 2:
        sys.exit(__doc__)
    main(args[0], args[1], *(int(a) for a in args[2:4]))
