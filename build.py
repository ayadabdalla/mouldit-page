"""
Builds the MouldIt project page.

    PYTHONPATH=~/utn/mouldit_benchmark/src python build.py

Fills the header curves from the real reference cycle and writes
  index.html      full HTML document for GitHub Pages (serve this folder)
  preview.html    the same page without the document skeleton, for the claude.ai preview
"""

from pathlib import Path

import numpy as np
from mouldit_benchmark.datasets.reference_preprocessing import CHANNELS, ReferencePreprocessing

ROOT = Path(__file__).resolve().parent
W, H = 1000, 40

_, x = ReferencePreprocessing().load(CHANNELS)
page = (ROOT / "src" / "page.html").read_text()
for i, name in enumerate(CHANNELS):
    s = x[i][::2]
    t = np.linspace(0, W, len(s))
    path = "M" + " L".join(f"{a:.1f},{H - 3 - (H - 6) * b:.1f}" for a, b in zip(t, s))
    page = page.replace("{{" + name + "}}", path)
assert not any("{{" + c + "}}" in page for c in CHANNELS)

(ROOT / "preview.html").write_text(page)
(ROOT / "index.html").write_text(
    '<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
    '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
    "</head>\n<body>\n" + page + "\n</body>\n</html>\n")
print("wrote index.html and preview.html")
