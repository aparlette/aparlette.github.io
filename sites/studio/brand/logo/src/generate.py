"""Generate Parlette Studios mark + lockup as SVG built from exact primitives.
Pieces overlap; VectorCraft's Pathfinder unites them afterwards."""
import math, sys

NAVY, STEEL = "#0F1720", "#64748B"

def f(v): return f"{v:.3f}".rstrip("0").rstrip(".")

def pt(cx, cy, r, a):
    a = math.radians(a)
    return cx + r * math.cos(a), cy + r * math.sin(a)

def sector(cx, cy, ri, ro, a0, a1):
    """Annular sector, angles in degrees (SVG, y down), a0 < a1 clockwise."""
    large = 1 if (a1 - a0) > 180 else 0
    x0, y0 = pt(cx, cy, ro, a0); x1, y1 = pt(cx, cy, ro, a1)
    x2, y2 = pt(cx, cy, ri, a1); x3, y3 = pt(cx, cy, ri, a0)
    return (f"M{f(x0)} {f(y0)} A{f(ro)} {f(ro)} 0 {large} 1 {f(x1)} {f(y1)} "
            f"L{f(x2)} {f(y2)} A{f(ri)} {f(ri)} 0 {large} 0 {f(x3)} {f(y3)} Z")

def poly(*pts):
    return "M" + " L".join(f"{f(x)} {f(y)}" for x, y in pts) + " Z"

def rect(x0, y0, x1, y1):
    return poly((x0, y0), (x1, y0), (x1, y1), (x0, y1))

# ---------------------------------------------------------------- the mark
LIGHT_STEEL = "#94A3B8"   # stands in for Steel on dark backgrounds

def ring_blade(cx, cy, ri, ro, start, end):
    """Ring segment from start to end, each an (inner, outer) angle pair in degrees
    (clockwise). Different inner and outer angles give a slanted end."""
    (si, so), (ei, eo) = start, end
    x0, y0 = pt(cx, cy, ro, so); x1, y1 = pt(cx, cy, ro, eo)
    x2, y2 = pt(cx, cy, ri, ei); x3, y3 = pt(cx, cy, ri, si)
    lo = 1 if eo - so > 180 else 0; li = 1 if ei - si > 180 else 0
    return (f"M{f(x0)} {f(y0)} A{f(ro)} {f(ro)} 0 {lo} 1 {f(x1)} {f(y1)} "
            f"L{f(x2)} {f(y2)} A{f(ri)} {f(ri)} 0 {li} 0 {f(x3)} {f(y3)} Z")

def blade_cut(a, r, side):
    """Angle where one edge of the aperture cut centred at mid-ring angle `a` meets
    radius r. Cuts are tangent to a circle of radius TAN, like an iris's blade
    edges; side -1 is the edge before the cut, +1 the edge after."""
    rm = (RI + RO) / 2
    phi = a - math.degrees(math.acos(TAN / rm))
    return phi + math.degrees(math.acos((TAN - side * CUT / 2) / r))

def on_slope(x0, y0, r, lo, hi):
    """Angle in [lo, hi] where the slope-K line through (x0, y0) meets radius r."""
    def g(t):
        x, y = pt(CX, CY, r, t)
        return (x - x0) - K * (y - y0)
    for _ in range(60):
        m = (lo + hi) / 2
        if (g(lo) > 0) == (g(m) > 0): lo = m
        else: hi = m
    return (lo + hi) / 2

# Construction, in mark units (y down). Everything derives from these.
W = 11          # navy weight: stem, bars, bowl
T = 7           # ring weight
G = 6           # gap between the P and the ring
CUT = 3.5       # width of the aperture cuts
SX = 7          # stem left
TOP = 16        # top of the P
BASE = 88       # baseline
R = 18          # bowl outer radius
CX, CY = 42, TOP + R
RI, RO = R + G, R + G + T
TAN = R         # the cuts run tangent to the bowl, as iris blades do to the opening
CUTS = (-50, -5, 40)  # mid-ring angles of the cuts
K = 0.66        # run per unit rise of every diagonal in the mark
LEAD_X = SX - K * (TOP - (CY - RO))      # lead-in bar's tip, on the line from the P's corner
MARK_BOX = (LEAD_X, CY - RO, CX + RO, BASE)   # x0, y0, x1, y1

