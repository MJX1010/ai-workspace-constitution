"""Unit tests for template rendering primitives."""
from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from scripts.lib.common import resolve_vars
from scripts.lib.render import (
    apply_marker_section,
    render_file,
    render_text,
    strip_tmpl_suffix,
)


class TestResolveVars(unittest.TestCase):
    def test_simple(self):
        self.assertEqual(
            resolve_vars("hello ${NAME}", {"NAME": "world"}),
            "hello world",
        )

    def test_multiple(self):
        self.assertEqual(
            resolve_vars("${A}/${B}", {"A": "foo", "B": "bar"}),
            "foo/bar",
        )

    def test_missing_left_alone(self):
        self.assertEqual(
            resolve_vars("hello ${UNKNOWN}", {"NAME": "x"}),
            "hello ${UNKNOWN}",
        )

    def test_nested(self):
        # First pass replaces ${A}, second pass replaces ${B}
        self.assertEqual(
            resolve_vars("${A}", {"A": "${B}", "B": "final"}),
            "final",
        )

    def test_no_placeholder(self):
        self.assertEqual(resolve_vars("plain text", {"X": "y"}), "plain text")


class TestStripTmplSuffix(unittest.TestCase):
    def test_drops_tmpl(self):
        self.assertEqual(strip_tmpl_suffix(Path("a.md.tmpl")).name, "a.md")

    def test_keeps_non_tmpl(self):
        self.assertEqual(strip_tmpl_suffix(Path("a.md")).name, "a.md")


class TestRenderFile(unittest.TestCase):
    def test_render_template(self):
        with tempfile.TemporaryDirectory() as tmp:
            src = Path(tmp) / "x.md.tmpl"
            src.write_text("hello ${NAME}\n", encoding="utf-8")
            content, was_tmpl = render_file(src, {"NAME": "alice"})
            self.assertTrue(was_tmpl)
            self.assertEqual(content.decode("utf-8"), "hello alice\n")

    def test_copy_non_template(self):
        with tempfile.TemporaryDirectory() as tmp:
            src = Path(tmp) / "x.md"
            src.write_bytes(b"hello ${NAME}\n")
            content, was_tmpl = render_file(src, {"NAME": "alice"})
            self.assertFalse(was_tmpl)
            self.assertEqual(content, b"hello ${NAME}\n")  # NOT substituted


class TestApplyMarkerSection(unittest.TestCase):
    START = "<!-- USER:START -->"
    END = "<!-- USER:END -->"

    def test_new_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            tgt = Path(tmp) / "f.md"
            content = f"{self.START}\nhello\n{self.END}\n"
            apply_marker_section(tgt, content, self.START, self.END)
            self.assertEqual(tgt.read_text(encoding="utf-8"), content)

    def test_existing_with_markers_replaces(self):
        with tempfile.TemporaryDirectory() as tmp:
            tgt = Path(tmp) / "f.md"
            tgt.write_text(
                f"OUTSIDE BEFORE\n{self.START}\nold\n{self.END}\nOUTSIDE AFTER\n",
                encoding="utf-8",
            )
            apply_marker_section(
                tgt, f"{self.START}\nnew\n{self.END}\n",
                self.START, self.END,
            )
            text = tgt.read_text(encoding="utf-8")
            self.assertIn("OUTSIDE BEFORE", text)
            self.assertIn("OUTSIDE AFTER", text)
            self.assertIn(f"{self.START}\nnew\n{self.END}", text)
            self.assertNotIn("old", text)

    def test_existing_without_markers_appends(self):
        with tempfile.TemporaryDirectory() as tmp:
            tgt = Path(tmp) / "f.md"
            tgt.write_text("preserved\n", encoding="utf-8")
            section = f"{self.START}\nnew\n{self.END}\n"
            apply_marker_section(tgt, section, self.START, self.END)
            text = tgt.read_text(encoding="utf-8")
            self.assertTrue(text.startswith("preserved"))
            self.assertIn(self.START, text)
            self.assertIn(self.END, text)


if __name__ == "__main__":
    unittest.main()
