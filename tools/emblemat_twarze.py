"""Warianty środka emblematu: twarz w profilu (jak na rzymskiej monecie) w kilku technikach + monogram.
Wieniec bierze z emblemat.py. Wynik: assets/emblemat-warianty.svg (zestaw <symbol id="gv-e1".."gv-e4">).
Kolory przez zmienne CSS: --gv-laur (wieniec), --gv-twarz (twarz), --gv-linia (linie skanu), --gv-tlo (tło)."""
import math, random
from pathlib import Path
from scipy.spatial import Delaunay
from emblemat import branch, C

# profil głowy zwrócony w prawo, współrzędne w pudełku ok. 100 x 125
# proporcje wg metody Loomisa: linia brwi y=42, podstawa nosa y=72, broda y=102
PROFIL = [(48, 2), (62, 3.5), (73, 8), (81, 16), (85, 26), (86.5, 35), (88, 41), (86.5, 45), (87.5, 48), (90.5, 55),
          (94.5, 63), (98, 69.5), (96.5, 72), (91, 73), (88, 74), (88.5, 77), (90, 79.5), (88, 81.5), (89.5, 84),
          (86.5, 87.5), (86.5, 90), (89.5, 95), (89, 100), (84.5, 103), (76, 104), (68, 105.5),
          (65, 112), (64.5, 116), (62, 124), (58, 140), (14, 140), (17, 118), (21, 96), (19, 86), (13, 74),
          (8.5, 58), (8, 42), (11, 27), (19, 15), (31, 6)]
LANDMARKS = {"czolo": (80, 20), "skron": (66, 40), "brew": (88, 41), "oko": (79, 49), "nos": (98, 69.5),
             "nozdrze": (86, 69), "warga_g": (90, 79.5), "warga_d": (89, 83.5), "broda": (89.5, 95),
             "zuchwa": (53, 90), "ucho": (50, 58), "policzek": (74, 62), "ciemie": (38, 8), "kark": (22, 92)}
MESH = ["czolo-skron", "czolo-brew", "skron-oko", "brew-oko", "oko-nos", "oko-policzek", "policzek-nozdrze",
        "nos-nozdrze", "nozdrze-warga_g", "warga_g-warga_d", "warga_d-broda", "broda-zuchwa", "zuchwa-policzek",
        "zuchwa-ucho", "ucho-policzek", "ucho-skron", "skron-ciemie", "ciemie-czolo", "ucho-kark", "kark-zuchwa",
        "ucho-ciemie", "policzek-warga_d"]
TX, TY = 68, 58          # przesunięcie pudełka profilu w układ emblematu 240 x 240
CLIP_R = 63              # popiersie ucięte okręgiem jak na monecie

def T(p):
    return p[0] + TX, p[1] + TY

def catmull(points, closed=True):
    """Gładka ścieżka SVG przez punkty (Catmull-Rom -> Bezier)."""
    P = [T(p) for p in points]
    n = len(P)
    d = f"M{P[0][0]:.1f} {P[0][1]:.1f}"
    for i in range(n if closed else n - 1):
        p0, p1, p2, p3 = P[i - 1], P[i], P[(i + 1) % n], P[(i + 2) % n]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        d += f"C{c1[0]:.1f} {c1[1]:.1f} {c2[0]:.1f} {c2[1]:.1f} {p2[0]:.1f} {p2[1]:.1f}"
    return d + ("Z" if closed else "")

def sample_outline(step=3.0):
    """Gęste próbkowanie konturu (odcinki), w układzie emblematu."""
    P = [T(p) for p in PROFIL]
    out = []
    for i in range(len(P)):
        a, b = P[i], P[(i + 1) % len(P)]
        L = math.dist(a, b)
        k = max(1, int(L / step))
        out += [(a[0] + (b[0] - a[0]) * j / k, a[1] + (b[1] - a[1]) * j / k) for j in range(k)]
    return out

