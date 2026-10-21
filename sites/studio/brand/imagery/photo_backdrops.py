"""Build the photo backdrop masters from Andrew's originals on Flickr.

Each photo is cropped to 16:9, scaled to 5120 x 2880, and graded toward the
palette: nearly colourless, toned from slate to Soft White, low contrast with
no true blacks, and a little haze toward the sky. A second copy adds a soft
centre lift toward Soft White, for a logo to sit on.

  photos/<name>.jpg            graded
  photos/<name>-vignette.jpg   graded, with the centre lift

usage: python3 brand/imagery/photo_backdrops.py <download dir>   (from sites/studio)
needs: numpy, Pillow"""
import pathlib, subprocess, sys
import numpy as np
from PIL import Image

HERE = pathlib.Path(__file__).resolve().parent
W, H = 5120, 2880
SOFT_WHITE = np.array([0.973, 0.98, 0.988], np.float32)

# name: (original on Flickr, vertical offset of the 16:9 window as a fraction of the height)
PHOTOS = {
    "grinnell-trail": ("https://live.staticflickr.com/65535/51806978445_9eed3104cb_o.jpg", 0.10),
    "blue-ridge":     ("https://live.staticflickr.com/65535/52460143426_9b24593f3d_o.jpg", 0.12),
    "lake-mcdonald":  ("https://live.staticflickr.com/65535/52633885111_d2f8709a1f_o.jpg", 0.03),
}

def grade(a, lift=0.30, span=0.68, keep=0.08):
    L = 0.2126 * a[..., 0] + 0.7152 * a[..., 1] + 0.0722 * a[..., 2]
    L = lift + span * L                                   # low contrast, no true blacks
    y = np.linspace(0, 1, a.shape[0], dtype=np.float32)[:, None]
    L = L + (1 - L) * 0.25 * np.clip(1 - y * 1.6, 0, 1)   # haze toward the sky
    # slate -> steel -> cool gray -> soft white
    stops = np.array([[0.20, 0.25, 0.33], [0.39, 0.45, 0.55], [0.82, 0.85, 0.89], [0.97, 0.98, 0.99]], np.float32)
    pos = np.array([0.0, 0.35, 0.75, 1.0], np.float32)
    out = np.stack([np.interp(L, pos, stops[:, c]).astype(np.float32) for c in range(3)], -1)
    return out * (1 - keep) + a * keep                    # a trace of the original colour

def vignette(a, cx=0.5, cy=0.45, rx=0.42, ry=0.48, amt=0.55):
    """Soft centre lift toward Soft White: strongest behind the logo, gone by the edges."""
    h, w, _ = a.shape
    y = (np.arange(h, dtype=np.float32) / h - cy) / ry
    x = (np.arange(w, dtype=np.float32) / w - cx) / rx
    m = np.exp(-(y[:, None] ** 2 + x[None, :] ** 2) * 1.4) * amt
    return a * (1 - m[..., None]) + SOFT_WHITE * m[..., None]

def save(a, path, icc):
    Image.fromarray((np.clip(a, 0, 1) * 255 + 0.5).astype("uint8")).save(path, quality=92, icc_profile=icc)

if __name__ == "__main__":
    cache = pathlib.Path(sys.argv[1]); cache.mkdir(parents=True, exist_ok=True)
    out = HERE / "photos"; out.mkdir(exist_ok=True)
    for name, (url, off) in PHOTOS.items():
        src = cache / f"{name}-original.jpg"
        if not src.exists():
            subprocess.run(["curl", "-sfL", "-A", "Mozilla/5.0", "-o", str(src), url], check=True)
        im = Image.open(src)
        icc = im.info.get("icc_profile")
        im = im.convert("RGB")
        w, h = im.size
        th = round(w * 9 / 16)
        top = min(round(h * off), h - th)
        im = im.crop((0, top, w, top + th)).resize((W, H), Image.LANCZOS)
        g = grade(np.asarray(im, dtype=np.float32) / 255)
        save(g, out / f"{name}.jpg", icc)
        save(vignette(g), out / f"{name}-vignette.jpg", icc)
        print(name)
