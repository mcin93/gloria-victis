"""Wstawia wybrany emblemat (symbol gv-e1 z assets/emblemat-warianty.svg) między znaczniki
<!--EMBLEMAT-E1--> i <!--/EMBLEMAT-E1--> w podanych plikach HTML. Można odpalać wielokrotnie.
Użycie: python tools/wstaw_e1.py index.html wersja-b/index.html"""
import re
import sys
from pathlib import Path

root = Path(__file__).resolve().parent.parent
warianty = (root / "assets" / "emblemat-warianty.svg").read_text(encoding="utf-8")
e1 = re.search(r'<symbol id="gv-e1".*?</symbol>', warianty, re.S).group(0)
for name in sys.argv[1:]:
    p = Path(name)
    html = p.read_text(encoding="utf-8")
    html, n = re.subn(r"<!--EMBLEMAT-E1-->.*?<!--/EMBLEMAT-E1-->",
                      lambda m: "<!--EMBLEMAT-E1-->" + e1 + "<!--/EMBLEMAT-E1-->", html, flags=re.S)
    p.write_text(html, encoding="utf-8")
    print(p, "wstawiono" if n else "BRAK ZNACZNIKA")
