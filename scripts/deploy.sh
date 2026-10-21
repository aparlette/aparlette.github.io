#!/usr/bin/env bash
# Build and deploy one site, or the redirect Worker, to Cloudflare.
#
#   ./scripts/deploy.sh studio
#   ./scripts/deploy.sh redirects
#
# Needs Cloudflare credentials: either `npx wrangler login` once, or
# CLOUDFLARE_API_TOKEN in the environment (which is what CI uses).
source "$(dirname "$0")/lib.sh"
require_tools npx

target=${1:-}
if [ -z "$target" ]; then
  echo "error: name a site to deploy" >&2
  echo "known targets: ${SITES[*]} redirects" >&2
  exit 1
fi

if [ "$target" = "redirects" ]; then
  echo "==> testing redirect table"
  ( cd "$REPO_ROOT" && node --test workers/redirects/test/ )
  echo "==> deploying redirect Worker"
  ( cd "$REPO_ROOT/workers/redirects" && npx wrangler deploy )
  exit 0
fi

if ! valid_site "$target"; then
  echo "error: unknown target '$target'" >&2
  echo "known targets: ${SITES[*]} redirects" >&2
  exit 1
fi

"$REPO_ROOT/scripts/build.sh" "$target"
echo "==> deploying $target"
( cd "$REPO_ROOT/sites/$target" && npx wrangler deploy )
