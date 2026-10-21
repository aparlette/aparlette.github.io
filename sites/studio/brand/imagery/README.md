# Decorative imagery

These are AI-generated illustrations, used on the site only as decoration
(backdrops, the social card). They are never presented as photography.
Andrew's photographs come from his own archive.

| File | Used for | Generated with |
|---|---|---|
| `hero-fog.png` | Home page hero backdrop (`assets/img/hero-backdrop.jpg`) | Juggernaut XL, prompt `hero-fog`, seed 23 |
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
