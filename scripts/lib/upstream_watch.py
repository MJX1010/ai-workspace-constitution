"""Watch upstream documentation sources for drift.

Fetches each source listed in `upstream/sources.yaml`, compares its SHA-256
against the last-saved snapshot, and either reports drift (--check) or
captures the new snapshot (--apply).

The maintainer is then expected to:
  1. `git diff upstream/` to read what actually changed
  2. Decide whether to absorb the change into `governance/`
  3. If yes: edit governance, bump VERSION, add CHANGELOG entry, commit
  4. `git push`

Network: stdlib `urllib.request` only (no `requests` dep). Honours $http_proxy
/ $https_proxy env vars automatically.
"""
from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any, Dict, List, Optional

try:
    import yaml
except ImportError:
    print(
        "[constitution] ERROR: PyYAML not installed. "
        "Use scripts/upstream-watch.sh which bootstraps it.",
        file=sys.stderr,
    )
    sys.exit(1)

from .common import Log, now_iso, repo_root, sha256_bytes


UPSTREAM_STATE_FILENAME = ".upstream-state.json"


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        prog="constitution-upstream-watch",
        description="Detect drift in upstream provider documentation.",
    )
    p.add_argument(
        "--check",
        action="store_true",
        help="Fetch and report diffs without saving snapshots (default if neither flag).",
    )
    p.add_argument(
        "--apply",
        action="store_true",
        help="Save new snapshots and update upstream state file.",
    )
    p.add_argument(
        "--source",
        action="append",
        default=None,
        help="Only check specific source IDs (repeatable).",
    )
    p.add_argument(
        "--sources-file",
        default=None,
        help="Override path to sources.yaml.",
    )
    p.add_argument(
        "--timeout",
        type=int,
        default=None,
        help="HTTP timeout in seconds (default from sources.yaml policy).",
    )
    p.add_argument("--verbose", "-v", action="store_true")
    return p.parse_args()


def load_sources(path: Path) -> Dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"Sources file not found: {path}")
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def load_state(state_path: Path) -> Dict[str, Any]:
    if not state_path.exists():
        return {"sources": {}}
    with state_path.open("r", encoding="utf-8") as f:
        return json.load(f)


def save_state(state_path: Path, state: Dict[str, Any]) -> None:
    state_path.parent.mkdir(parents=True, exist_ok=True)
    with state_path.open("w", encoding="utf-8") as f:
        json.dump(state, f, indent=2, ensure_ascii=False)
        f.write("\n")


def fetch(url: str, user_agent: str, timeout: int) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": user_agent})
    with urllib.request.urlopen(req, timeout=timeout) as resp:  # noqa: S310 - explicit URLs
        return resp.read()


def filter_sources(
    sources: List[Dict[str, Any]], requested_ids: Optional[List[str]]
) -> List[Dict[str, Any]]:
    if not requested_ids:
        return sources
    requested = set(requested_ids)
    found = [s for s in sources if s["id"] in requested]
    missing = requested - {s["id"] for s in found}
    for m in missing:
        Log.warn(f"Unknown source id: {m}")
    return found


def main() -> int:
    args = parse_args()
    repo = repo_root()

    sources_path = (
        Path(args.sources_file) if args.sources_file
        else repo / "upstream" / "sources.yaml"
    )
    state_path = repo / "upstream" / UPSTREAM_STATE_FILENAME

    try:
        cfg = load_sources(sources_path)
    except FileNotFoundError as e:
        Log.error(str(e))
        return 2

    policy = cfg.get("policy", {}) or {}
    user_agent = policy.get("user_agent", "ai-workspace-constitution")
    timeout = args.timeout or policy.get("timeout_seconds", 30)

    sources = cfg.get("sources", []) or []
    sources = filter_sources(sources, args.source)
    if not sources:
        Log.warn("No sources to check.")
        return 0

    # If neither --check nor --apply, default to --check.
    apply_mode = args.apply
    if not apply_mode and not args.check:
        Log.info("(neither --check nor --apply given; defaulting to --check)")

    state = load_state(state_path)
    state.setdefault("sources", {})

    Log.info(f"Sources: {len(sources)} | Mode: {'APPLY' if apply_mode else 'CHECK'}")

    new_count = 0
    changed_count = 0
    unchanged_count = 0
    error_count = 0
    changed_ids: List[str] = []

    for src in sources:
        sid = src["id"]
        url = src["url"]
        snapshot_rel = src.get("snapshot")
        if not snapshot_rel:
            Log.warn(f"[{sid}] no snapshot path; skipping")
            continue
        snapshot_path = repo / snapshot_rel

        Log.info(f"[{sid}] fetching {url}")
        try:
            content = fetch(url, user_agent, timeout)
        except urllib.error.URLError as e:
            Log.warn(f"[{sid}] fetch error: {e.reason}")
            error_count += 1
            continue
        except Exception as e:
            Log.warn(f"[{sid}] {type(e).__name__}: {e}")
            error_count += 1
            continue

        new_hash = sha256_bytes(content)
        prev = state["sources"].get(sid, {})
        prev_hash = prev.get("sha256")

        if prev_hash is None:
            Log.warn(f"[{sid}] NEW (no prior snapshot)")
            new_count += 1
            changed_ids.append(sid)
        elif prev_hash != new_hash:
            Log.warn(
                f"[{sid}] CHANGED ({prev_hash[:8]} -> {new_hash[:8]})"
            )
            changed_count += 1
            changed_ids.append(sid)
        else:
            unchanged_count += 1
            if args.verbose:
                Log.detail(f"[{sid}] unchanged")
            continue

        if apply_mode:
            snapshot_path.parent.mkdir(parents=True, exist_ok=True)
            snapshot_path.write_bytes(content)
            state["sources"][sid] = {
                "sha256": new_hash,
                "url": url,
                "snapshot": snapshot_rel,
                "fetched_at": now_iso(),
                "size": len(content),
            }

    if apply_mode and (new_count or changed_count):
        save_state(state_path, state)
        Log.ok("Snapshots updated. Review with: git diff upstream/")
        Log.info(
            "If a change is substantive, edit governance/, bump VERSION, "
            "add a CHANGELOG `Upstream` entry, then commit."
        )

    Log.ok(
        f"Done. checked={len(sources)} "
        f"new={new_count} changed={changed_count} "
        f"unchanged={unchanged_count} errors={error_count}"
    )

    if (new_count or changed_count) and not apply_mode:
        Log.info(
            "Drift detected. Re-run with --apply to capture snapshots, "
            "then `git diff upstream/`."
        )

    if error_count > 0 and (new_count + changed_count) == 0:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
