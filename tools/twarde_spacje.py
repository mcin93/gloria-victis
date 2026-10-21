"""Wstawia twarde spacje między liczbą a jednostką, tylko w tekście (nie w atrybutach i nie w SVG).
Użycie: python tools/twarde_spacje.py wersja-b/index.html"""
import re
import sys
from pathlib import Path

NBSP = " "
JEDN = ("zł|mln|tys\\.|dni|dzień|osób|osoby|tygodni|tygodnie|tydzień|lat|lata|miesięcy|faktur|godziny|godzin|"
        "projekty|projektów|profesorów|specjalistów|doktorów|zakładach|patentów|publikacji|projektami")
WZOR_JEDN = re.compile(r"(\d) (" + JEDN + r")(?=[\s.,:;)<]|$)")
WZOR_TYS = re.compile(r"\b(\d)(\d{3})\b")


def popraw_tekst(t):
    t = WZOR_JEDN.sub(lambda m: m.group(1) + NBSP + m.group(2), t)
    t = t.replace("mln zł", "mln" + NBSP + "zł")
    # 1846 -> 1 846 (bez lat, np. 2019, 2021-2027)
    t = WZOR_TYS.sub(lambda m: m.group(0) if 1900 <= int(m.group(0)) <= 2100 and m.group(0) != "1900"
                     else m.group(1) + NBSP + m.group(2), t)
    return t


for name in sys.argv[1:]:
    p = Path(name)
    html = p.read_text(encoding="utf-8")
    przed = html.count(NBSP)
    # pomijamy wnętrze <svg>...</svg> i <script>...</script>
    czesci = re.split(r"(<svg.*?</svg>|<script.*?</script>)", html, flags=re.S)
    for i in range(0, len(czesci), 2):
        czesci[i] = re.sub(r">[^<]+<", lambda m: popraw_tekst(m.group(0)), czesci[i])
    html = "".join(czesci)
    p.write_text(html, encoding="utf-8")
    print(p, "twarde spacje:", przed, "->", html.count(NBSP))
