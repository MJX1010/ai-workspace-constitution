# Plugin Bootstrap

The constitution itself does **not** install Claude Code, Codex, or their
plugins. This document lists the install commands for the plugins this
constitution assumes are present on a fresh machine.

> All commands and URLs in this file are tracked by `upstream-watch` so that
> drift in any of these install procedures is surfaced. If something below is
> stale, run `./scripts/upstream-watch.sh --check` and update accordingly.

## Required Layer 0: Harnesses

| Harness | Install reference |
|---|---|
| **Claude Code** | https://docs.claude.com/en/docs/claude-code/quickstart |
| **OpenAI Codex CLI** | https://developers.openai.com/codex/cli — `npm install -g @openai/codex` (or the latest documented method) |
| **Gemini CLI** (optional) | https://github.com/google-gemini/gemini-cli |

The constitution targets `${WORKSPACE_ROOT}/AGENTS.md`, `CLAUDE.md`, and
`GEMINI.md` regardless of which subset is actually installed. Unused files
are harmless.

## Layer 1: Claude Code plugins enabled by `claude.settings.local.json`

The rendered `${WORKSPACE_ROOT}/.claude/settings.local.json` declares:

```json
{
  "enabledPlugins": {
    "claude-mem@thedotmack": true,
    "memsearch@memsearch-plugins": true,
    "superpowers@claude-plugins-official": true
  }
}
```

These plugins must be installed via Claude Code's marketplace before they
can be enabled.

### superpowers (Anthropic-blessed agentic skills framework)

```text
/plugin add superpowers@claude-plugins-official
```

Repository: https://github.com/obra/superpowers
Marketplace metadata: comes pre-configured with the official Anthropic
marketplace.

### claude-mem (cross-session memory)

```text
/plugin add claude-mem@thedotmack
```

Repository: https://github.com/thedotmack/claude-mem
Note: as of February 2026, a community audit flagged claude-mem's local
HTTP API on port 37777 as having no authentication. If your machine sits on
a hostile network, either firewall the port or rely on `memsearch` only.

### memsearch (Markdown-backed memory)

```text
/plugin add memsearch@memsearch-plugins
```

Repository: https://github.com/zilliztech/memsearch

## Layer 2: Everything Claude Code (ECC)

ECC ships the global `~/.claude/AGENTS.md` and `~/.claude/rules/*` tree that
this constitution intentionally does **not** carry.

```bash
# As of v0.1.0 of this constitution, ECC's canonical install is:
#   1. Clone the repo
git clone https://github.com/affaan-m/everything-claude-code

#   2. Run its installer
cd everything-claude-code
./install.sh        # macOS / Linux
# or
.\install.ps1       # Windows
```

After this:
- `~/.claude/AGENTS.md` will be the ECC-managed file.
- `~/.claude/rules/{common,zh,web,...}` will be populated.
- 47+ agents, 180+ skills, 79+ commands become available.

When ECC releases a new version, re-run its installer. The constitution does
not interfere — it only manages the *workspace*-level files and the user
section of `~/.claude/CLAUDE.md`.

## Layer 3: oh-my-claudecode (OMC)

OMC manages the orchestration block inside `~/.claude/CLAUDE.md` between
`<!-- OMC:START -->` and `<!-- OMC:END -->`. The constitution writes its own
section between `<!-- USER:CONSTITUTION:START -->` and
`<!-- USER:CONSTITUTION:END -->`, so the two coexist.

```bash
# Install reference (see upstream/omc/README.md snapshot for the latest):
# Typical pattern:
#   1. Run OMC's installer in any session by saying "setup omc"
#   2. Or invoke /oh-my-claudecode:omc-setup if the slash command is registered
```

After OMC is installed, re-running `./scripts/install.sh` will re-insert the
constitution's user section without disturbing OMC's block.

## Layer 4: Codex superpowers whitelist (Windows + Codex only)

This is the only plugin **content** the constitution itself ships, because
the whitelist semantics depend on local junctions and a desktop shortcut
that aren't in the upstream superpowers repo.

```powershell
# After install.ps1 has materialised the workspace skill, the script lives at:
${WORKSPACE_ROOT}\.codex\scripts\manage-superpowers.ps1

# List enabled:
powershell -ExecutionPolicy Bypass -File ${WORKSPACE_ROOT}\.codex\scripts\manage-superpowers.ps1 -ListOnly

# Set whitelist (must pass the FULL desired set):
powershell -ExecutionPolicy Bypass -File ${WORKSPACE_ROOT}\.codex\scripts\manage-superpowers.ps1 -SetEnabled brainstorming systematic-debugging writing-plans
```

(The skill `manage-superpowers-whitelist` lives at
`governance/workspace-skills/codex-only/`.)

The script is authored by this constitution at
`governance/workspace-scripts/codex/manage-superpowers.ps1` and is installed
into the workspace. It updates only the local superpowers junctions and the
managed superpowers block in `~/.codex/AGENTS.md`; it does not vendor the
upstream `superpowers` plugin content.

## Verification

After all layers are in place, run:

```bash
./scripts/verify.sh
```

Then sanity-check each harness:

- Claude Code: `claude --version` and start a session — confirm
  `superpowers`, `claude-mem`, `memsearch` are listed in available plugins.
- Codex: `codex --version` and confirm `~/.codex/AGENTS.md` references the
  managed superpowers whitelist block.
- Gemini CLI: open the workspace and confirm `GEMINI.md` is read.

## When a Plugin Updates

The constitution does **not** track plugin internal versions. Re-run the
plugin's own installer when you want to update it. Examples:

```bash
# ECC
cd <wherever you cloned everything-claude-code>
git pull && ./install.sh   # or .\install.ps1

# Claude marketplace plugins
/plugin update superpowers@claude-plugins-official
/plugin update claude-mem@thedotmack
/plugin update memsearch@memsearch-plugins
```

If a plugin's behaviour changes in a way that affects governance (new flags,
new file conventions), reflect that in `governance/` and bump
`VERSION` + `CHANGELOG.md`.
