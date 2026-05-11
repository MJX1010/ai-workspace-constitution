"""Manage the .constitution-state.json file on the target machine.

The state file records which files were materialised, their SHA-256 hashes,
and the constitution version. It enables:
  - drift detection by `verify`
  - precise removal by `uninstall`
  - changelog diff by `update`
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Optional

from .common import now_iso


STATE_FILENAME = ".constitution-state.json"


def state_path(workspace_root: Path) -> Path:
    return workspace_root / STATE_FILENAME


def load(workspace_root: Path) -> Optional[Dict[str, Any]]:
    p = state_path(workspace_root)
    if not p.exists():
        return None
    with p.open("r", encoding="utf-8") as f:
        return json.load(f)


def save(workspace_root: Path, state: Dict[str, Any]) -> None:
    p = state_path(workspace_root)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("w", encoding="utf-8") as f:
        json.dump(state, f, indent=2, ensure_ascii=False)
        f.write("\n")


def new_state(version: str) -> Dict[str, Any]:
    ts = now_iso()
    return {
        "constitution_version": version,
        "installed_at": ts,
        "updated_at": ts,
        "files": {},
    }


def record_file(
    state: Dict[str, Any],
    target: Path,
    sha: str,
    source: str,
    component: str,
    mode: str = "replace",
    marker_start: Optional[str] = None,
    marker_end: Optional[str] = None,
) -> None:
    """Record (or update) a single file in the state.

    For replace mode: sha is the SHA-256 of the full file content.
    For marker-section mode: sha is the SHA-256 of the section between markers
    (the parts of the file outside the markers are unmanaged).
    """
    entry: Dict[str, Any] = {
        "sha256": sha,
        "source": source,
        "component": component,
        "mode": mode,
        "updated_at": now_iso(),
    }
    if mode == "marker-section":
        entry["marker_start"] = marker_start
        entry["marker_end"] = marker_end
    state["files"][str(target)] = entry
    state["updated_at"] = now_iso()


def remove_file(state: Dict[str, Any], target: Path) -> None:
    state["files"].pop(str(target), None)
    state["updated_at"] = now_iso()


def installed_files(state: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    return state.get("files", {})
