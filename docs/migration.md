# Migration Guide

How to bring up the constitution on a new work machine, regardless of OS.

## Prerequisites

- **Git** installed.
- **Python 3.8 or newer** on PATH.
  - macOS: `brew install python3` (or use `python3` shipped since macOS 11)
  - Linux: `sudo apt install python3 python3-pip` (or distro equivalent)
  - Windows: `winget install Python.Python.3.12` or download from python.org
- **Network** for the first install (to clone the repo and pip-install PyYAML).
  After bootstrap, no network is required for daily install/verify/update.

## First-Time Setup on a New Machine

### 1. Clone

```bash
git clone https://github.com/<you>/ai-workspace-constitution
cd ai-workspace-constitution
```

### 2. Choose your workspace root

The "workspace root" is the directory where your AI coding repos live (and
where this constitution will materialise the top-level `AGENTS.md`,
`CLAUDE.md`, etc.).

Examples:
- macOS: `/Users/me/projects/agents`
- Linux: `/home/me/projects/agents`
- Windows: `D:\projects\agents`

### 3. (Optional) Per-machine overrides

```bash
cp manifests/machine.example.yaml manifests/machine.local.yaml
# Edit manifests/machine.local.yaml — set absolute workspace_root,
# disable Windows-only components on Mac, etc.
```

`machine.local.yaml` is gitignored.

### 4. Install

#### macOS / Linux

```bash
WORKSPACE_ROOT=/Users/me/projects/agents ./scripts/install.sh
```

#### Windows (PowerShell)

```powershell
$env:WORKSPACE_ROOT = "D:\projects\agents"
.\scripts\install.ps1
```

The installer will:

1. Find Python 3.8+.
2. Bootstrap PyYAML via `pip install --user --quiet pyyaml` if missing.
3. Read `manifests/default.yaml` (and `machine.local.yaml` if present).
4. Render every `*.tmpl` with your variables.
5. Back up any existing files at the targets to `*.backup.<UTC-stamp>`.
6. Write the new files.
7. Save `$WORKSPACE_ROOT/.constitution-state.json` with hashes.

A typical first install writes ~21 files in 2-3 seconds.

### 5. Bootstrap plugins

The constitution does **not** install ECC / OMC / superpowers / claude-mem /
memsearch — they have their own installers. See
[`plugin-bootstrap.md`](plugin-bootstrap.md) for the chained install steps
on a fresh machine.

### 6. Verify

```bash
./scripts/verify.sh        # macOS / Linux
.\scripts\verify.ps1       # Windows
```

Expected output:

```text
[constitution] Files in state: 21
[constitution] OK: 21
[constitution] Verification PASSED
```

## Daily / Periodic Commands

```bash
# Pull latest constitution from GitHub, re-render, verify.
./scripts/update.sh

# Quick health check without pulling.
./scripts/verify.sh

# Check whether upstream provider docs (Anthropic / OpenAI / Google / MCP / …)
# changed since last snapshot. Read-only.
./scripts/upstream-watch.sh --check

# After reviewing the diff, capture the new snapshots so future --check
# runs only highlight what's new again.
./scripts/upstream-watch.sh --apply
```

The PowerShell equivalents are `update.ps1`, `verify.ps1`, `upstream-watch.ps1`.

## Authoring Changes (Same or Different Machine)

The constitution is yours; you edit it directly.

```bash
# Edit governance/, then:
git add governance/...
git commit -m "feat(governance): tighten guardrail X"
git push
```

On any other machine:

```bash
./scripts/update.sh   # pulls and re-renders
```

When you make a meaningful change:

1. Bump `VERSION` (SemVer: bump patch for fixes, minor for new content,
   major for breaking re-organisation).
2. Move the new content from the `[Unreleased]` section of `CHANGELOG.md`
   into a versioned section.
3. Tag: `git tag v0.2.0 && git push --tags`.

## Troubleshooting

### `Python 3.8+ not found`

Install per the prerequisites above and reopen your terminal so PATH is refreshed.

### `PyYAML not installed`

The wrapper auto-bootstraps. If it fails (proxy / corporate firewall):

```bash
python3 -m pip install --user pyyaml
# or download the wheel manually from pypi.org and:
python3 -m pip install --user pyyaml-*.whl
```

### `WORKSPACE_ROOT is required`

Either pass `--workspace-root /path` to the installer, set the environment
variable, or set `paths.workspace_root` in `manifests/machine.local.yaml`.

### Verify reports drift after a routine plugin update

Most likely the OMC block of `~/.claude/CLAUDE.md` changed (OMC self-updates
its block). The marker-section verifier should ignore content outside our
markers; if it doesn't, file a bug — that's a verifier regression.

For ordinary `.codex/config.toml` or workspace `.md` drift: someone (you, an
agent, or a tool) edited the file directly. Decide:

- Was the edit intentional? Update the **template** in `governance/`,
  re-install, commit.
- Was it accidental? Re-install (`./scripts/update.sh --no-pull`) to overwrite.

### Failed `git pull --ff-only`

You committed locally on this machine and it diverged from the remote. Run
`git status`, decide whether to push or rebase, then re-run `update.sh`.

## Removing the Constitution from a Machine

Deletion is manual for now (the state file enumerates exactly which paths to
remove):

```bash
python3 -c "
import json, sys
from pathlib import Path
state = json.loads(Path(sys.argv[1]).read_text())
for path in state['files']:
    p = Path(path)
    if p.exists():
        print(f'rm {p}')
" /path/to/workspace/.constitution-state.json
```

Review the output, then remove the files and the `.constitution-state.json`.
For marker-section files, also remove the section between
`<!-- USER:CONSTITUTION:START -->` and `<!-- USER:CONSTITUTION:END -->`.

(A formal `uninstall.sh` is a TODO for v0.2.0.)