def inside(pt, poly):
    x, y = pt
    res = False
    for i in range(len(poly)):
        (x1, y1), (x2, y2) = poly[i], poly[i - 1]
        if (y1 > y) != (y2 > y) and x < (x2 - x1) * (y - y1) / (y2 - y1) + x1:
            res = not res
    return res

def in_coin(pt, margin=0):
    return math.dist(pt, (C, C)) <= CLIP_R - margin

def wieniec():
    lstem, lleaves = branch(False)
    rstem, rleaves = branch(True)
    return (f'<g fill="var(--gv-laur)" stroke="var(--gv-laur)" stroke-width="0">'
            f'<g fill="none" stroke-width="2.6" stroke-linecap="round">{lstem}{rstem}</g>'
            f'<g class="gv-liscie">{"".join(lleaves + rleaves)}</g></g>')

def defs(n):
    return (f'<defs><clipPath id="gv-moneta-{n}"><circle cx="{C}" cy="{C}" r="{CLIP_R}"/></clipPath>'
            f'<clipPath id="gv-glowa-{n}"><path d="{catmull(PROFIL)}"/></clipPath></defs>')

def obrecz():
    return f'<circle cx="{C}" cy="{C}" r="{CLIP_R + 4}" fill="none" stroke="var(--gv-laur)" stroke-width="1.4" opacity=".7"/>'

def wariant_skan(n):
    lines = "".join(f'<path d="M60 {y}H190"/>' for y in range(60, 190, 5))
    L = {k: T(v) for k, v in LANDMARKS.items()}
    mesh = "".join(f'<path d="M{L[a][0]:.1f} {L[a][1]:.1f}L{L[b][0]:.1f} {L[b][1]:.1f}"/>'
                   for a, b in (e.split("-") for e in MESH))
    na_konturze = {"brew", "nos", "warga_g", "warga_d", "broda", "ciemie"}
    dots = "".join(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{3.6 if k == "oko" else 1.6 if k in na_konturze else 2.4}"/>'
                   for k, (x, y) in L.items())
    wlosy = catmull([(81, 16), (74, 22), (69, 32), (62, 44), (57, 53)], closed=False)
    return (defs(n) + obrecz() +
            f'<g clip-path="url(#gv-moneta-{n})">'
            f'<g clip-path="url(#gv-glowa-{n})" stroke="var(--gv-linia)" stroke-width="1.1" opacity=".75">{lines}</g>'
            f'<path d="{catmull(PROFIL)}" fill="none" stroke="var(--gv-twarz)" stroke-width="2.2"/>'
            f'<path d="{wlosy}" fill="none" stroke="var(--gv-twarz)" stroke-width="1.6" stroke-linecap="round"/>'
            f'<g stroke="var(--gv-twarz)" stroke-width="1.2" opacity=".9">{mesh}</g>'
            f'<g fill="var(--gv-twarz)">{dots}</g></g>')

def wariant_lowpoly(n):
    rnd = random.Random(11)
    poly = sample_outline(2.0)
    pts = sample_outline(9.0)
    pts += [T(v) for v in LANDMARKS.values()]
    for gx in range(60, 190, 11):
        for gy in range(56, 200, 11):
            p = (gx + rnd.uniform(-3.5, 3.5), gy + rnd.uniform(-3.5, 3.5))
            if inside(p, poly) and min(math.dist(p, q) for q in pts) > 5:
                pts.append(p)
    tri = Delaunay(pts)
    facets = []
    xs = [p[0] for p in pts]
    xmin, xmax = min(xs), max(xs)
    for a, b, c in tri.simplices:
        A, B, Cc = pts[a], pts[b], pts[c]
        cx, cy = (A[0] + B[0] + Cc[0]) / 3, (A[1] + B[1] + Cc[1]) / 3
        if not inside((cx, cy), poly):
            continue
        shade = 0.22 + 0.62 * (cx - xmin) / (xmax - xmin) - 0.12 * (cy - 60) / 130 + rnd.uniform(-0.13, 0.13)
        shade = max(0.12, min(0.98, shade))
        facets.append(f'<path d="M{A[0]:.1f} {A[1]:.1f}L{B[0]:.1f} {B[1]:.1f}L{Cc[0]:.1f} {Cc[1]:.1f}Z" fill-opacity="{shade:.2f}"/>')
    return (defs(n) + obrecz() +
            f'<g clip-path="url(#gv-moneta-{n})"><g fill="var(--gv-twarz)" stroke="var(--gv-tlo)" stroke-width=".8" stroke-linejoin="round">'
            f'{"".join(facets)}</g></g>')

