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
- 新增工作区级 `repo_explorer` / `repo_worker` Codex 角色、受控 multi-agent 配置及项目配置同步脚本，默认限制为 2 个线程、1 层委派。
- 顶层与 DragonPow2 治理模板新增主 Agent 唯一沟通、SubAgent 局部上下文、精简回传和新 Chat 交接规则。
- `governance/project-overlays/DragonPow2/` for Git-backed DragonPow2 `AGENTS.md` / `CLAUDE.md`, agent-doc templates, and sync/check scripts.
- `governance/global/codex/AGENTS.md.partial.tmpl` for the user-authored Codex home-level marker section and superpowers activation policy.
- `governance/workspace-scripts/codex/manage-superpowers.ps1` and `.bat` so the Windows Codex superpowers whitelist manager is versioned and installed from the constitution.
- `governance/workspace-skills/shared/github-sync-commit/` for credential-safe GitHub commit/push workflows, mirrored into both Codex and Claude workspace skills.
- `governance/workspace-skills/shared/browser-doc-crawler/` for exporting logged-in browser documentation pages to local HTML/Markdown artifacts.
- `governance/workspace-skills/shared/karpathy-guidelines/` for lightweight coding/review/refactor behavior guardrails.
- `governance/workspace-config/claude-env/` for Claude plugin/settings recovery notes and scripts.
- `manifests/skills-lock.json` to pin external workspace skill sources and hashes.
- `governance/global/codex/agents/` and `governance/global/codex/skills/` for user-level Codex agent/skill snapshots, excluding bundled `.system` skills.
- `governance/global/{codex,claude}/mcp/mcp-servers.json` for MCP server templates with placeholders.
- Redacted Claude/Codex environment snapshots under `governance/global/` and `governance/environment-inventory/`.
- `docs/sync-scope.md` documenting synced paths, materialised targets, and deliberately ignored local/plugin/runtime surfaces.
- Chinese workspace structure and Agent Git-management inventory documents under `docs/`.

### Changed
- 工作区 AGENTS/CLAUDE 约束 Paseo 本地文件链接不得把行号写入 Markdown target，避免 Windows 将行号后缀当作文件名并触发 `ENOENT`。
- 工作区 handoff 统一落到 `${WORKSPACE_ROOT}/ai_handoff/<项目_模块_用途_日期>/`，并明确覆盖通用 handoff skill 的系统临时目录默认值。
- DragonPow2 skill authoring rules now require Chinese `SKILL.md` trigger descriptions and relative or placeholder paths instead of machine-local absolute project paths.
- DragonPow2 agent rules now require final responses after code/resource/config/doc changes to include a copyable suggested commit log for manual submission.
- DragonPow2 uLoop rules now treat unsaved scene/Prefab test blockers as save-and-rerun cases by default, including `Assets/Scenes/Init.unity` causing `Unity.Tests` to report 0 tests.
- DragonPow2 client uLoop rules now require `Unity.Tests` coverage and full `Unity.Tests` runs by default for non-trivial iterative client feature work.
- `manifests/default.yaml` now installs the DragonPow2 overlay to `${DRAGONPOW2_ROOT}`, defaulting to `${WORKSPACE_ROOT}/DragonPow2`.
- `manifests/default.yaml` now installs the Codex global marker section, Codex helper scripts, and the shared `github-sync-commit` skill.
- `manifests/default.yaml` now mirrors shared workspace skills into `.agents/skills` as well as Codex and Claude skill directories.
- `manifests/default.yaml` now restores user-level Codex agents, non-system Codex skills, and MCP config templates on new machines.
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
