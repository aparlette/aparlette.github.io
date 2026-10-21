# Parlette Studios — brand guide

Parlette Studios is the name Andrew's photography and software projects go under. It is
a **sub-brand of the parlette.net sites**, not a separate company. It has its own mark,
colours and type so that project pages and photographs read as a coherent set, but it
stays part of the parlette.net network (the shared footer stays).

This folder is source material. `logo/` is also published at `/brand/logo/` (minus
`src/`) so the site's [brand page](https://studio.parlette.net/brand/) can show and offer
the files. That page is the visual version of this guide. The build scripts write the
logo files the site itself uses (header logo, favicons, hero drawing); see *Rebuilding
the logo*.

> **Parlette Studios is an independent creative studio for software, photography, and
> digital projects.**

## Personality

**Precise. Thoughtful. Creative. Understated. Capable.**

It should feel like a small studio run by someone who cares about craft. It should not
feel flashy, futuristic for its own sake, corporate, whimsical or aggressively "tech". The
same identity should look natural on a GitHub project page and in the corner of a
fine-art photograph.

## Logo

| File | Use |
|---|---|
| `logo/parlette-studios-lockup.svg` | **Primary logo.** Mark over PARLETTE / STUDIOS, on light backgrounds. |
| `logo/parlette-studios-horizontal.svg` | Mark beside PARLETTE / STUDIOS, divided by a thin rule. Headers and other wide, short spaces. |
| `logo/parlette-studios-badge.svg` | Circle badge: the mark inside a rim, PARLETTE set around the top and STUDIOS around the bottom. Square by construction. For round or square spaces where the name must travel with the mark: stickers, merch, profile images, a photography signature on a print's back. Not a replacement for the primary logo. At least 96 px across; below that, use the mark. |
| `logo/parlette-studios-mark.svg` | Mark only: avatars, favicons, watermarks, app publisher identity. |
| `…-reverse.svg` | On Midnight Navy or other dark backgrounds. White P and PARLETTE, Light Steel ring and STUDIOS. |
| `…-navy.svg`, `…-black.svg`, `…-white.svg` | One-colour versions for print, embossing, single-ink and watermark use. |

The SVGs are trimmed **tight** to the art: clear space is applied wherever the logo is
placed, never baked into the file. The PNGs in `logo/png/` are padded and ready to use:
transparent, art centred, about 8% padding. The mark is 1024 × 1024. The lockup is
1200 × 800 (3:2). The horizontal lockup is 1600 × 400 (4:1). The badge is 1024 × 1024. `logo/pdf/` has print masters.
`logo/src/` has the VectorCraft documents and `generate.py`, the script that builds the
geometry (see *Rebuilding the logo* below).

### The mark

A monogram drawn on a strict geometric construction. One stroke weight for the P, one
for the ring, one gap between them, and every diagonal on the same slope:

- **The P**: stem, top bar and bowl in Midnight Navy. The bowl doesn't close back onto
  the stem.
- **The fold**: the bowl's end turns under, cut on the mark's diagonal. It stands for layers
  and building in depth.
- **The hidden A**: below the bowl, the stem rises to a pointed apex, with a triangular
  counter cut from the baseline. It is an A for Andrew and an upward arrow for
  direction.
- **The aperture ring**: a thin Steel Blue band around the bowl, cut into four blades by
  three slanted gaps. Like the blade edges of a real iris, each cut is a straight line
  tangent to the opening, which here is the P's bowl, so the ring reads as an aperture
  without becoming a shutter icon.
- **One slope**: every diagonal in the mark runs on the same slope (`K`). The lead-in
  bar's tip sits on the line from the P's top-left corner. The fold, the A's legs and the
  ring's lower end are cut on that slope too, and the ring ends exactly where the fold's
  diagonal, carried on past the bowl, crosses it.

**Two colours, tied to the wordmark:** the P is Midnight Navy, the same as PARLETTE,
and the ring is Steel Blue, the same as STUDIOS. On dark backgrounds they become white
and Light Steel, again matching the reverse wordmark.

### The wordmark

