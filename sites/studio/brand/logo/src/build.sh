#!/usr/bin/env bash
# Rebuild every Parlette Studios logo file from generate.py.
#
#   sites/studio/brand/logo/src/build.sh [path/to/vectorcraft-cli]
#
# 1. generate.py draws mark, lockup, horizontal and badge as overlapping primitives.
# 2. VectorCraft unites each colour into one path and trims the artboard.
# 3. Colour variants are the same paths with fills swapped.
# 4. export_png.py makes padded PNGs; VectorCraft makes the PDFs.
# 5. The site gets a theme-aware header logo and favicons.
set -euo pipefail

VC=${1:-/projects/external/ArtCraft/vectorcraft/target/release/vectorcraft-cli}
SRC="$(cd "$(dirname "$0")" && pwd)"
LOGO="$(dirname "$SRC")"
SITE="$(cd "$LOGO/../.." && pwd)"
WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT

NAVY=0f1720 STEEL=64748b LIGHT=94a3b8

python3 "$SRC/generate.py" "$WORK"

for n in mark lockup horizontal badge; do
  "$VC" run --in "$WORK/$n.svg" \
    --cmd select.all --cmd select.same.fillColor --cmd object.pathfinder.unite \
    --cmd select.inverse --cmd object.pathfinder.unite \
    --cmd select.none --cmd artboard.fitToArt \
    --export "$SRC/$n.vectorcraft" --export "$WORK/$n-clean.svg" >/dev/null
  b="$LOGO/parlette-studios-$n"
  sed -E 's#<title>[^<]*</title>#<title>Parlette Studios</title>#' "$WORK/$n-clean.svg" > "$b.svg"
  sed -e "s/#$STEEL/#$LIGHT/; s/#$NAVY/#ffffff/" "$b.svg" > "$b-reverse.svg"
  for c in navy:#$NAVY white:#ffffff black:#000000; do
    sed -E "s/#($NAVY|$STEEL)/${c#*:}/g" "$b.svg" > "$b-${c%%:*}.svg"
  done
done

rm -f "$LOGO"/png/*.png "$LOGO"/pdf/*.pdf
mkdir -p "$LOGO/pdf"
python3 "$SRC/export_png.py" "$LOGO" "$VC" >/dev/null
for n in mark lockup horizontal badge; do
  "$VC" convert "$LOGO/parlette-studios-$n.svg" "$LOGO/pdf/parlette-studios-$n.pdf" >/dev/null
done

python3 "$SRC/site_assets.py" "$LOGO" "$SITE" "$VC"
echo "logo files rebuilt"
