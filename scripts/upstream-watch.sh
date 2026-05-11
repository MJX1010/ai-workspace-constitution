#!/usr/bin/env bash
# Watch upstream provider documentation for drift.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

find_python() {
  local cand
  for cand in python3 python; do
    if command -v "$cand" >/dev/null 2>&1; then
      local ver
      ver=$("$cand" -c 'import sys; print(sys.version_info[0]*100+sys.version_info[1])' 2>/dev/null || echo 0)
      if [ "$ver" -ge 308 ]; then echo "$cand"; return 0; fi
    fi
  done
  return 1
}

PY=$(find_python) || { echo "[constitution] ERROR: Python 3.8+ not found." >&2; exit 2; }

if ! "$PY" -c 'import yaml' 2>/dev/null; then
  echo "[constitution] PyYAML not found; installing via pip --user (one-time)..."
  "$PY" -m pip install --user --quiet --disable-pip-version-check pyyaml
fi

cd "$REPO_DIR"
exec "$PY" -m scripts.lib.upstream_watch "$@"
