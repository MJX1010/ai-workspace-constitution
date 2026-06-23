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
- `governance/workspace-config/claude-env/**`
- `governance/workspace-skills/shared/**`
- `governance/workspace-skills/codex-only/manage-superpowers-whitelist/**`
- `governance/workspace-scripts/codex/manage-superpowers.ps1`
- `governance/workspace-scripts/codex/manage-superpowers.bat`
- `governance/project-overlays/DragonPow2/**`
- `governance/global/claude/CLAUDE.md.partial.tmpl`
- `governance/global/claude/mcp/mcp-servers.json`
- `governance/global/claude/plugins/*.redacted.json`
- `governance/global/claude/settings/*.redacted.json`
- `governance/global/codex/AGENTS.md.partial.tmpl`
- `governance/global/codex/agents/**`
- `governance/global/codex/config/config.redacted.toml`
- `governance/global/codex/mcp/mcp-servers.json`
- `governance/global/codex/skills/**`
- `governance/global/superpowers/**`
- `governance/environment-inventory/*.redacted.json`
- `manifests/default.yaml`
- `manifests/machine.example.yaml`
- `manifests/skills-lock.json`
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
- `${WORKSPACE_ROOT}/.agents/skills/**`
- `${WORKSPACE_ROOT}/.codex/scripts/manage-superpowers.ps1`
- `${WORKSPACE_ROOT}/.codex/scripts/manage-superpowers.bat`
- `${WORKSPACE_ROOT}/.claude/env/**`
- `${WORKSPACE_ROOT}/skills-lock.json`
- `${HOME}/.codex/agents/**`
- `${HOME}/.codex/skills/**` except bundled `.system`
- `${HOME}/.codex/mcp-configs/mcp-servers.json`
- `${HOME}/.claude/mcp-configs/mcp-servers.json`
- `${DRAGONPOW2_ROOT}/AGENTS.md`
- `${DRAGONPOW2_ROOT}/CLAUDE.md`
- `${DRAGONPOW2_ROOT}/governance/agent-docs/**`
- `${DRAGONPOW2_ROOT}/scripts/sync-agent-docs.ps1`
- `${DRAGONPOW2_ROOT}/scripts/check-agent-docs.ps1`
- `${HOME}/.claude/CLAUDE.md` between `<!-- USER:CONSTITUTION:START -->` and `<!-- USER:CONSTITUTION:END -->`
- `${HOME}/.codex/AGENTS.md` between `<!-- USER:CONSTITUTION:START -->` and `<!-- USER:CONSTITUTION:END -->`

## Deliberately Not Synced

These are secrets, machine state, runtime artifacts, third-party installs, or
repo-owned overlays:

- `${HOME}/.claude/.credentials.json`
- `${HOME}/.codex/auth.json`
- `${HOME}/.codex/cap_sid`
- `${HOME}/.claude/settings.json` raw values, especially auth tokens and provider secrets
- `${HOME}/.codex/config.toml` raw machine runtime paths, native pipe IDs, hook trust state, and provider-local state
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
- `${HOME}/.codex/skills/.system/**`
- `${HOME}/.agents/skills/superpowers/**`
- repository-local `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `.codex/**`, and `.claude/**` under child repos, unless a specific repo overlay is explicitly declared under `governance/project-overlays/`
- any `machine.local.yaml`, `.env*`, `*.key`, `*.pem`, backup, cache, or generated state file

## Decision Rule

Sync only user-authored templates, scripts, skills, manifests, and documents
that are stable across machines. Keep secrets, logs, sessions, caches,
plugin-managed content, generated files, and undeclared child-repo overlays out
of this repo. If a child repo needs Git-backed AI governance, add a named
`governance/project-overlays/<repo>/` source so the project-specific boundary is
visible in review.
