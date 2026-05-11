"""Shared utilities for the AI Workspace Constitution scripts.

Cross-platform: macOS / Linux / Windows. Python 3.8+, stdlib only.
"""
from __future__ import annotations

import datetime
import hashlib
import os
import platform
import shutil
import sys
from pathlib import Path
from typing import Dict


# ── OS detection ─────────────────────────────────────────────────────
def detect_os() -> str:
    s = platform.system().lower()
    if s == "windows":
        return "windows"
    if s == "darwin":
        return "macos"
    if s == "linux":
        return "linux"
    return s


def is_windows() -> bool:
    return detect_os() == "windows"


def is_macos() -> bool:
    return detect_os() == "macos"


def is_linux() -> bool:
    return detect_os() == "linux"


# ── Logging ──────────────────────────────────────────────────────────
class Log:
    """Minimal coloured logger. Falls back to plain text on Windows or non-tty."""

    USE_COLOR = sys.stdout.isatty() and not is_windows()
    PREFIX = "[constitution]"

    @staticmethod
    def _c(code: int, text: str) -> str:
        return f"\033[{code}m{text}\033[0m" if Log.USE_COLOR else text

    @staticmethod
    def info(msg: str) -> None:
        print(f"{Log.PREFIX} {msg}")

    @staticmethod
    def ok(msg: str) -> None:
        print(Log._c(32, f"{Log.PREFIX} {msg}"))

    @staticmethod
    def warn(msg: str) -> None:
        print(Log._c(33, f"{Log.PREFIX} WARN: {msg}"))

    @staticmethod
    def error(msg: str) -> None:
        print(Log._c(31, f"{Log.PREFIX} ERROR: {msg}"), file=sys.stderr)

    @staticmethod
    def detail(msg: str) -> None:
        print(Log._c(90, f"{Log.PREFIX}   {msg}"))


# ── Variable resolution ─────────────────────────────────────────────
def resolve_vars(text: str, vars: Dict[str, str]) -> str:
    """Replace every ${VAR} in text with vars[VAR]. Multi-pass for nested vars."""
    result = text
    for _ in range(8):  # cap at 8 passes to prevent infinite loops
        prev = result
        for key, value in vars.items():
            result = result.replace("${" + key + "}", str(value))
        if result == prev:
            break
    return result


def env_vars() -> Dict[str, str]:
    """Build the baseline variable dict from the environment."""
    home = (
        os.environ.get("HOME")
        or os.environ.get("USERPROFILE")
        or str(Path.home())
    )
    return {
        "HOME": home,
        "USERPROFILE": os.environ.get("USERPROFILE", home),
        "USER": os.environ.get("USER") or os.environ.get("USERNAME") or "user",
        "WORKSPACE_ROOT": os.environ.get("WORKSPACE_ROOT", ""),
    }


# ── Hashing ──────────────────────────────────────────────────────────
def sha256_bytes(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


# ── Backup ───────────────────────────────────────────────────────────
def backup_path(path: Path, timestamp: str) -> Path:
    return path.with_name(path.name + f".backup.{timestamp}")


def make_backup(path: Path, timestamp: str) -> Path:
    bak = backup_path(path, timestamp)
    shutil.copy2(path, bak)
    return bak


def now_iso_compact() -> str:
    """UTC timestamp suitable for filenames: 20260429T132300Z."""
    return datetime.datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")


def now_iso() -> str:
    return datetime.datetime.utcnow().isoformat(timespec="seconds") + "Z"


# ── Repo root ────────────────────────────────────────────────────────
def repo_root() -> Path:
    """Return the constitution repo root (parents[2] of this file)."""
    # This file lives at __ai_law/scripts/lib/common.py
    return Path(__file__).resolve().parents[2]


# ── Pretty paths ────────────────────────────────────────────────────
def short_path(p: Path, base: Path) -> str:
    """Return p relative to base if possible, else absolute."""
    try:
        return str(p.relative_to(base))
    except ValueError:
        return str(p)
