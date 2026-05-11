"""Verify the constitution installation against the recorded state.

Reports:
  - OK     : file present, hash matches recorded
  - DRIFT  : file present, hash differs (someone edited the materialised file)
  - MISSING: file recorded in state but not on disk

For marker-section files, hashes only the content between markers — drift
in surrounding content (e.g. the OMC block in ~/.claude/CLAUDE.md) does not
trigger a false positive.

Exit codes:
  0  = all files OK (or fail_on_drift=false in manifest and no missing files)
  1  = drift or missing detected (and fail_on_drift=true)
  2  = no state file
  3  = invalid state
"""
from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple

from .common import Log, repo_root, sha256_bytes, sha256_file, short_path
from . import manifest as mf
from . import state as st


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        prog="constitution-verify",
        description="Verify the installed constitution against recorded state.",
    )
    p.add_argument(
        "--workspace-root",
        default=None,
        help="Workspace root to verify (defaults to $WORKSPACE_ROOT).",
    )
    p.add_argument(
        "--manifest",
        default=None,
        help="Path to default manifest (only used to read fail_on_drift).",
    )
    p.add_argument(
        "--fail-on-drift",
        action="store_true",
        help="Override manifest: exit non-zero on any drift or missing.",
    )
    p.add_argument("--verbose", "-v", action="store_true")
    return p.parse_args()


def extract_marker_section(
    text: str, marker_start: str, marker_end: str
) -> Tuple[bool, str]:
    """Return (found, section_text). section_text starts at marker_start and
    ends at the line containing marker_end (inclusive of newline)."""
    s_idx = text.find(marker_start)
    if s_idx == -1:
        return False, ""
    e_idx = text.find(marker_end, s_idx)
    if e_idx == -1:
        return False, ""
    e_idx += len(marker_end)
    line_end = text.find("\n", e_idx)
    if line_end != -1:
        e_idx = line_end + 1
    return True, text[s_idx:e_idx]


def hash_for_file(path: Path, info: Dict[str, Any]) -> Tuple[str, str]:
    """Compute the comparable hash for a file given its state entry.
    Returns (status, hash) where status is "ok" or an error description."""
    mode = info.get("mode", "replace")
    if mode == "marker-section":
        text = path.read_text(encoding="utf-8")
        found, section = extract_marker_section(
            text, info["marker_start"], info["marker_end"]
        )
        if not found:
            return ("markers-missing", "")
        # Normalize trailing newline so comparison is stable.
        normalized = section.rstrip("\n") + "\n"
        return ("ok", sha256_bytes(normalized.encode("utf-8")))
    return ("ok", sha256_file(path))


def main() -> int:
    args = parse_args()
    repo = repo_root()

    ws_root = args.workspace_root or os.environ.get("WORKSPACE_ROOT", "")
    if not ws_root:
        Log.error("WORKSPACE_ROOT is required (env var or --workspace-root).")
        return 2
    workspace_root = Path(ws_root)
    if not workspace_root.exists():
        Log.error(f"Workspace not found: {workspace_root}")
        return 2

    state = st.load(workspace_root)
    if not state:
        Log.error(f"No state file at {st.state_path(workspace_root)}.")
        Log.info("Run install first: ./scripts/install.sh")
        return 2

    fail_on_drift = args.fail_on_drift
    if not fail_on_drift:
        manifest_path = (
            Path(args.manifest) if args.manifest
            else repo / "manifests" / "default.yaml"
        )
        machine_path = repo / "manifests" / "machine.local.yaml"
        try:
            manifest_data = mf.load(manifest_path, machine_path)
            fail_on_drift = bool(
                manifest_data.get("verify", {}).get("fail_on_drift", False)
            )
        except Exception as e:
            Log.warn(f"Could not load manifest: {e}")

    files = st.installed_files(state)
    Log.info(f"Workspace: {workspace_root}")
    Log.info(f"Constitution version: {state.get('constitution_version', '?')}")
    Log.info(f"Installed at: {state.get('installed_at', '?')}")
    Log.info(f"Files in state: {len(files)}")

    ok: List[str] = []
    drift: List[Tuple[str, str]] = []
    missing: List[str] = []

    for path_str, info in files.items():
        p = Path(path_str)
        if not p.exists():
            missing.append(path_str)
            continue
        status, actual = hash_for_file(p, info)
        if status != "ok":
            drift.append((path_str, f"({status})"))
            continue
        if actual != info["sha256"]:
            drift.append((path_str, "(hash mismatch)"))
            continue
        ok.append(path_str)

    Log.ok(f"OK: {len(ok)}")
    if drift:
        Log.warn(f"Drift: {len(drift)}")
        for path_str, reason in drift:
            Log.detail(f"  {short_path(Path(path_str), workspace_root)} {reason}")
    if missing:
        Log.warn(f"Missing: {len(missing)}")
        for path_str in missing:
            Log.detail(f"  {short_path(Path(path_str), workspace_root)}")

    if args.verbose and ok:
        Log.detail("OK files:")
        for path_str in ok:
            Log.detail(f"  {short_path(Path(path_str), workspace_root)}")

    if drift or missing:
        if fail_on_drift:
            Log.error("Verification FAILED")
            return 1
        else:
            Log.warn(
                "Verification reports drift but fail_on_drift=false; "
                "exiting 0. Use --fail-on-drift to enforce."
            )
            return 0

    Log.ok("Verification PASSED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
