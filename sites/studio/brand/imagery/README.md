# Imagery

## Photo backdrops

Andrew's own photographs, graded into the palette for use behind the logo or
words. `photos/` holds 5120 × 2880 masters, each plain and with a centre lift
toward Soft White (`-vignette`). The site makes its web sizes from them at
build time; `config/_default/module.toml` mounts `photos/` as `assets/photos/`.

| File | Photograph | Used for |
|---|---|---|
| `photos/grinnell-trail*.jpg` | [Overlook from Grinnell Trail, Glacier National Park](https://www.flickr.com/photos/aparlette/51806978445/) | Home page hero (the vignette version) |
| `photos/blue-ridge*.jpg` | [Blue Ridge Mountains](https://www.flickr.com/photos/aparlette/52460143426/) | Spare |
| `photos/lake-mcdonald*.jpg` | [Sunrise over Lake McDonald, Glacier National Park](https://www.flickr.com/photos/aparlette/52633885111/) | Spare |

`photo_backdrops.py` downloads the originals from Flickr and rebuilds all six
masters: crop, grade and vignette settings are in the script. It needs numpy
and Pillow.

```sh
python3 brand/imagery/photo_backdrops.py /tmp/originals
```

## AI-generated illustration

Used only as decoration. Never presented as photography.

| File | Used for | Generated with |
|---|---|---|
| `dark-arc.png` | Social card background (`assets/img/social.png`) | Juggernaut XL, prompt `dark-lines`, seed 11 |

All were rendered on pompom's ComfyUI with `comfy.py`, which holds the exact
prompts and settings: 30 steps, CFG 5, dpmpp_2m karras, with the negative prompt
in the script. To regenerate or make more:

```sh
python3 brand/imagery/comfy.py /tmp/out   # needs pompom:8188 reachable
python3 brand/imagery/social_card.py      # rebuilds assets/img/social.png
```

Prompting notes: keep to cool steel and slate tones with vast negative space,
and say "matte" and "high key" (or "deep midnight navy" for dark pieces).
Saturated skies and warm light fall outside the palette.