def mark_parts():
    """[(path, colour-role)]: 'navy' is the P, 'steel' the aperture ring."""
    sr = SX + W                       # stem right
    bot_i, bot_o = CY + R - W, CY + R # bowl bottom bar, inner/outer edge
    fold = CX - 5                     # where the bowl turns into the fold
    parts = [
        # P: stem, top bar, bowl, return bar
        (rect(SX, TOP, sr, BASE), "navy"),
        (rect(SX, TOP, CX, TOP + W), "navy"),
        (sector(CX, CY, R - W, R, -90, 90), "navy"),
        (rect(fold, bot_i, CX + 0.5, bot_o), "navy"),
        # the fold: the bowl's end, turned under, cut on slope K
        (poly((fold - 8, bot_i), (fold, bot_i), (fold, bot_o),
              (fold - 8 + K * W, bot_o)), "navy"),
    ]
    # hidden A: apex G below the fold, legs on slope K, notch parallel to them
    ax, ay = sr + 8, bot_o + G
    left_y = ay + (ax - sr) / K               # left diagonal meets the stem
    right_x = CX                              # right leg drops vertically at the bowl's centre line
    right_y = ay + (right_x - ax) / K
    nb_r = 2 * ax - sr                        # symmetric notch about the apex
    n_apex_y = BASE - (ax - sr) / K
    parts.append((poly((sr - 1, left_y), (ax, ay), (right_x, right_y), (right_x, BASE),
                       (nb_r, BASE), (ax, n_apex_y), (sr, BASE), (sr - 1, BASE)), "navy"))
    # aperture ring. The lead-in bar's tip lies on the slope-K line through the P's
    # top-left corner; the ring ends on the fold's diagonal, carried on past the bowl.
    top, inner = CY - RO, CY - RI
    parts.append((poly((LEAD_X, top), (CX, top), (CX, inner), (SX - K * (TOP - inner), inner)), "steel"))
    end = (on_slope(fold - 8, bot_i, RI, 30, 150), on_slope(fold - 8, bot_i, RO, 30, 150))
    edges = [(-90.5, -90.5)]
    for a in CUTS:
        edges += [(blade_cut(a, RI, -1), blade_cut(a, RO, -1)), (blade_cut(a, RI, +1), blade_cut(a, RO, +1))]
    edges.append(end)
    for i in range(0, len(edges), 2):
        parts.append((ring_blade(CX, CY, RI, RO, edges[i], edges[i + 1]), "steel"))
    return parts

PALETTES = {
    "color":   {"navy": NAVY, "steel": STEEL},
    "reverse": {"navy": "#FFFFFF", "steel": LIGHT_STEEL},
}

def mark(ox=0, oy=0, s=1.0, palette="color"):
    pal = PALETTES[palette]
    return [(scale_path(d, s, ox, oy), pal[role]) for d, role in mark_parts()]

def scale_path(d, s, dx, dy):
    import re
    toks = re.findall(r"[MLAZ]|-?[\d.]+", d)
    out, i, cmd = [], 0, None
    while i < len(toks):
        t = toks[i]
        if t in "MLAZ":
            cmd = t; out.append(t); i += 1
            if t == "Z": continue
        if cmd in "ML":
            out.append(f"{f(float(toks[i]) * s + dx)} {f(float(toks[i+1]) * s + dy)}"); i += 2
        elif cmd == "A":
            a = toks[i:i + 7]
            out.append(f"{f(float(a[0]) * s)} {f(float(a[1]) * s)} {a[2]} {a[3]} {a[4]} "
                       f"{f(float(a[5]) * s + dx)} {f(float(a[6]) * s + dy)}"); i += 7
    return " ".join(out)


