"""Write the logo files the Studio site itself uses.

  assets/img/logo.svg      header logo: the horizontal lockup with its fills
                           replaced by classes, so CSS can recolour it for dark mode
  static/favicon.svg       navy tile with the reverse mark
  static/favicon-*.png, favicon.ico, apple-touch-icon.png, android-chrome-*.png
  static/site.webmanifest
  layouts/partials/studio/hero-drawing.html
                           the mark as a construction drawing for the home hero

usage: python3 site_assets.py <logo dir> <site dir> <vectorcraft-cli>"""
import io, json, pathlib, re, subprocess, sys, tempfile
from PIL import Image

NAVY, STEEL, LIGHT = "#0f1720", "#64748b", "#94a3b8"

def paths_of(svg):
    src = svg.read_text()
    w, h = map(float, re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', src).groups())
    return w, h, re.findall(r"<path[^>]*/>", src)

def header_logo(logo, site):
    w, h, paths = paths_of(logo / "parlette-studios-horizontal.svg")
    body = "".join(paths).replace(f'fill="{NAVY}"', 'class="ps-ink"').replace(f'fill="{STEEL}"', 'class="ps-steel"')
    out = site / "assets/img/logo.svg"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:g} {h:g}" '
                   f'class="ps-logo" aria-hidden="true" focusable="false">{body}</svg>\n')

def tile(logo, rounded, pad):
    """Navy square, 100 units, with the reverse mark centred inside `pad`."""
    w, h, paths = paths_of(logo / "parlette-studios-mark-reverse.svg")
    s = (100 - 2 * pad) / max(w, h)
    tx, ty = (100 - w * s) / 2, (100 - h * s) / 2
    rx = ' rx="22"' if rounded else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100" height="100">'
            f'<rect width="100" height="100"{rx} fill="{NAVY}"/>'
            f'<g transform="translate({tx:.3f} {ty:.3f}) scale({s:.5f})">{"".join(paths)}</g></svg>\n')

def render(svg_text, px, vc):
    with tempfile.TemporaryDirectory() as d:
        src, out = pathlib.Path(d, "in.svg"), pathlib.Path(d, "out.png")
        src.write_text(svg_text)
        subprocess.run([vc, "convert", str(src), str(out), "--scale", str(px / 100)],
                       check=True, stdout=subprocess.DEVNULL)
        return Image.open(io.BytesIO(out.read_bytes())).convert("RGBA")

def favicons(logo, site, vc):
    static = site / "static"
    static.mkdir(exist_ok=True)
    browser = tile(logo, rounded=True, pad=14)     # tabs: small, rounded
    app = tile(logo, rounded=False, pad=20)        # home screens round it themselves
    (static / "favicon.svg").write_text(browser)
    icons = {px: render(browser, px, vc) for px in (16, 32, 48)}
    icons[16].save(static / "favicon-16x16.png")
    icons[32].save(static / "favicon-32x32.png")
    icons[48].save(static / "favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)])
    render(app, 180, vc).save(static / "apple-touch-icon.png")
    for px in (192, 512):
        render(app, px, vc).save(static / f"android-chrome-{px}x{px}.png")
    (static / "site.webmanifest").write_text(json.dumps({
        "name": "Parlette Studios",
        "short_name": "Parlette Studios",
        "icons": [{"src": f"/android-chrome-{px}x{px}.png", "sizes": f"{px}x{px}",
                   "type": "image/png", "purpose": "any maskable"} for px in (192, 512)],
        "theme_color": NAVY,
        "background_color": NAVY,
        "display": "standalone",
    }, indent=2) + "\n")

def hero_drawing(logo, site):
    src = (logo / "parlette-studios-mark.svg").read_text()
    vb = re.search(r'viewBox="([^"]+)"', src).group(1)
    ink = re.search(rf'<path d="([^"]+)" fill="{NAVY}"', src).group(1)
    ring = re.search(rf'<path d="([^"]+)" fill="{STEEL}"', src).group(1)
    (site / "layouts/partials/studio/hero-drawing.html").write_text(
        "{{/* The mark as a construction drawing: the ring solid, the P traced in a\n"
        "     hairline. Written by brand/logo/src/site_assets.py; colour comes from\n"
        "     the parent through currentColor. */}}\n"
        f'<svg class="ps-hero__ring" viewBox="{vb}" aria-hidden="true" focusable="false">'
        f'<path d="{ring}" fill="currentColor"/>'
        f'<path d="{ink}" fill="none" stroke="currentColor" stroke-width="1" vector-effect="non-scaling-stroke"/>'
        "</svg>\n")

if __name__ == "__main__":
    logo, site, vc = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2]), sys.argv[3]
    header_logo(logo, site)
    favicons(logo, site, vc)
    hero_drawing(logo, site)
