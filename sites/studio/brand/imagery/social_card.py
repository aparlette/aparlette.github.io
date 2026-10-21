"""Build the 1200 x 630 social card (assets/img/social.png): the dark-arc
illustration, darkened toward navy, with the reverse horizontal lockup on top.

usage: python3 brand/imagery/social_card.py [vectorcraft-cli]   (from sites/studio)"""
import io, pathlib, re, subprocess, sys, tempfile
from PIL import Image

VC = sys.argv[1] if len(sys.argv) > 1 else "/projects/external/ArtCraft/vectorcraft/target/release/vectorcraft-cli"
HERE = pathlib.Path(__file__).resolve().parent
SITE = HERE.parent.parent
W, H = 1200, 630
NAVY = (15, 23, 32)

def lockup_png(width):
    src = (SITE / "brand/logo/parlette-studios-horizontal-reverse.svg").read_text()
    vw = float(re.search(r'viewBox="0 0 ([\d.]+)', src).group(1))
    with tempfile.TemporaryDirectory() as d:
        out = pathlib.Path(d, "l.png")
        subprocess.run([VC, "convert", str(SITE / "brand/logo/parlette-studios-horizontal-reverse.svg"),
                        str(out), "--scale", str(width / vw)], check=True, stdout=subprocess.DEVNULL)
        return Image.open(io.BytesIO(out.read_bytes())).convert("RGBA")

bg = Image.open(HERE / "dark-arc.png").convert("RGB")
scale = max(W / bg.width, H / bg.height)
bg = bg.resize((round(bg.width * scale), round(bg.height * scale)), Image.LANCZOS)
left, top = (bg.width - W) // 2, (bg.height - H) // 2
bg = bg.crop((left, top, left + W, top + H))
card = Image.blend(bg, Image.new("RGB", (W, H), NAVY), 0.35).convert("RGBA")

logo = lockup_png(720)
card.alpha_composite(logo, ((W - logo.width) // 2, round(H * 0.4 - logo.height / 2)))
card.convert("RGB").save(SITE / "assets/img/social.png", optimize=True)
print("assets/img/social.png")