# ------------------------------------------------------------ letterforms
# Geometric monoline caps built from exact pieces. Cap height H, weight w.
def letters(H, w):
    h = w / 2
    def stroke_line(x0, y0, x1, y1):
        dx, dy = x1 - x0, y1 - y0; L = math.hypot(dx, dy)
        nx, ny = -dy / L * h, dx / L * h
        return poly((x0 + nx, y0 + ny), (x1 + nx, y1 + ny), (x1 - nx, y1 - ny), (x0 - nx, y0 - ny))
    def leg(xt, yt, xb, yb):
        """Slanted leg with horizontal ends of horizontal width w*k."""
        ang = math.atan2(yb - yt, xb - xt)
        hw = h / abs(math.sin(ang))
        return poly((xt - hw, yt), (xt + hw, yt), (xb + hw, yb), (xb - hw, yb))
    G = {}
    # P
    rb = (H * 0.56 - w) / 2 + h            # bowl centreline radius
    def bowl(x0, xb):
        cy = h + rb
        return [rect(x0, 0, xb, w), rect(x0, 2 * rb, xb, 2 * rb + w),
                sector(xb, cy, rb - h, rb + h, -90, 90)]
    pw = H * 0.62
    xb = pw - rb - h
    G["P"] = (pw, [rect(0, 0, w, H)] + bowl(0, xb))
    # R = P + leg
    G["R"] = (pw + H * 0.02, [rect(0, 0, w, H)] + bowl(0, xb) +
              [leg(xb - w * 0.2, 2 * rb + w * 0.5, pw + H * 0.02 - h * 1.2, H)])
    # A as Λ (no crossbar), pointed apex
    aw = H * 0.78
    apex = aw / 2
    sl = math.atan2(H, apex)
    hw = h / math.sin(sl)
    G["A"] = (aw, [poly((0, H), (apex, 0), (aw, H), (aw - 2 * hw, H), (apex, H * 2 * hw / apex), (2 * hw, H))])
    # L, E, T, I
    G["L"] = (H * 0.5, [rect(0, 0, w, H), rect(0, H - w, H * 0.5, H)])
    ew = H * 0.52
    G["E"] = (ew, [rect(0, 0, w, H), rect(0, 0, ew, w), rect(0, (H - w) / 2, ew * 0.92, (H + w) / 2), rect(0, H - w, ew, H)])
    tw = H * 0.6
    G["T"] = (tw, [rect(0, 0, tw, w), rect((tw - w) / 2, 0, (tw + w) / 2, H)])
    G["I"] = (w, [rect(0, 0, w, H)])
    # O
    r = H / 2 - h
    G["O"] = (H, [sector(H / 2, H / 2, r - h, r + h, -90, 89.99), sector(H / 2, H / 2, r - h, r + h, 89.99, 269.98)])
    # D
    dw = H * 0.86
    rd = H / 2 - h
    xd = dw - rd - h
    G["D"] = (dw, [rect(0, 0, w, H), rect(0, 0, xd, w), rect(0, H - w, xd, H),
                   sector(xd, H / 2, rd - h, rd + h, -90, 90)])
    # U
    uw = H * 0.78
    ru = uw / 2 - h
    G["U"] = (uw, [rect(0, 0, w, H - uw / 2), rect(uw - w, 0, uw, H - uw / 2),
                   sector(uw / 2, H - uw / 2, ru - h, ru + h, 0, 180)])
    # S: two stacked arcs, lower slightly larger
    ru_, rl = (H - w) * 0.475 / 2, (H - w) * 0.525 / 2
    cx = h + rl
    cu, cl = h + ru_, H - h - rl
    G["S"] = (2 * rl + w, [sector(cx, cu, ru_ - h, ru_ + h, 90, 335),
                           sector(cx, cl, rl - h, rl + h, -90, 155)])
    return G

def word(text, x, y, H, w, track, fill):
    G = letters(H, w)
    out = []
    for ch in text:
        gw, parts = G[ch]
        for d in parts:
            out.append((translate(d, x, y), fill))
        x += gw + track
    return out, x - track

