"""Template rendering and target-path computation.

Templates use ${VAR} placeholders. Files with the .tmpl suffix are rendered;
files without it are copied verbatim. Directories are walked recursively.
"""
from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Tuple

from .common import resolve_vars


TMPL_SUFFIX = ".tmpl"


def render_text(text: str, vars: Dict[str, str]) -> str:
    return resolve_vars(text, vars)


def render_file(source: Path, vars: Dict[str, str]) -> Tuple[bytes, bool]:
    """Returns (rendered_bytes, was_template)."""
    if source.suffix == TMPL_SUFFIX:
        text = source.read_text(encoding="utf-8")
        rendered = render_text(text, vars)
        return rendered.encode("utf-8"), True
    return source.read_bytes(), False


def strip_tmpl_suffix(path: Path) -> Path:
    """File.md.tmpl -> File.md; File.md -> File.md."""
    if path.suffix == TMPL_SUFFIX:
        return path.with_suffix("")
    return path


def walk_files(root: Path) -> List[Path]:
    """Sorted list of all regular files under root (or [root] if it's a file)."""
    if root.is_file():
        return [root]
    if not root.is_dir():
        raise FileNotFoundError(f"Source not found: {root}")
    return sorted(p for p in root.rglob("*") if p.is_file())


def apply_marker_section(
    target_path: Path,
    rendered_content: str,
    start_marker: str,
    end_marker: str,
) -> None:
    """Write rendered_content into the region delimited by markers.

    - If the target file does not exist: write rendered_content.
    - If markers exist in the target: replace from the start of the start_marker
      line through the end of the end_marker line.
    - If markers do not exist: append rendered_content (with separating blank line).

    The rendered_content itself MUST contain both markers; this function preserves
    everything outside them.
    """
    target_path.parent.mkdir(parents=True, exist_ok=True)
    if not target_path.exists():
        target_path.write_text(rendered_content, encoding="utf-8")
        return

    existing = target_path.read_text(encoding="utf-8")
    if start_marker in existing and end_marker in existing:
        start_idx = existing.find(start_marker)
        end_idx = existing.find(end_marker, start_idx)
        if end_idx == -1:
            # Malformed: only start marker present. Append.
            sep = _join_sep(existing)
            target_path.write_text(existing + sep + rendered_content, encoding="utf-8")
            return
        end_idx += len(end_marker)
        # Extend to the end of the line containing the end marker
        line_end = existing.find("\n", end_idx)
        if line_end != -1:
            end_idx = line_end + 1
        new_text = existing[:start_idx] + rendered_content
        if not new_text.endswith("\n"):
            new_text += "\n"
        new_text += existing[end_idx:]
        target_path.write_text(new_text, encoding="utf-8")
    else:
        sep = _join_sep(existing)
        target_path.write_text(existing + sep + rendered_content, encoding="utf-8")


def _join_sep(existing: str) -> str:
    """Choose the separator between existing content and an appended block."""
    if existing.endswith("\n\n"):
        return ""
    if existing.endswith("\n"):
        return "\n"
    return "\n\n"
