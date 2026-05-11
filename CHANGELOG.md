# Changelog

All notable changes to this constitution are documented in this file.

The format is based on [Keep a Changelog 1.1.0](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning 2.0.0](https://semver.org/spec/v2.0.0.html).

Entries are grouped under these section headings (in order):

- **Added** — new rules, skills, harness adapters, scripts.
- **Changed** — meaningful changes to existing rules / scripts.
- **Deprecated** — features still present but slated for removal.
- **Removed** — content removed in this release.
- **Fixed** — bug or rendering fixes.
- **Security** — security-relevant changes.
- **Upstream** — drifts pulled in from official provider docs (Anthropic, OpenAI, Google, MCP, Superpowers, ECC, etc.). Always include the source URL and the date the snapshot was taken.

## [Unreleased]

## [0.1.0] - 2026-04-29

### Added
- Initial scaffold extracted from the `Users\user9e2f966c\projects\agents-d62cea7574` workspace.
- `governance/workspace/` — top-level `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `README_AI_GOVERNANCE.md` as `${WORKSPACE_ROOT}`-templated files.
- `governance/workspace-skills/shared/` — `workspace-governance` and `skill-factory-playbook` skills (single source, installed into both `.codex/skills/` and `.claude/skills/`).
- `governance/workspace-skills/codex-only/manage-superpowers-whitelist/` — Codex-only, Windows-scoped skill (templated paths via `${USERPROFILE}` / `${HOME}`).
- `governance/workspace-config/` — `.codex/config.toml` and `.claude/settings.local.json` as templates.
- `governance/global/claude/CLAUDE.md.partial.tmpl` — only the user-authored sections (`Environment Correction`, `Issue Investigation Discipline`); plugin-managed regions are explicitly **not** included here.
- `upstream/` — placeholder for provider-doc and plugin-content snapshots used by the local watcher.
- `scripts/` — `install`, `update`, `verify`, `uninstall` entrypoints (Bash + PowerShell), backed by shared `scripts/lib/` helpers.
- `manifests/default.yaml` — default install profile selecting which harnesses to materialise.
- `docs/` — architecture, migration, update policy, plugin bootstrap, and ADRs.

### Changed
- Consolidated two divergent copies of `workspace-vibe-coding-guardrails.md` (one under `.claude/skills/`, one under `.codex/skills/`) into a single source. The newer Codex copy that includes the **Encoding Guardrail** section was kept as the canonical version.

### Notes
- Plugin-managed content is **not** copied verbatim into this repo. The following are restored on a fresh box by re-running their official installers (see `docs/plugin-bootstrap.md`), not by this repo:
  - ECC's `~/.claude/AGENTS.md` and `~/.claude/rules/` tree.
  - The OMC-managed block (`<!-- OMC:START -->` … `<!-- OMC:END -->`) inside `~/.claude/CLAUDE.md`.
  - `superpowers`, `claude-mem`, `memsearch` plugin internals.
- Snapshots may live under `upstream/` for diff and recovery purposes.

[Unreleased]: ../../compare/v0.1.0...HEAD
[0.1.0]: ../../releases/tag/v0.1.0
