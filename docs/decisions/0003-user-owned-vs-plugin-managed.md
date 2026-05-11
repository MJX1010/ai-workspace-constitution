# ADR-0003: User-owned vs plugin-managed content separation

## Status

Accepted — 2026-04-29

## Context

When extracting the existing rules from the live workspace, the directories
under `~/.claude/` and the OMC block of `~/.claude/CLAUDE.md` were full
of content that was **not authored by the user**. It was installed by
plugins (Everything Claude Code, oh-my-claudecode, superpowers) and is
maintained on its own update cycle.

Two reasonable strategies existed:

1. **Snapshot everything** into `governance/`, install verbatim. The
   constitution becomes a complete single-shot reproduction of the live
   environment.
2. **Carry only user-authored content.** Treat plugin content as out-of-scope;
   document the install commands instead.

## Decision

Use strategy 2: only the user's actual authored content lives in
`governance/`.

- **Workspace level**: `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`,
  `README_AI_GOVERNANCE.md`, the two workspace skills
  (`workspace-governance`, `skill-factory-playbook`), `.codex/config.toml`,
  `.claude/settings.local.json`, plus the Codex+Windows-only
  `manage-superpowers-whitelist` skill.
- **Global level (`~/.claude/`)**: only the user-authored sections of
  `CLAUDE.md` (Environment Correction + Issue Investigation Discipline),
  inserted via marker section so it never collides with the OMC block
  or future plugin content.

The constitution does **not** copy:
- ECC's `~/.claude/AGENTS.md`
- ECC's `~/.claude/rules/` tree
- The OMC block of `~/.claude/CLAUDE.md`
- The internals of superpowers, claude-mem, memsearch

`docs/plugin-bootstrap.md` lists the chained install commands that restore
those on a fresh machine.

## Consequences

**Good:**
- The repo stays small (~120 KB instead of multi-MB).
- Plugin upgrades don't trigger constitution version bumps.
- No license risk from redistributing third-party plugin content.
- The git diff of `governance/` is always meaningful — it represents
  *the user's* thinking, not transient plugin churn.

**Bad:**
- A fresh machine needs multiple install steps:
  constitution → ECC → OMC → marketplace plugins. Documented but more
  steps than a single shot.
- If a plugin disappears upstream, the constitution alone won't bring
  back its content. (Mitigation: `upstream/` snapshots ECC / OMC
  READMEs so we at least keep historical references.)

## Alternatives considered

- **Full snapshot.** Mirror everything into `governance/`. Rejected:
  every plugin release would break verify; license unclear for verbatim
  redistribution; the constitution's intent (capture *user* judgment)
  gets diluted.
- **Submodule approach.** `git submodule add` ECC, OMC, etc. Rejected:
  submodules are operationally awkward and the user already has these
  cloned elsewhere on the machine.

## Revisit if

- A critical plugin disappears from its upstream and we lose the install
  channel. At that point, archive a known-good copy of the plugin in
  `upstream/<plugin>/snapshot/` and document a manual install fallback.
