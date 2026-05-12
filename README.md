# AI Workspace Constitution (`__ai_law`)

Personal, version-controlled **constitution** for an AI coding workspace.
One repository to install, update, and verify the same rules across
**Windows / macOS / Linux** machines.

## Why This Exists

Three years of AI coding rules, skills, and harness configs accumulated
locally across multiple boxes. Every new machine meant manually copying
scattered files, sometimes with stale paths.

This repo is the single source of truth:

- The **constitution** (rules, skills, configs) lives here as templates.
- A thin installer **renders** them at the right paths on each machine.
- A local **updater** pulls upstream provider doc changes into a CHANGELOG.
- Every iteration is a versioned, audited git commit.

## Quick Start

### macOS / Linux

```bash
git clone https://github.com/<you>/ai-workspace-constitution
cd ai-workspace-constitution
WORKSPACE_ROOT=/Users/me/projects/agents ./scripts/install.sh
```

### Windows (PowerShell)

```powershell
git clone https://github.com/<you>/ai-workspace-constitution
cd ai-workspace-constitution
$env:WORKSPACE_ROOT = "D:\projects\agents"
.\scripts\install.ps1
```

### Daily Commands

```bash
./scripts/verify.sh    # Hash-check installed files match the active version
./scripts/update.sh    # git pull, re-render, append CHANGELOG entry
# git push is always manual — no CI auto-pushes from this repo
```

## Layout

```text
__ai_law/
├── governance/                # USER-OWNED constitution
│   ├── workspace/             # → $WORKSPACE_ROOT/{AGENTS,CLAUDE,GEMINI,README_AI_GOVERNANCE}.md
│   ├── workspace-skills/      # → $WORKSPACE_ROOT/.{codex,claude}/skills/
│   ├── workspace-config/      # → $WORKSPACE_ROOT/.{codex/config.toml, claude/settings.local.json}
│   └── global/                # → ~/.claude/, ~/.codex/, etc. (only user-authored sections)
├── upstream/                  # READ-ONLY snapshots
│   ├── sources.yaml           # what to watch (Anthropic / OpenAI / Google / MCP / ECC / OMC / …)
│   ├── docs/                  # snapshots of official provider documentation
│   └── {ecc,omc,superpowers,claude-mem,memsearch}/  # plugin content snapshots (recovery only)
├── scripts/                   # install / update / verify / uninstall (Bash + PowerShell)
│   └── lib/                   # render, upstream-fetch, changelog helpers
├── manifests/
│   ├── default.yaml           # default install profile
│   └── machine.example.yaml   # per-machine override template (gitignored when used)
├── docs/                      # architecture, migration, update policy, ADRs, plugin bootstrap
├── tests/                     # render + idempotency checks
├── README.md / CHANGELOG.md / VERSION / LICENSE
├── .gitignore / .gitattributes / .editorconfig
└── .git/
```

## Design Principles

| # | Rule | Why |
|---|---|---|
| 1 | **User-owned only in `governance/`** | Plugin content (ECC, OMC, superpowers) is restored by re-running their official installers. Copying it here would mean re-syncing on every plugin release. |
| 2 | **Templates over hard paths** | `${WORKSPACE_ROOT}`, `${HOME}`, `${USER}` placeholders. The renderer materialises them per-machine. |
| 3 | **No CI push** | `update.sh` runs locally on demand. The `git push` step is always manual. |
| 4 | **SemVer + Keep-a-Changelog** | Every iteration is a versioned, reviewable commit. `Upstream` section in CHANGELOG records doc drifts. |
| 5 | **Idempotent install** | Re-running `install.sh` should be a no-op when state matches. Drift is detected by the installer hash check. |
| 6 | **Plugin bootstrap chained, not copied** | `docs/plugin-bootstrap.md` lists the install commands for ECC / OMC / superpowers / claude-mem / memsearch. The constitution invokes them; it doesn't try to be them. |

## Workflow

```text
   [edit governance/]
          │
          ▼
   git commit  ──►  git push   (manual)
          │
          ▼
   on another machine:
     git pull
     ./scripts/update.sh   ──►  re-renders, runs verify
                                 appends CHANGELOG diff if upstream snapshots changed
```

```text
   [upstream provider updates docs]
          │
   ./scripts/update.sh --check-upstream
          │
          ▼
   diff appears in upstream/docs/
          │
   you read it, decide what to absorb into governance/
          │
          ▼
   commit changes → CHANGELOG `Upstream` section auto-stamped
```

## What This Repo Is NOT

- Not a plugin — it does not declare itself to Claude Code, Codex, or Gemini as
  an installable extension. It just writes files.
- Not a package manager — it does not install ECC / OMC / superpowers itself.
  See `docs/plugin-bootstrap.md` for the chained install steps.
- Not a secret store — never commit API keys or paths to private filesystems.
  Use environment variables and `${VAR}` placeholders.

## Status

- Version: see [`VERSION`](./VERSION)
- History: see [`CHANGELOG.md`](./CHANGELOG.md)
- Architecture: see [`docs/architecture.md`](./docs/architecture.md)
- Migration to a new machine: see [`docs/migration.md`](./docs/migration.md)
- Plugin bootstrap (ECC / OMC / etc.): see [`docs/plugin-bootstrap.md`](./docs/plugin-bootstrap.md)
- Update policy (when and how to absorb upstream changes): see [`docs/update-policy.md`](./docs/update-policy.md)
- Sync scope (what is versioned vs ignored): see [`docs/sync-scope.md`](./docs/sync-scope.md)
