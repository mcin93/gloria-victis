"""Pobiera fonty z fontsource (jsdelivr), zostawia podzbiory latin + latin-ext, hostuje lokalnie."""
import re, sys, urllib.request
from pathlib import Path

FONTY = [  # (pakiet npm, plik css)
    ("@fontsource-variable/newsreader", "index.css"),
    ("@fontsource-variable/newsreader", "wght-italic.css"),
    ("@fontsource-variable/public-sans", "index.css"),
    ("@fontsource/marcellus", "400.css"),
    ("@fontsource-variable/source-sans-3", "index.css"),
    ("@fontsource-variable/schibsted-grotesk", "index.css"),
]
OUT = Path(sys.argv[1])
OUT.mkdir(parents=True, exist_ok=True)
css_out = []
for pkg, css in FONTY:
    base = f"https://cdn.jsdelivr.net/npm/{pkg}@5/"
    text = urllib.request.urlopen(base + css).read().decode()
    for block in re.findall(r"/\*[^*]*\*/\s*@font-face\s*\{[^}]*\}", text):
        if not re.search(r"/\*\s*[\w-]*-(latin|latin-ext)-", block):
            continue
        for rel in re.findall(r"url\(\./files/([^)]+\.woff2)\)", block):
            dst = OUT / rel
            if not dst.exists():
                dst.write_bytes(urllib.request.urlopen(base + "files/" + rel).read())
        block = re.sub(r"url\(\./files/([^)]+\.woff2)\)", r"url(./\1)", block)
        block = re.sub(r",\s*url\([^)]+\.woff\)\s*format\('woff'\)", "", block)
        css_out.append(block)
(OUT / "fonts.css").write_text("\n".join(css_out), encoding="utf-8")
print(len(css_out), "bloków @font-face")
