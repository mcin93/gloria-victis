"""Wstawia emblemat z assets/emblemat-symbol.svg w miejsca znaczników w HTML (można odpalać wielokrotnie)."""
import re, sys
from pathlib import Path

root = Path(__file__).resolve().parent.parent
symbol = (root / "assets" / "emblemat-symbol.svg").read_text(encoding="utf-8")
inner = re.search(r"<symbol[^>]*>(.*)</symbol>", symbol, re.S).group(1)
for name in sys.argv[1:]:
    p = Path(name)
    html = p.read_text(encoding="utf-8")
    for tag, content in (("EMBLEMAT-SYMBOL", symbol), ("EMBLEMAT-G", inner)):
        html = re.sub(rf"<!--{tag}-->(.*?<!--/{tag}-->)?", lambda m: f"<!--{tag}-->{content}<!--/{tag}-->", html, flags=re.S)
    p.write_text(html, encoding="utf-8")
    print("ok", p)