PARLETTE and STUDIOS are **custom lettering**, not a typeset font: geometric monoline
capitals, with the A drawn as an open Λ that matches the hidden A in the mark. Never
retype the wordmark in a font. Use the artwork.

- PARLETTE: Midnight Navy, wide tracking.
- STUDIOS: Steel Blue, about 40% of the cap height of PARLETTE, very wide tracking,
  with a thin rule on each side.

### Rules

- **Clear space:** the width of the mark's stem (about a fifth of the mark's height) on
  every side of the mark or lockup.
- **Minimum size:** the lockup is at least 120 px wide on screen (30 mm in print). The
  mark is at least 24 px; below that (16 px favicons), use the one-colour mark.
- The tagline is **never** part of the logo.
- No gradients, shadows, bevels, outlines, metallic effects or rotation in the logo
  artwork. Those are presentation treatments for mockups, not the logo.
- Don't recolour the mark with the accent (Signal Blue). Use the files as supplied.
- Don't stretch it, rearrange the lockup or rebuild it from a font.

## Colour

| Role | Name | Hex | Use |
|---|---|---|---|
| Primary | Midnight Navy | `#0F1720` | Logo, headings, dark backgrounds |
| Secondary | Deep Slate | `#334155` | Secondary text, alternate dark surface |
| Midtone | Steel Blue | `#64748B` | The ring in the mark, STUDIOS, icons, supporting graphics |
| Midtone (reverse) | Light Steel | `#94A3B8` | Steel's stand-in on dark backgrounds, where `#64748B` lacks contrast |
| Light | Cool Gray | `#D1D5DB` | Borders, rules, subtle fills |
| Base | Soft White | `#F8FAFC` | Light backgrounds |
| Accent | Signal Blue | `#3B82F6` | Links, highlights, selected states. **Never in the logo.** |

The palette is mostly navy, slate and white. Signal Blue is the only saturated colour and
should be used sparingly, for things that need attention or a click. Steel Blue is for
graphics and large text only: on Soft White it falls short of WCAG AA contrast for body
text. Use Deep Slate for small secondary text.

## Typography

| Use | Typeface | Notes |
|---|---|---|
| Headings | **Archivo** 600 | Tracking −0.01em (−0.02em at hero size). |
| Labels | **Archivo** 600, capitals, width 112% | Tracking 0.24em: the STUDIOS treatment. Eyebrows, captions, table heads, buttons (0.16em). |
| Body, UI | **IBM Plex Sans** 400 | Normal tracking. Body text in Deep Slate. |
| Code | IBM Plex Mono | |

These are the parlette.net family's typefaces, so Studios reads as part of Andrew's
sites; its own identity comes from the logo and the palette. The brief originally named
Montserrat and Inter; they were compared side by side against these and replaced
(2026-10-21) as too round and too generic for "precise, understated".

All are variable fonts under the SIL Open Font License. Plex comes from the shared layer.
Archivo is self-hosted in `sites/studio/static/fonts/` in its full build (Latin subset,
from Fontsource 5.2.8), because the shared file has no width axis and the labels need
it. Don't add a serif unless a
photography-specific editorial treatment appears later.

## Visual style

- **Software and project pages:** clean grids, simple line icons, thin rules, restrained
  cards, minimal decoration.
- **Photography:** lots of negative space, edge-to-edge images, the logo kept
  unobtrusive. No heavy overlays and no branded frames.
- **Supporting graphic language** comes from the mark's own geometry: arcs, parallel
  lines, right angles, 45° cuts, circular framing, layered shapes. Avoid generic camera
  shutters, code brackets and circuit-board graphics.

## On the web

The site is Blowfish with a Studio layer on top of the shared parlette.net layer:

| File | What it does |
|---|---|
| `assets/css/schemes/studio.css` | The Blowfish colour scheme. Neutral runs Soft White → Midnight Navy (navy sits at `neutral-800`, which Blowfish uses for headings and the dark-mode ground). Primary is Signal Blue, secondary is Steel. |
| `assets/css/studio.css` | Fonts, links, buttons, hero, pillars, cards, the ledger in Studio type, and the brand page. Loaded after the shared CSS, so it overrides it. |
| `layouts/partials/extend-head.html` | Preloads Archivo and IBM Plex Sans and links `studio.css`. Replaces the shared partial. |
| `layouts/partials/home/custom.html` | The home page: hero, pillars, then the page content and the ledger. Hero words live in `content/_index.md` front matter. |
| `assets/icons/ps-*.svg` | The icon set. |

