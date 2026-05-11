"""Load, merge, and validate install manifests."""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

try:
    import yaml  # PyYAML
except ImportError:
    print(
        "[constitution] ERROR: PyYAML not installed.\n"
        "  Run: python3 -m pip install --user pyyaml\n"
        "  Or use the wrapper scripts (install.sh / install.ps1) which bootstrap it.",
        file=sys.stderr,
    )
    sys.exit(1)

from .common import detect_os, env_vars, resolve_vars


def _deep_merge(base: dict, override: dict) -> dict:
    """Deep-merge override into base. Lists are replaced, dicts are merged."""
    result = dict(base)
    for k, v in override.items():
        if k in result and isinstance(result[k], dict) and isinstance(v, dict):
            result[k] = _deep_merge(result[k], v)
        else:
            result[k] = v
    return result


def load(default_path: Path, machine_path: Optional[Path] = None) -> Dict[str, Any]:
    """Load default manifest, optionally overlay machine-local manifest."""
    if not default_path.exists():
        raise FileNotFoundError(f"Manifest not found: {default_path}")
    with default_path.open("r", encoding="utf-8") as f:
        manifest = yaml.safe_load(f) or {}
    if machine_path and machine_path.exists():
        with machine_path.open("r", encoding="utf-8") as f:
            machine = yaml.safe_load(f) or {}
        manifest = _deep_merge(manifest, machine)
    return manifest


def build_vars(
    manifest: Dict[str, Any],
    cli_overrides: Optional[Dict[str, str]] = None,
) -> Dict[str, str]:
    """Build the variable dict for ${VAR} substitution.

    Resolution order: env vars -> manifest paths -> CLI overrides.
    Adds CONSTITUTION_VERSION from manifest.
    """
    vars = env_vars()
    vars["CONSTITUTION_VERSION"] = str(
        manifest.get("constitution", {}).get("version", "0.0.0")
    )
    # Resolve manifest paths (these may reference env vars)
    paths = manifest.get("paths", {}) or {}
    for k, v in paths.items():
        resolved = resolve_vars(str(v), vars)
        # Empty string from env var -> let CLI / manifest fill it later
        if resolved and not resolved.startswith("${"):
            vars[k.upper()] = resolved
            vars[k] = resolved
    if cli_overrides:
        for k, v in cli_overrides.items():
            vars[k] = str(v)
            vars[k.upper()] = str(v)

    # Auto-derive WORKSPACE_NAME from WORKSPACE_ROOT if not explicitly set.
    # Allows templates to reference a friendly display name without hard-coding.
    if not vars.get("WORKSPACE_NAME"):
        ws = vars.get("WORKSPACE_ROOT", "")
        if ws:
            # Use Path basename — last path component, regardless of separator.
            from pathlib import PurePath
            vars["WORKSPACE_NAME"] = PurePath(ws).name or ws
    return vars


def filter_components(
    manifest: Dict[str, Any], current_os: Optional[str] = None
) -> List[Dict[str, Any]]:
    """Return enabled components matching the current OS."""
    if current_os is None:
        current_os = detect_os()
    components = []
    for name, spec in (manifest.get("components") or {}).items():
        if not spec.get("enabled", True):
            continue
        os_filter = spec.get("os")
        if os_filter and current_os not in os_filter:
            continue
        components.append({**spec, "name": name})
    return components


def validate(manifest: Dict[str, Any], vars: Dict[str, str]) -> List[str]:
    """Return list of error strings (empty if valid)."""
    errors: List[str] = []
    ws = vars.get("WORKSPACE_ROOT", "")
    if not ws or ws.startswith("${"):
        errors.append(
            "WORKSPACE_ROOT is required. Either set the env var "
            "(WORKSPACE_ROOT=/path/to/agents on Unix, "
            '$env:WORKSPACE_ROOT="D:\\path" on PowerShell) '
            "or set paths.workspace_root in manifests/machine.local.yaml."
        )
    if not manifest.get("components"):
        errors.append("Manifest has no `components` section.")
    return errors
