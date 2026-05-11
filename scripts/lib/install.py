"""Install the AI Workspace Constitution to a target machine.

Usage (via wrapper):
    ./scripts/install.sh           # macOS / Linux / Git-Bash
    .\\scripts\\install.ps1        # Windows PowerShell

Direct:
    cd <repo>
    python3 -m scripts.lib.install [--workspace-root PATH] [--dry-run] [--yes]
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any, Dict, List

from .common import (
    Log,
    detect_os,
    make_backup,
    now_iso_compact,
    repo_root,
    sha256_bytes,
    short_path,
)
from . import manifest as mf
from . import render as rd
from . import state as st


# ── Argument parsing ─────────────────────────────────────────────────
def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        prog="constitution-install",
        description="Install the AI Workspace Constitution to a target machine.",
    )
    p.add_argument(
        "--workspace-root",
        default=None,
        help="Override $WORKSPACE_ROOT (the target workspace path).",
    )
    p.add_argument(
        "--manifest",
        default=None,
        help="Path to default manifest (defaults to manifests/default.yaml).",
    )
    p.add_argument(
        "--machine-manifest",
        default=None,
        help="Path to per-machine manifest (defaults to manifests/machine.local.yaml).",
    )
    p.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the install plan without writing any files.",
    )
    p.add_argument(
        "--yes",
        "-y",
        action="store_true",
        help="Skip the interactive confirmation prompt.",
    )
    p.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Print every file written.",
    )
    return p.parse_args()


# ── Plan building ────────────────────────────────────────────────────
def build_plan(
    manifest_data: Dict[str, Any],
    vars: Dict[str, str],
    repo: Path,
) -> List[Dict[str, Any]]:
    """Return list of action dicts: source, target, component, mode, marker info."""
    plan: List[Dict[str, Any]] = []
    components = mf.filter_components(manifest_data)

    for comp in components:
        name = comp["name"]
        sources = comp.get("sources") or []
        target_dir_tmpl = comp.get("target_dir")
        target_file_tmpl = comp.get("target")
        mode = comp.get("mode", "replace")
        marker_start = comp.get("section_marker_start")
        marker_end = comp.get("section_marker_end")

        for src_rel in sources:
            src_rel = src_rel.rstrip("/").rstrip("\\")
            src_path = (repo / src_rel).resolve()
            if not src_path.exists():
                Log.warn(f"[{name}] source missing: {src_rel}")
                continue

            for src_file in rd.walk_files(src_path):
                # Compute target path
                if src_path.is_file():
                    if target_file_tmpl:
                        # Single explicit target file
                        tgt = Path(rd.resolve_vars(target_file_tmpl, vars))
                    elif target_dir_tmpl:
                        # File goes under target_dir, drop .tmpl
                        tgt_dir = Path(rd.resolve_vars(target_dir_tmpl, vars))
                        tgt = tgt_dir / rd.strip_tmpl_suffix(src_file).name
                    else:
                        Log.warn(f"[{name}] no target/target_dir for {src_rel}")
                        continue
                else:
                    # Directory source: preserve leaf dir name + relative subpath
                    tgt_dir = Path(rd.resolve_vars(target_dir_tmpl, vars))
                    rel = src_file.relative_to(src_path)
                    tgt = tgt_dir / src_path.name / rel
                    tgt = rd.strip_tmpl_suffix(tgt)

                plan.append({
                    "component": name,
                    "source": src_file,
                    "target": tgt,
                    "mode": mode,
                    "marker_start": marker_start,
                    "marker_end": marker_end,
                })
    return plan


# ── Execution ────────────────────────────────────────────────────────
def execute(
    plan: List[Dict[str, Any]],
    vars: Dict[str, str],
    state: Dict[str, Any],
    repo: Path,
    backup_ts: str,
    verbose: bool,
) -> int:
    """Execute the plan. Returns count of files written."""
    written = 0
    for action in plan:
        comp = action["component"]
        src = action["source"]
        tgt = action["target"]
        mode = action["mode"]

        rendered_bytes, was_tmpl = rd.render_file(src, vars)

        if mode == "marker-section":
            rendered_text = rendered_bytes.decode("utf-8")
            rd.apply_marker_section(
                tgt, rendered_text,
                action["marker_start"], action["marker_end"],
            )
            # Record hash of the rendered section content only.
            # Content outside the markers is unmanaged, so we don't track it.
            section_sha = sha256_bytes(rendered_text.encode("utf-8"))
            st.record_file(
                state, tgt, section_sha, short_path(src, repo), comp,
                mode="marker-section",
                marker_start=action["marker_start"],
                marker_end=action["marker_end"],
            )
            if verbose:
                Log.detail(f"[{comp}] marker-applied -> {tgt}")
            written += 1
            continue

        # Default: replace mode
        tgt.parent.mkdir(parents=True, exist_ok=True)
        if tgt.exists():
            existing = tgt.read_bytes()
            if existing == rendered_bytes:
                # No change; still record state
                st.record_file(state, tgt, sha256_bytes(rendered_bytes),
                               short_path(src, repo), comp)
                if verbose:
                    Log.detail(f"[{comp}] unchanged -> {tgt}")
                continue
            # Differs; back it up first
            make_backup(tgt, backup_ts)
            if verbose:
                Log.detail(f"[{comp}] backed up old -> .backup.{backup_ts}")

        tgt.write_bytes(rendered_bytes)
        sha = sha256_bytes(rendered_bytes)
        st.record_file(state, tgt, sha, short_path(src, repo), comp)
        if verbose:
            Log.detail(f"[{comp}] wrote -> {tgt}")
        written += 1

    return written


# ── Main ─────────────────────────────────────────────────────────────
def main() -> int:
    args = parse_args()
    repo = repo_root()

    cli_overrides: Dict[str, str] = {}
    if args.workspace_root:
        cli_overrides["WORKSPACE_ROOT"] = args.workspace_root

    manifest_path = (
        Path(args.manifest) if args.manifest
        else repo / "manifests" / "default.yaml"
    )
    machine_path = (
        Path(args.machine_manifest) if args.machine_manifest
        else repo / "manifests" / "machine.local.yaml"
    )

    Log.info(f"Repo: {repo}")
    Log.info(f"Manifest: {short_path(manifest_path, repo)}")
    if machine_path.exists():
        Log.info(f"Machine overlay: {short_path(machine_path, repo)}")

    manifest_data = mf.load(manifest_path, machine_path)
    vars = mf.build_vars(manifest_data, cli_overrides)

    errors = mf.validate(manifest_data, vars)
    if errors:
        for e in errors:
            Log.error(e)
        return 2

    workspace_root = Path(vars["WORKSPACE_ROOT"])
    Log.info(f"Target workspace: {workspace_root}")
    Log.info(f"OS: {detect_os()}")
    Log.info(f"Constitution version: {vars['CONSTITUTION_VERSION']}")

    plan = build_plan(manifest_data, vars, repo)
    components_in_plan = {a["component"] for a in plan}
    Log.info(
        f"Plan: {len(plan)} files across {len(components_in_plan)} components."
    )

    if args.verbose or args.dry_run:
        for action in plan:
            print(
                f"  {action['component']:42} "
                f"{short_path(action['source'], repo)} -> {action['target']}"
            )

    if args.dry_run:
        Log.info("Dry-run; no files written.")
        return 0

    if not args.yes:
        try:
            resp = input(f"Proceed with install to {workspace_root}? [y/N] ").strip().lower()
        except EOFError:
            resp = ""
        if resp != "y":
            Log.info("Aborted.")
            return 1

    state = st.load(workspace_root) or st.new_state(vars["CONSTITUTION_VERSION"])
    state["constitution_version"] = vars["CONSTITUTION_VERSION"]
    backup_ts = now_iso_compact()

    written = execute(plan, vars, state, repo, backup_ts, args.verbose)

    st.save(workspace_root, state)
    Log.ok(
        f"Done. {written} files written. "
        f"State: {st.state_path(workspace_root)}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
