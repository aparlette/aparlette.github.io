"""Export padded PNGs from the tight SVG masters.

The SVGs are trimmed to the art; the PNGs sit the art centred on a standard canvas
with padding, transparent background:
  mark   -> 1024 x 1024
  lockup -> 1200 x 800 (3:2, close to the lockup's own proportions)
  horizontal -> 1600 x 400 (4:1)
  badge  -> 1024 x 1024

usage: python3 export_png.py <logo dir> <vectorcraft-cli>"""
import pathlib, re, subprocess, sys, tempfile

CANVAS = {"mark": (1024, 1024), "badge": (1024, 1024), "lockup": (1200, 800), "horizontal": (1600, 400)}
PAD = 0.08  # of the canvas's shorter side

def export(svg_path, out_png, vc):
    kind = next(k for k in ("horizontal", "lockup", "badge", "mark") if k in svg_path.name)
    cw, ch = CANVAS[kind]
    src = svg_path.read_text()
    aw, ah = map(float, re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', src).groups())
    pad = PAD * min(cw, ch)
    s = min((cw - 2 * pad) / aw, (ch - 2 * pad) / ah)
    tx, ty = (cw - aw * s) / 2, (ch - ah * s) / 2
    paths = "".join(re.findall(r"<path[^>]*/>", src))
    wrapped = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{cw}" height="{ch}" '
               f'viewBox="0 0 {cw} {ch}"><g transform="translate({tx:.3f} {ty:.3f}) '
               f'scale({s:.5f})">{paths}</g></svg>')
    with tempfile.NamedTemporaryFile("w", suffix=".svg") as tmp:
        tmp.write(wrapped); tmp.flush()
        subprocess.run([vc, "convert", tmp.name, str(out_png)], check=True,
                       stdout=subprocess.DEVNULL)

if __name__ == "__main__":
    logo, vc = pathlib.Path(sys.argv[1]), sys.argv[2]
    (logo / "png").mkdir(exist_ok=True)
    for svg in sorted(logo.glob("parlette-studios-*.svg")):
        export(svg, logo / "png" / f"{svg.stem}.png", vc)
        print(svg.stem)
