#!/usr/bin/env bash
# Build one site, or every site when given no argument.
#
#   ./scripts/build.sh            # all of them
#   ./scripts/build.sh studio     # just studio.parlette.net
source "$(dirname "$0")/lib.sh"
require_tools hugo go

build_one() {
  local site=$1
  echo "==> building $site"
  ( cd "$REPO_ROOT/sites/$site" && hugo --gc --minify --cleanDestinationDir )
}

if [ $# -eq 0 ]; then
  for site in "${SITES[@]}"; do build_one "$site"; done
  exit 0
fi

if ! valid_site "$1"; then
  echo "error: unknown site '$1'" >&2
  usage_sites
  exit 1
fi
build_one "$1"