def wariant_obwod(n):
    """Przód twarzy pełny, tył głowy rozpada się w piksele i ścieżki obwodu."""
    rnd = random.Random(5)
    cut = lambda y: 44 + 8 * math.sin(y / 18)  # granica w układzie profilu
    step = 6
    solid = []
    for y in range(0, 130, step):
        x0 = cut(y)
        solid.append(f'<rect x="{x0 + TX:.1f}" y="{y + TY}" width="{100 - x0:.1f}" height="{step + 0.6}"/>')
    pix = []
    for y in range(0, 130, step):
        x0 = cut(y)
        for k in range(1, 5):
            if rnd.random() < 0.85 - k * 0.18:
                pix.append(f'<rect x="{x0 - k * step + TX + .6:.1f}" y="{y + TY + .6}" width="{step - 1.2}" height="{step - 1.2}"/>')
    traces, nodes = [], []
    for y in (14, 26, 38, 52, 66, 80, 94):
        x0 = cut(y) - 4 * step + TX
        yy = y + TY
        dx = rnd.choice([10, 14, 18])
        dy = rnd.choice([-8, 8])
        x1, y1 = x0 - dx, yy
        x2, y2 = x1 - abs(dy), yy + dy
        x3 = x2 - rnd.choice([6, 10, 14])
        traces.append(f'<path d="M{x0:.1f} {yy}L{x1:.1f} {y1}L{x2:.1f} {y2}L{x3:.1f} {y2}"/>')
        nodes.append(f'<circle cx="{x3:.1f}" cy="{y2}" r="2.6"/>')
    return (defs(n) + obrecz() +
            f'<g clip-path="url(#gv-moneta-{n})">'
            f'<g clip-path="url(#gv-glowa-{n})" fill="var(--gv-twarz)">{"".join(solid)}{"".join(pix)}'
            f'<g fill="none" stroke="var(--gv-linia)" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">{"".join(traces)}</g>'
            f'<g fill="var(--gv-linia)">{"".join(nodes)}</g></g>'
            f'<path d="{catmull(PROFIL)}" fill="none" stroke="var(--gv-twarz)" stroke-width="1.8"/></g>')

def wariant_monogram(n):
    return (obrecz() +
            f'<text x="{C}" y="{C + 25}" text-anchor="middle" font-family="Marcellus, serif" font-size="78" '
            f'letter-spacing="-2" fill="var(--gv-twarz)">GV</text>'
            f'<path d="M86 {C + 40}H154" stroke="var(--gv-laur)" stroke-width="1.6"/>'
            f'<g fill="var(--gv-laur)"><circle cx="{C}" cy="{C - 46}" r="3"/><circle cx="{C - 14}" cy="{C - 42}" r="2"/><circle cx="{C + 14}" cy="{C - 42}" r="2"/></g>')

if __name__ == "__main__":
    root = Path(__file__).resolve().parent.parent / "assets"
    w = wieniec()
    warianty = {1: wariant_skan, 2: wariant_lowpoly, 3: wariant_obwod, 4: wariant_monogram}
    symbols = "".join(f'<symbol id="gv-e{k}" viewBox="0 0 240 240">{w}{f(k)}</symbol>' for k, f in warianty.items())
    (root / "emblemat-warianty.svg").write_text(symbols, encoding="utf-8")
    print("ok", len(symbols))
