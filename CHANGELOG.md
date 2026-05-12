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

### Added
- `governance/global/codex/AGENTS.md.partial.tmpl` for the user-authored Codex home-level marker section and superpowers activation policy.
- `governance/workspace-scripts/codex/manage-superpowers.ps1` and `.bat` so the Windows Codex superpowers whitelist manager is versioned and installed from the constitution.
- `docs/sync-scope.md` documenting synced paths, materialised targets, and deliberately ignored local/plugin/runtime surfaces.

### Changed
- `manifests/default.yaml` now installs the Codex global marker section and Codex helper scripts.
- `.gitignore` now excludes common AI harness runtime state if it is accidentally copied into the constitution repo.

## [0.2.0] - 2026-05-11

### Added
- `governance/workspace-skills/shared/feature-spec-workflow/` — new shared skill defining the per-feature `specs/<NNN-name>/{spec,plan,tasks}.md` convention. Triggered when starting a non-trivial change, resuming after a session break, or handling ambiguous requests. Mirrored into both `.codex/skills/` and `.claude/skills/`.
- `references/spec-template.md`, `plan-template.md`, `tasks-template.md` — fill-in templates an AI tool can copy into a new feature directory.
- `references/convention-sources.md` — provenance for the convention, citing GitHub Spec Kit, Kiro, BMAD, PRP, Superpowers, Anthropic Plan Mode, AGENTS.md, and the Feb-2026 ETH Zurich study on context files.

### Changed
- `governance/workspace/AGENTS.md.tmpl` — added `## Active Feature Tracking` section between `AI Vibe Coding Guardrails` and `Shared Governance Layout`. Tells any AI tool entering the workspace to check `specs/` before writing code and resume from the first unchecked task.
- `manifests/default.yaml` — `workspace_skills_codex` and `workspace_skills_claude` now also install `feature-spec-workflow`; `constitution.version` bumped to `0.2.0`.

### Notes
- The convention deliberately matches GitHub Spec Kit's directory layout so `/specify`, `/plan`, and `/tasks` slash commands work unmodified. Compatible with Kiro (`requirements.md` ≈ `spec.md`, `design.md` ≈ `plan.md`), ECC (`/prp-prd` → `/prp-plan` → `/prp-implement`), and Superpowers (`brainstorming` → `writing-plans` → `executing-plans`).
- No backwards-incompatible changes. Existing v0.1.0 installs upgrade cleanly via `./scripts/update.sh`.

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

[Unreleased]: ../../compare/v0.2.0...HEAD
[0.2.0]: ../../compare/v0.1.0...v0.2.0
[0.1.0]: ../../releases/tag/v0.1.0
