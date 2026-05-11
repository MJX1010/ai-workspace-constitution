#!/usr/bin/env bash
# Install the AI Workspace Constitution.
# Targets: macOS (bash 3.2+), Linux (bash 4+), Windows Git-Bash.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

# ── Find a usable Python 3.8+ ────────────────────────────────────────
find_python() {
  local cand
  for cand in python3 python; do
    if command -v "$cand" >/dev/null 2>&1; then
      local ver
      ver=$("$cand" -c 'import sys; print(sys.version_info[0]*100+sys.version_info[1])' 2>/dev/null || echo 0)
      if [ "$ver" -ge 308 ]; then
        echo "$cand"
        return 0
      fi
    fi
  done
  return 1
}

PY=$(find_python) || {
  cat >&2 <<'EOF'
[constitution] ERROR: Python 3.8+ not found.

Install one of:
  macOS  : brew install python3
  Linux  : apt-get install python3 python3-pip   (or your distro equivalent)
  Windows: winget install Python.Python.3.12     (or download from python.org)
EOF
  exit 2
}

# ── Bootstrap PyYAML on first run ────────────────────────────────────
if ! "$PY" -c 'import yaml' 2>/dev/null; then
  echo "[constitution] PyYAML not found; installing via pip --user (one-time)..."
  if ! "$PY" -m pip install --user --quiet --disable-pip-version-check pyyaml; then
    cat >&2 <<EOF
[constitution] ERROR: failed to install PyYAML.
  Try manually: $PY -m pip install --user pyyaml
  If your environment blocks pip, see docs/migration.md for offline options.
EOF
    exit 3
  fi
fi

# ── Dispatch to Python entrypoint ────────────────────────────────────
cd "$REPO_DIR"
exec "$PY" -m scripts.lib.install "$@"
