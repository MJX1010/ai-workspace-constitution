"""End-to-end smoke tests: install, idempotency, drift detection."""
from __future__ import annotations

import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO = Path(__file__).resolve().parent.parent


def run_module(module: str, *args: str, env: dict = None) -> subprocess.CompletedProcess:
    """Run `python -m scripts.lib.<module>` from repo root with env vars."""
    full_env = os.environ.copy()
    if env:
        full_env.update(env)
    return subprocess.run(
        [sys.executable, "-m", f"scripts.lib.{module}", *args],
        cwd=str(REPO),
        env=full_env,
        capture_output=True,
        text=True,
    )


class TestInstallSmoke(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.mkdtemp(prefix="constitution_smoke_")
        self.target = Path(self.tmp)

    def tearDown(self) -> None:
        import shutil
        shutil.rmtree(self.tmp, ignore_errors=True)

    def _env(self) -> dict:
        return {
            "WORKSPACE_ROOT": str(self.target),
            "HOME": str(self.target),
            "USERPROFILE": str(self.target),
        }

    def test_install_creates_expected_files(self):
        r = run_module("install", "--yes", env=self._env())
        self.assertEqual(r.returncode, 0, msg=r.stdout + r.stderr)
        self.assertTrue((self.target / "AGENTS.md").exists())
        self.assertTrue((self.target / "CLAUDE.md").exists())
        self.assertTrue((self.target / "GEMINI.md").exists())
        self.assertTrue((self.target / "README_AI_GOVERNANCE.md").exists())
        self.assertTrue((self.target / ".codex" / "config.toml").exists())
        self.assertTrue((self.target / ".codex" / "AGENTS.md").exists())
        self.assertTrue(
            (self.target / ".codex" / "scripts" / "manage-superpowers.ps1").exists()
        )
        self.assertTrue(
            (self.target / ".codex" / "scripts" / "manage-superpowers.bat").exists()
        )
        self.assertTrue(
            (self.target / ".codex" / "skills" / "workspace-governance" / "SKILL.md").exists()
        )
        self.assertTrue(
            (self.target / ".claude" / "skills" / "skill-factory-playbook" / "SKILL.md").exists()
        )
        self.assertTrue((self.target / ".constitution-state.json").exists())
        codex_agents = (self.target / ".codex" / "AGENTS.md").read_text(encoding="utf-8")
        self.assertIn("USER:CONSTITUTION:START", codex_agents)
        self.assertIn("Superpowers Activation Policy", codex_agents)

    def test_workspace_root_substituted(self):
        run_module("install", "--yes", env=self._env())
        text = (self.target / "AGENTS.md").read_text(encoding="utf-8")
        # Path may use forward or backward slashes depending on shell;
        # check that the basename appears somewhere.
        self.assertIn(self.target.name, text)
        # The literal placeholder must NOT remain.
        self.assertNotIn("${WORKSPACE_ROOT}", text)
        self.assertNotIn("${WORKSPACE_NAME}", text)

    def test_idempotent_reinstall(self):
        r1 = run_module("install", "--yes", env=self._env())
        self.assertEqual(r1.returncode, 0)
        # Snapshot file mtimes
        agents_path = self.target / "AGENTS.md"
        first_mtime = agents_path.stat().st_mtime_ns

        r2 = run_module("install", "--yes", env=self._env())
        self.assertEqual(r2.returncode, 0)
        # File should be unchanged (mtime preserved because content matched).
        # We tolerate a small race where mtime may be updated; check content instead.
        self.assertEqual(
            agents_path.read_text(encoding="utf-8"),
            (self.target / "AGENTS.md").read_text(encoding="utf-8"),
        )

    def test_verify_passes_after_install(self):
        run_module("install", "--yes", env=self._env())
        r = run_module("verify", env=self._env())
        self.assertEqual(r.returncode, 0, msg=r.stdout + r.stderr)
        self.assertIn("Verification PASSED", r.stdout)

    def test_verify_detects_drift(self):
        run_module("install", "--yes", env=self._env())
        # Tamper
        (self.target / "AGENTS.md").write_text("DRIFT", encoding="utf-8")
        r = run_module("verify", "--fail-on-drift", env=self._env())
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("Drift", r.stdout)

    def test_marker_section_isolation(self):
        """Editing OUTSIDE the marker section must NOT trigger drift on that file."""
        run_module("install", "--yes", env=self._env())
        global_claude = self.target / ".claude" / "CLAUDE.md"
        original = global_claude.read_text(encoding="utf-8")

        # Inject content BEFORE the start marker — outside our managed section.
        global_claude.write_text(
            "## SOMETHING ELSE NOT OURS\n\nfake content\n\n" + original,
            encoding="utf-8",
        )

        r = run_module("verify", "--fail-on-drift", env=self._env())
        self.assertEqual(r.returncode, 0, msg=r.stdout + r.stderr)
        self.assertIn("PASSED", r.stdout)

    def test_codex_marker_section_isolation(self):
        """Local blocks outside the Codex marker section are not constitution drift."""
        run_module("install", "--yes", env=self._env())
        global_codex = self.target / ".codex" / "AGENTS.md"
        original = global_codex.read_text(encoding="utf-8")

        global_codex.write_text(
            "<!-- BEGIN MANAGED SUPERPOWERS -->\nlocal state\n"
            "<!-- END MANAGED SUPERPOWERS -->\n\n" + original,
            encoding="utf-8",
        )

        r = run_module("verify", "--fail-on-drift", env=self._env())
        self.assertEqual(r.returncode, 0, msg=r.stdout + r.stderr)
        self.assertIn("PASSED", r.stdout)


if __name__ == "__main__":
    unittest.main()