def translate(d, dx, dy):
    import re
    toks = re.findall(r"[MLAZ]|-?[\d.]+", d)
    out, i, cmd = [], 0, None
    while i < len(toks):
        t = toks[i]
        if t in "MLAZ":
            cmd = t; out.append(t); i += 1
            if t == "Z": continue
        if cmd in "ML":
            out.append(f"{f(float(toks[i]) + dx)} {f(float(toks[i+1]) + dy)}"); i += 2
        elif cmd == "A":
            a = toks[i:i + 7]
            out.append(" ".join(a[:5]) + f" {f(float(a[5]) + dx)} {f(float(a[6]) + dy)}"); i += 7
    return " ".join(out)

def rotate(d, deg, ox, oy, dx, dy):
    """Rotate path d by deg (clockwise, y down) about (ox, oy), then move it so
    (ox, oy) lands on (dx, dy). Arcs here are circular, so only their end points move."""
    import re
    c, sn = math.cos(math.radians(deg)), math.sin(math.radians(deg))
    def p(x, y):
        x, y = float(x) - ox, float(y) - oy
        return f"{f(x * c - y * sn + dx)} {f(x * sn + y * c + dy)}"
    toks = re.findall(r"[MLAZ]|-?[\d.]+", d)
    out, i, cmd = [], 0, None
    while i < len(toks):
        t = toks[i]
        if t in "MLAZ":
            cmd = t; out.append(t); i += 1
            if t == "Z": continue
        if cmd in "ML":
            out.append(p(toks[i], toks[i + 1])); i += 2
        elif cmd == "A":
            a = toks[i:i + 7]
            out.append(" ".join(a[:5]) + " " + p(a[5], a[6])); i += 7
    return " ".join(out)

def arc_word(text, cx, cy, r, H, w, track, fill, bottom=False):
    """Set text around a circle, centred on the top (or bottom) of it. Letters
    stand on radius r with their feet toward the centre on top; on the bottom
    they hang from r, still reading left to right."""
    G = letters(H, w)
    rm = r + H / 2                                        # spacing measured mid-cap
    widths = [G[ch][0] for ch in text]
    total = (sum(widths) + track * (len(text) - 1)) / rm  # radians
    out, a = [], -total / 2
    for ch, gw in zip(text, widths):
        mid = math.degrees(a + gw / 2 / rm)
        for d in G[ch][1]:
            if bottom:   # baseline on the outside: radius r + H
                x, y = cx + (r + H) * math.sin(math.radians(mid)), cy + (r + H) * math.cos(math.radians(mid))
                out.append((rotate(d, -mid, gw / 2, H, x, y), fill))
            else:        # baseline on the inside: radius r
                x, y = cx + r * math.sin(math.radians(mid)), cy - r * math.cos(math.radians(mid))
                out.append((rotate(d, mid, gw / 2, H, x, y), fill))
        a += (gw + track) / rm
    return out

def ring(cx, cy, ri, ro, fill):
    return [(sector(cx, cy, ri, ro, -90, 89.99), fill), (sector(cx, cy, ri, ro, 89.99, 269.98), fill)]

def dot(cx, cy, r, fill):
    return (f"M{f(cx - r)} {f(cy)} A{f(r)} {f(r)} 0 1 1 {f(cx + r)} {f(cy)} "
            f"A{f(r)} {f(r)} 0 1 1 {f(cx - r)} {f(cy)} Z", fill)

def badge():
    """Circle badge, 400 units across: a navy rim, PARLETTE over the top and
    STUDIOS under the bottom between two steel dots, a steel hairline, and the
    mark in the middle."""
    C, RIM, RW = 200, 200, 5            # centre, rim outer radius, rim weight
    H, w = 30, 4.6                      # letter height and weight (wordmark proportions)
    band_o = RIM - RW - 15              # caps reach out to here
    band_i = band_o - H                 # and stand on / hang from here
    out = ring(C, C, RIM - RW, RIM, NAVY)
    out += arc_word("PARLETTE", C, C, band_i, H, w, 24, NAVY)
    out += arc_word("STUDIOS", C, C, band_i, H, w, 24, STEEL, bottom=True)
    rm = band_i + H / 2
    out += [dot(C - rm, C, 4, STEEL), dot(C + rm, C, 4, STEEL)]
    hair = band_i - 14
    out += ring(C, C, hair - 2, hair, STEEL)
    # the mark, centred on its own box inside the hairline
    x0, y0, x1, y1 = MARK_BOX
    s = (hair - 16) * 2 / math.hypot(x1 - x0, y1 - y0)
    out += mark(C - (x0 + x1) / 2 * s, C - (y0 + y1) / 2 * s, s)
    return out

