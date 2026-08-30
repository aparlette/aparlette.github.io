#!/usr/bin/env bash
# Serve one site locally with live reload.
#
#   ./scripts/dev.sh studio
#
# Each site gets its own port so several can run side by side.
source "$(dirname "$0")/lib.sh"
require_tools hugo go

site=${1:-andrew}
if ! valid_site "$site"; then
  echo "error: unknown site '$site'" >&2
  usage_sites
  exit 1
fi

case "$site" in
  andrew) port=1313 ;;
  www)    port=1314 ;;
  studio) port=1315 ;;
esac

echo "==> $site on http://localhost:$port"
cd "$REPO_ROOT/sites/$site"
exec hugo server --port "$port" --buildDrafts --disableFastRender
