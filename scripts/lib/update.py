"""Update the constitution from upstream and re-render to the target machine.

Flow:
  1. Check git working tree is clean (unless --allow-dirty)
  2. git pull --ff-only
  3. Re-run install --yes
  4. Run verify
  5. Print summary

The user is responsible for `git push` of any local edits before running update,
and for resolving merge conflicts if `git pull --ff-only` fails.

Note: this command consumes a constitution; it does not author CHANGELOG entries.
For author-side workflow (writing changelog, bumping version, releasing), see
docs/update-policy.md.
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path
from typing import List

from .common import Log, repo_root


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        prog="constitution-update",
        description="Pull latest constitution, re-render, and verify.",
    )
    p.add_argument("--workspace-root", default=None)
    p.add_argument(
        "--no-pull", action="store_true",
        help="Skip git pull. Useful for re-rendering after local edits."
    )
    p.add_argument(
        "--no-verify", action="store_true",
        help="Skip post-install verification."
    )
    p.add_argument(
        "--allow-dirty", action="store_true",
        help="Allow git pull even when the working tree has uncommitted changes."
    )
    p.add_argument("--yes", "-y", action="store_true")
    p.add_argument("--verbose", "-v", action="store_true")
    return p.parse_args()


def run(cmd: List[str], cwd: Path = None, check: bool = False) -> subprocess.CompletedProcess:
    Log.detail(f"$ {' '.join(cmd)}")
    return subprocess.run(cmd, cwd=str(cwd) if cwd else None, check=check)


def is_git_repo(path: Path) -> bool:
    r = subprocess.run(
        ["git", "-C", str(path), "rev-parse", "--git-dir"],
        capture_output=True, text=True,
    )
    return r.returncode == 0


def is_clean(path: Path) -> bool:
    r = subprocess.run(
        ["git", "-C", str(path), "status", "--porcelain"],
        capture_output=True, text=True,
    )
    return r.stdout.strip() == ""


def current_commit(path: Path) -> str:
    r = subprocess.run(
        ["git", "-C", str(path), "rev-parse", "--short", "HEAD"],
        capture_output=True, text=True,
    )
    return r.stdout.strip() if r.returncode == 0 else "?"


def main() -> int:
    args = parse_args()
    repo = repo_root()

    Log.info(f"Constitution repo: {repo}")

    # ── Stage 1: pull ────────────────────────────────────────────────
    if args.no_pull:
        Log.info("Skipping git pull (--no-pull).")
    elif not is_git_repo(repo):
        Log.warn("Not a git repo; skipping pull.")
    else:
        before = current_commit(repo)
        if not is_clean(repo) and not args.allow_dirty:
            Log.error(
                "Working tree has uncommitted changes. "
                "Commit/stash first, or pass --allow-dirty."
            )
            run(["git", "-C", str(repo), "status", "--short"])
            return 1

        Log.info(f"Pulling latest constitution (currently at {before})...")
        r = run(["git", "-C", str(repo), "pull", "--ff-only"])
        if r.returncode != 0:
            Log.error(
                "git pull failed (likely non-fast-forward). "
                "Resolve manually with `git pull` or `git rebase` and re-run update."
            )
            return 2

        after = current_commit(repo)
        if before == after:
            Log.info("Already up to date.")
        else:
            Log.ok(f"Pulled: {before} -> {after}")

    # ── Stage 2: install ─────────────────────────────────────────────
    Log.info("Re-rendering constitution to workspace...")
    install_cmd = [sys.executable, "-m", "scripts.lib.install"]
    if args.yes:
        install_cmd.append("--yes")
    else:
        # update implies yes; user already opted in by running update
        install_cmd.append("--yes")
    if args.workspace_root:
        install_cmd += ["--workspace-root", args.workspace_root]
    if args.verbose:
        install_cmd.append("--verbose")
    r = run(install_cmd, cwd=repo)
    if r.returncode != 0:
        Log.error(f"Install step failed (exit {r.returncode}).")
        return r.returncode

    # ── Stage 3: verify ──────────────────────────────────────────────
    if args.no_verify:
        Log.info("Skipping verify (--no-verify).")
    else:
        Log.info("Verifying...")
        verify_cmd = [sys.executable, "-m", "scripts.lib.verify"]
        if args.workspace_root:
            verify_cmd += ["--workspace-root", args.workspace_root]
        r = run(verify_cmd, cwd=repo)
        if r.returncode != 0:
            Log.warn(f"Verify reported issues (exit {r.returncode}).")
            # Don't fail update on drift — verify already logged what's wrong.

    Log.ok("Update complete.")
    Log.info("Next: run `git push` from the constitution repo if you authored changes.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
