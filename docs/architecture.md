# Architecture

This document explains the design rationale behind the AI Workspace Constitution.
For ground-truth on individual decisions, see `docs/decisions/` (ADRs).

## Goal

A single, version-controlled source of truth for the author's AI coding rules,
skills, and harness configuration — installable on any of three OSes
(macOS / Linux / Windows) with one command, updatable on demand, and auditable
through git.

Non-goals:

- Replace plugin managers (ECC, OMC, claude-mem, etc.). Those have their own
  install lifecycles.
- Be a generic cross-team distribution mechanism. This is a personal repo.
- Provide automated CI push. The author owns the git workflow.

## Core Layout

```
__ai_law/
├── governance/      # USER-OWNED constitution (templates of .md / .toml / .json)
├── upstream/        # READ-ONLY snapshots of provider docs and plugin READMEs
├── manifests/       # What goes where, per-machine overrides
├── scripts/         # install / update / verify / upstream-watch (Bash + PowerShell + Python)
├── tests/           # unittest-based smoke + render tests
└── docs/            # This file plus migration / policy / ADRs
```

Three orthogonal layers:

1. **What to install** — `governance/` plus `manifests/`.
2. **How to install** — `scripts/` plus templates with `${VAR}` placeholders.
3. **What changed upstream** — `upstream/` plus `scripts/upstream-watch`.

## User-Owned vs Plugin-Managed

The repo only carries content the **author writes**. Content installed and
maintained by other tools is referenced but not duplicated:

| Source | Treatment |
|---|---|
| Workspace `AGENTS.md`, `CLAUDE.md`, `GEMINI.md` | Templated under `governance/workspace/`, written verbatim on install. |
| Workspace skills `workspace-governance`, `skill-factory-playbook` | Templated under `governance/workspace-skills/shared/`, mirrored to both `.codex/skills/` and `.claude/skills/`. |
| `~/.claude/AGENTS.md` (ECC plugin file) | **Not copied.** ECC's installer recreates it. See `docs/plugin-bootstrap.md`. |
| `~/.claude/rules/*` (ECC plugin tree) | **Not copied.** Same reason. |
| OMC block in `~/.claude/CLAUDE.md` | **Not touched.** OMC's plugin manages it between `<!-- OMC:START -->` and `<!-- OMC:END -->`. |
| User-authored sections of `~/.claude/CLAUDE.md` | Templated under `governance/global/claude/CLAUDE.md.partial.tmpl`, inserted via marker section into the live file. |
| superpowers, claude-mem, memsearch | **Not copied.** Their plugins are installed by the user; only the *whitelist* skill (Windows + Codex) is part of governance. |

ADR-0003 expands this rule.

## Template Syntax

Pure `${VAR}` substitution, multi-pass to handle nested references.

- `${WORKSPACE_ROOT}` — required, set per machine.
- `${WORKSPACE_NAME}` — auto-derived from `WORKSPACE_ROOT`'s basename.
- `${HOME}` / `${USERPROFILE}` — auto-detected.
- `${USER}` — from environment.
- `${CONSTITUTION_VERSION}` — read from `VERSION`.

No Jinja2 or Handlebars. ADR-0001 explains why simple substitution beats a
real templating engine for this use case.

## Install / Update / Verify Flow

```
                    ┌────────────────────────────┐
                    │  github: ai-workspace-...  │
                    └─────────────┬──────────────┘
                                  │ git clone (first machine)
                                  │ git pull   (subsequent updates)
                                  ▼
              ┌─────────────────────────────────────┐
              │   <repo>/governance/  +  manifests/  │
              └────────────────┬─────────────────────┘
                               │
                               │ install.sh / install.ps1
                               │ (loads default.yaml + machine.local.yaml)
                               │ renders ${VAR} placeholders
                               ▼
                  ┌──────────────────────────────┐
                  │   $WORKSPACE_ROOT/AGENTS.md  │
                  │   $WORKSPACE_ROOT/.codex/... │
                  │   $WORKSPACE_ROOT/.claude/.. │
                  │   $HOME/.claude/CLAUDE.md    │
                  │   .constitution-state.json   │
                  └──────────────────────────────┘
                               │
                               │ verify.sh / verify.ps1
                               │ (re-hash and compare against state)
                               ▼
                       OK / DRIFT / MISSING
```

## Cross-Platform Strategy

ADR-0002. In short:

- **Python 3.8+** for actual logic. Cross-platform out of the box.
- **Bash + PowerShell** as thin wrappers (~50 LOC each) that find Python and
  delegate. PyYAML is bootstrapped via `pip --user` on first run.
- **No** Node.js / Ruby / Go / compiled binaries.
- **Path handling**: `pathlib.Path` everywhere; templates use forward slashes
  for paths that go into doc text (works on all OSes); native separators only
  for actual filesystem operations (`pathlib` handles this transparently).

## State File

`$WORKSPACE_ROOT/.constitution-state.json` records:

```json
{
  "constitution_version": "0.1.0",
  "installed_at": "2026-04-29T13:23:00Z",
  "updated_at":   "2026-04-29T13:23:00Z",
  "files": {
    "<absolute_path>": {
      "sha256": "<hex>",
      "source": "governance/...",
      "component": "<manifest_component_name>",
      "mode": "replace" | "marker-section",
      "marker_start": "<only for marker-section>",
      "marker_end": "<only for marker-section>",
      "updated_at": "..."
    },
    ...
  }
}
```

For `mode: replace`, the SHA-256 is over the **whole file**. For
`mode: marker-section`, it is over the **rendered section content** between
markers, so unrelated edits outside markers (e.g. OMC block updates) do not
register as drift.

## Why Not …

- **A Claude Code plugin** — Plugins target installation into `~/.claude/plugins/`,
  but this repo wants to govern *both* `~/.claude/` and the workspace at
  `$WORKSPACE_ROOT/`. A plain installer is simpler.
- **dotfiles + chezmoi/yadm** — Those tools handle home directory only;
  governance also targets the workspace root and may target multiple workspaces
  on the same machine.
- **A Bash-only installer** — YAML parsing, HTTP fetching for upstream, hash
  computation, and JSON state are all painful in pure Bash. Doable, but the
  maintenance cost is much higher than a small Python codebase.
- **GitHub Actions for upstream watching** — The author wants manual `git pull`
  / `git push`, not a scheduled bot. Local `upstream-watch.sh` runs on demand.
  ADR-0004 expands.

See `docs/decisions/` for full rationale on each.