Rules the CSS encodes:

- **Links:** Signal Blue at `#2563EB`, which clears 4.5:1 on Soft White (`#3B82F6`
  doesn't), with a thin underline that firms up on hover. Dark mode uses `#60A5FA`.
  Project names in the ledger stay navy, so the only blue in that table is the one
  live status.
- **Buttons:** square-shouldered (2px radius), label type, no shadow. Solid navy for the
  one primary action, a Cool Gray outline for the alternative. They invert on dark.
- **Rules over boxes:** sections divide with 1px Cool Gray rules (Deep Slate on dark).
  Cards, where needed, are a hairline border with no shadow.
- **Spacing:** a 4px base. Sections are separated by `clamp(3.5rem, 8vw, 6rem)`.
- **Dark mode:** the ground is Midnight Navy, text Soft White and `neutral-300`, Steel
  becomes Light Steel. The header logo is inline SVG whose two fills are CSS classes,
  so it follows the theme.
- **Focus:** a 2px Signal Blue outline, offset 3px.

## Icons

Line icons on a 24-unit grid, 1.5 stroke, butt caps and mitred joins, in `currentColor`.
They are drawn from the mark's geometry rather than generic symbols:

- **Software** (`ps-software`): a window with a prompt chevron on the mark's slope.
- **Photography** (`ps-photography`): the aperture ring as four blades around a lens.
- **Digital creation** (`ps-digital`): the hidden A, an apex with its notch.

Use them in Steel (Light Steel on dark) next to labels, never as decoration on their own.

## Imagery

- **Photography is Andrew's own.** Nothing generated is ever presented as a photograph
  he took.
- **AI-generated illustration is allowed as decoration:** backdrops, textures, the
  social card, placeholders. It must stay in the palette: cool steel and slate, high key
  or deep navy, with vast negative space. `imagery/` holds the sources, the prompts and
  the script (local ComfyUI on pompom).
- The home hero backdrop (`assets/img/hero-backdrop.jpg`) sits at 55% opacity behind a
  soft radial mask (18% and desaturated in dark mode), so it never competes with the
  words.
- The social card (`assets/img/social.png`, 1200 × 630) is the reverse horizontal lockup
  on a navy horizon. `imagery/social_card.py` rebuilds it.

## Photography watermark

Use the **mark only**, white or black, at low opacity (about 30–50%), small, in a
corner. It should feel like a signature, not advertising. Never put the full lockup
across an image.

## Language

- **Descriptor:** Software • Photography • Digital Creation. It goes near the logo but
  is never part of it.
- **Philosophy:** Create thoughtfully. Build well. Keep exploring.
- **Positioning:** Parlette Studios is an independent creative studio for software,
  photography, and digital projects.

## Domain

The site is `studio.parlette.net`. `parlettestudios.com` redirects to it (see
`workers/redirects/`). If `parlette.studio` is registered later, it can either
become the canonical address (cleanest in print: **PARLETTE STUDIOS** /
`parlette.studio`) or join the redirects.

## Rebuilding the logo

The geometry is defined in `logo/src/generate.py`: exact rectangles, polygons and
circular-arc sectors. Its constants (`W`, `T`, `G`, `R`, `K`, `CUT`, `TAN`, `CUTS`) are the
whole construction. One script rebuilds everything from it:

```sh
sites/studio/brand/logo/src/build.sh    # optional arg: path to vectorcraft-cli
```

It runs `generate.py`, has VectorCraft unite each colour into one path and trim the
artboard, writes the colour variants (the same paths with their fills swapped), then the
padded PNGs (`export_png.py`) and PDFs. Finally `site_assets.py` writes what the site uses:
the theme-aware header logo, the favicons and web manifest, and the hero drawing. You
can also edit the `.vectorcraft` files directly in VectorCraft.

The concept boards this system came from were AI-generated mockups. They are references
only: their logos are raster images and not usable as artwork.
