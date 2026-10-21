"""Generuje emblemat Gloria Victis: wieniec laurowy (jak ONZ) wokół globu z siatki i węzłów sieci.
Wynik: assets/emblemat.svg (samodzielny, stałe kolory) i assets/emblemat-symbol.svg (<symbol> do wklejenia w HTML,
kolory przez zmienne CSS --gv-laur, --gv-glob, --gv-wezel)."""
import math
from pathlib import Path

C, R_STEM = 120, 88
GLOB_R = 60
PAIRS = 9

def pt(r, deg):
    a = math.radians(deg)
    return C + r * math.cos(a), C + r * math.sin(a)

def leaf(x, y, direction, length, width):
    L, w = length, width
    d = f"M0 0Q{L*0.45:.1f} {-w:.1f} {L:.1f} 0Q{L*0.45:.1f} {w:.1f} 0 0Z"
    return f'<path d="{d}" transform="translate({x:.1f} {y:.1f}) rotate({direction:.1f})"/>'

def branch(mirror):
    """Gałąź lewa; mirror=True odbija ją na prawą stronę."""
    leaves = []
    t0, t1 = 114, 242
    for i in range(PAIRS):
        t = i / (PAIRS - 1)
        th = t0 + t * (t1 - t0)
        tangent = th + 90
        L = 25 - 9 * t
        x, y = pt(R_STEM, th)
        leaves.append((i * 2, x, y, tangent - 30, L, L * 0.34))
        th2 = th + (t1 - t0) / (PAIRS - 1) / 2
        x2, y2 = pt(R_STEM, th2)
        leaves.append((i * 2 + 1, x2, y2, th2 + 90 + 34, L * 0.82, L * 0.82 * 0.34))
    tx, ty = pt(R_STEM, 250)
    leaves.append((PAIRS * 2, tx, ty, 250 + 90 - 4, 15, 5))
    out = []
    for idx, x, y, ang, L, w in leaves:
        if mirror:
            x, ang = 2 * C - x, 180 - ang
        out.append(leaf(x, y, ang, L, w).replace("<path ", f'<path style="--i:{idx}" ', 1))
    # łodyga: łuk od czubka w dół, potem zejście pod globem i skrzyżowanie z drugą gałęzią
    a, b = pt(R_STEM, 250), pt(R_STEM, 108)
    k1, end = (C - 4, C + R_STEM + 6), (C + 24, C + R_STEM + 14)
    if mirror:
        a, b, k1, end = [(2 * C - q[0], q[1]) for q in (a, b, k1, end)]
        sweep = 1
    else:
        sweep = 0
    stem = (f'<path class="gv-lodyga" d="M{a[0]:.1f} {a[1]:.1f}A{R_STEM} {R_STEM} 0 0 {sweep} {b[0]:.1f} {b[1]:.1f}'
            f'Q{k1[0]:.1f} {k1[1]:.1f} {end[0]:.1f} {end[1]:.1f}"/>')
    return stem, out

def globe():
    parts = []
    for r in (20, 40, GLOB_R):
        parts.append(f'<circle cx="{C}" cy="{C}" r="{r}"/>')
    for k in range(12):
        x, y = pt(GLOB_R, k * 30)
        parts.append(f'<path d="M{C} {C}L{x:.1f} {y:.1f}"/>')
    # hub w środku, trzy węzły pośrednie, sześciokąt na krawędzi globu (sieć + cząsteczka)
    nodes = {"o": (0, 0), "a": (40, 270), "b": (40, 30), "c": (40, 150),
             "1": (60, 240), "2": (60, 300), "3": (60, 0), "4": (60, 60), "5": (60, 120), "6": (60, 180)}
    edges = ["oa", "ob", "oc", "a1", "a2", "b3", "b4", "c5", "c6", "12", "23", "34", "45", "56", "61"]
    P = {k: pt(r, a) for k, (r, a) in nodes.items()}
    lines = [f'<path d="M{P[u][0]:.1f} {P[u][1]:.1f}L{P[v][0]:.1f} {P[v][1]:.1f}"/>' for u, v in edges]
    dots = [f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{7 if k == "o" else 5 if k in "abc" else 4.4}"/>' for k, (x, y) in P.items()]
    return parts, lines, dots

def build(colors=None):
    lstem, lleaves = branch(False)
    rstem, rleaves = branch(True)
    grid, lines, dots = globe()
    if colors:
        laur, glob, wezel = colors
    else:
        laur, glob, wezel = "var(--gv-laur, #b8954a)", "var(--gv-glob, #1d3557)", "var(--gv-wezel, #1d3557)"
    return (
        f'<g class="gv-wieniec" fill="{laur}" stroke="{laur}" stroke-width="0">'
        f'<g fill="none" stroke-width="2.6" stroke-linecap="round">{lstem}{rstem}</g>'
        f'<g class="gv-liscie">{"".join(lleaves + rleaves)}</g></g>'
        f'<g class="gv-glob" fill="none" stroke="{glob}" stroke-width="1.2" opacity=".45">{"".join(grid)}</g>'
        f'<g class="gv-siec" fill="none" stroke="{wezel}" stroke-width="2.4" stroke-linecap="round">{"".join(lines)}</g>'
        f'<g class="gv-wezly" fill="{wezel}">{"".join(dots)}</g>'
    )

if __name__ == "__main__":
  root = Path(__file__).resolve().parent.parent / "assets"
  (root / "emblemat-symbol.svg").write_text(
    f'<symbol id="gv-emblemat" viewBox="0 0 240 240">{build()}</symbol>', encoding="utf-8")
  (root / "emblemat.svg").write_text(
    f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 240 240">{build(("#b8954a", "#1d3557", "#1d3557"))}</svg>',
    encoding="utf-8")
  print("ok", len(build()), "znaków")
