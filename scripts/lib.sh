# Shared helpers. Sourced, not executed.
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SITES=(andrew www studio)

# Hugo needs the Go toolchain because the theme is a Hugo Module. A local
# install under ~/.local/go is not on every PATH, so add it when it is there.
if ! command -v go >/dev/null 2>&1 && [ -x "$HOME/.local/go/bin/go" ]; then
  export PATH="$HOME/.local/go/bin:$PATH"
fi

require_tools() {
  local missing=0
  for tool in "$@"; do
    if ! command -v "$tool" >/dev/null 2>&1; then
      echo "error: '$tool' is not installed or not on PATH" >&2
      missing=1
    fi
  done
  [ "$missing" -eq 0 ] || exit 1
}

valid_site() {
  local candidate=$1
  for site in "${SITES[@]}"; do
    [ "$site" = "$candidate" ] && return 0
  done
  return 1
}

usage_sites() {
  echo "known sites: ${SITES[*]}" >&2
}
