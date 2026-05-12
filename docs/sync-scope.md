# Sync Scope

This document records which local AI workspace surfaces belong in this
constitution and which must stay local, plugin-managed, or repo-owned.

## Synced by This Repo

These are user-authored, reusable, and safe to version:

- `governance/workspace/AGENTS.md.tmpl`
- `governance/workspace/CLAUDE.md.tmpl`
- `governance/workspace/GEMINI.md.tmpl`
- `governance/workspace/README_AI_GOVERNANCE.md.tmpl`
- `governance/workspace-config/codex.config.toml.tmpl`
- `governance/workspace-config/claude.settings.local.json.tmpl`
- `governance/workspace-skills/shared/**`
- `governance/workspace-skills/codex-only/manage-superpowers-whitelist/**`
- `governance/workspace-scripts/codex/manage-superpowers.ps1`
- `governance/workspace-scripts/codex/manage-superpowers.bat`
- `governance/global/claude/CLAUDE.md.partial.tmpl`
- `governance/global/codex/AGENTS.md.partial.tmpl`
- `manifests/default.yaml`
- `manifests/machine.example.yaml`
- `scripts/install.*`, `scripts/update.*`, `scripts/verify.*`, and `scripts/lib/**`
- `docs/architecture.md`, `docs/plugin-bootstrap.md`, `docs/update-policy.md`, `docs/migration.md`, `docs/sync-scope.md`, and ADRs
- `upstream/sources.yaml` and read-only upstream snapshots used for drift review
- `.editorconfig`, `.gitattributes`, `.gitignore`, `README.md`, `CHANGELOG.md`, `VERSION`, `LICENSE`

## Materialised Targets

The installer writes the synced sources to these target paths:

- `${WORKSPACE_ROOT}/AGENTS.md`
- `${WORKSPACE_ROOT}/CLAUDE.md`
- `${WORKSPACE_ROOT}/GEMINI.md`
- `${WORKSPACE_ROOT}/README_AI_GOVERNANCE.md`
- `${WORKSPACE_ROOT}/.codex/config.toml`
- `${WORKSPACE_ROOT}/.claude/settings.local.json`
- `${WORKSPACE_ROOT}/.codex/skills/**`
- `${WORKSPACE_ROOT}/.claude/skills/**`
- `${WORKSPACE_ROOT}/.codex/scripts/manage-superpowers.ps1`
- `${WORKSPACE_ROOT}/.codex/scripts/manage-superpowers.bat`
- `${HOME}/.claude/CLAUDE.md` between `<!-- USER:CONSTITUTION:START -->` and `<!-- USER:CONSTITUTION:END -->`
- `${HOME}/.codex/AGENTS.md` between `<!-- USER:CONSTITUTION:START -->` and `<!-- USER:CONSTITUTION:END -->`

## Deliberately Not Synced

These are secrets, machine state, runtime artifacts, third-party installs, or
repo-owned overlays:

- `${HOME}/.claude/.credentials.json`
- `${HOME}/.codex/auth.json`
- `${HOME}/.codex/cap_sid`
- `${HOME}/.claude/sessions/**`, `${HOME}/.codex/sessions/**`
- `${HOME}/.claude/history.jsonl`, `${HOME}/.codex/history.jsonl`
- `${HOME}/.claude/cache/**`, `${HOME}/.codex/log/**`
- `${HOME}/.claude/projects/**`
- `${HOME}/.claude/todos/**`
- `${HOME}/.claude/telemetry/**`
- `${HOME}/.claude/file-history/**`
- `${HOME}/.codex/state_*.sqlite*`, `${HOME}/.codex/logs_*.sqlite*`
- `${HOME}/.codex/.sandbox*/**`
- `${HOME}/.claude/plugins/**`
- `${HOME}/.claude/rules/**`
- `${HOME}/.claude/ecc/**`
- `${HOME}/.claude/.omc/**`
- `${HOME}/.codex/superpowers/**`
- `${HOME}/.agents/skills/superpowers/**`
- repository-local `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `.codex/**`, and `.claude/**` under child repos
- any `machine.local.yaml`, `.env*`, `*.key`, `*.pem`, backup, cache, or generated state file

## Decision Rule

Sync only user-authored templates, scripts, skills, manifests, and documents
that are stable across machines. Keep secrets, logs, sessions, caches,
plugin-managed content, generated files, and child-repo overlays out of this
repo.