def svg(w, h, paths, bg=None):
    body = "".join(f'<path d="{d}" fill="{c}"/>' for d, c in paths)
    bgr = f'<rect width="{w}" height="{h}" fill="{bg}"/>' if bg else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {f(w)} {f(h)}" '
            f'width="{f(w)}" height="{f(h)}">{bgr}{body}</svg>\n')

if __name__ == "__main__":
    out = sys.argv[1]
    x0, y0, x1, y1 = MARK_BOX
    mw, mh = x1 - x0, y1 - y0
    open(f"{out}/mark.svg", "w").write(svg(mw, mh, mark(-x0, -y0)))
    # lockup
    Hc, wc, tr = 40, 6.2, 22
    _, endx = word("PARLETTE", 0, 0, Hc, wc, tr, NAVY)
    Hs, ws, trs = 17, 2.6, 26
    _, ends = word("STUDIOS", 0, 0, Hs, ws, trs, STEEL)
    pad, rl, gap = 4, 48, 16
    W_ = endx + 2 * pad + 40
    s_ = 120 / mh
    mk = mark((W_ - mw * s_) / 2 - x0 * s_, pad - y0 * s_, s_)
    ty = pad + mh * s_ + 26
    top, _ = word("PARLETTE", (W_ - endx) / 2, ty, Hc, wc, tr, NAVY)
    sy = ty + Hc + 22
    sub, _ = word("STUDIOS", (W_ - ends) / 2, sy, Hs, ws, trs, STEEL)
    rules = [(rect((W_ - ends) / 2 - gap - rl, sy + Hs / 2 - 1.3, (W_ - ends) / 2 - gap, sy + Hs / 2 + 1.3), STEEL),
             (rect((W_ + ends) / 2 + gap, sy + Hs / 2 - 1.3, (W_ + ends) / 2 + gap + rl, sy + Hs / 2 + 1.3), STEEL)]
    open(f"{out}/lockup.svg", "w").write(svg(W_, sy + Hs + pad, mk + top + sub + rules))
    # horizontal lockup: mark | PARLETTE over STUDIOS, for headers and wide spaces
    hm = 100 / mh                               # mark drawn 100 units tall
    mk = mark(-x0 * hm, -y0 * hm, hm)
    div_x = mw * hm + 22
    Hc, wc, tr = 34, 5.3, 19
    _, endx = word("PARLETTE", 0, 0, Hc, wc, tr, NAVY)
    Hs, ws, trs = 14.5, 2.2, 22
    _, ends = word("STUDIOS", 0, 0, Hs, ws, trs, STEEL)
    tx, sgap = div_x + 2 + 24, 16
    ty = (100 - (Hc + sgap + Hs)) / 2
    top, _ = word("PARLETTE", tx, ty, Hc, wc, tr, NAVY)
    sy = ty + Hc + sgap
    sx = tx + (endx - ends) / 2
    sub, _ = word("STUDIOS", sx, sy, Hs, ws, trs, STEEL)
    rh, rg = 1.1, 12
    rules = [(rect(tx, sy + Hs / 2 - rh, sx - rg, sy + Hs / 2 + rh), STEEL),
             (rect(sx + ends + rg, sy + Hs / 2 - rh, tx + endx, sy + Hs / 2 + rh), STEEL),
             (rect(div_x, 12, div_x + 2, 88), STEEL)]
    open(f"{out}/horizontal.svg", "w").write(svg(tx + endx, 100, mk + top + sub + rules))
    # circle badge: square by construction
    open(f"{out}/badge.svg", "w").write(svg(400, 400, badge()))
