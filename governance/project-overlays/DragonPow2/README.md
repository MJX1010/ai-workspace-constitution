# DragonPow2 Project Overlay

This overlay versions the DragonPow2 repo-owned AI governance files without
mixing DragonPow2-specific Unity, protocol, or mock rules into the generic
workspace governance layer.

## Installed Targets

- `root/AGENTS.md.tmpl` -> `${DRAGONPOW2_ROOT}/AGENTS.md`
- `root/CLAUDE.md.tmpl` -> `${DRAGONPOW2_ROOT}/CLAUDE.md`
- `agent-docs/` -> `${DRAGONPOW2_ROOT}/governance/agent-docs/`
- `scripts/` -> `${DRAGONPOW2_ROOT}/scripts/`

`${DRAGONPOW2_ROOT}` defaults to `${WORKSPACE_ROOT}/DragonPow2`. Override
`paths.dragonpow2_root` in `manifests/machine.local.yaml` when a machine uses a
different checkout path.

## Update Workflow

1. Edit the source templates under `agent-docs/`.
2. Materialise them in the DragonPow2 checkout with
   `${DRAGONPOW2_ROOT}/scripts/sync-agent-docs.ps1`.
3. Refresh `root/AGENTS.md.tmpl` and `root/CLAUDE.md.tmpl` from the generated
   `${DRAGONPOW2_ROOT}/AGENTS.md` and `${DRAGONPOW2_ROOT}/CLAUDE.md`.
4. Run `${DRAGONPOW2_ROOT}/scripts/check-agent-docs.ps1 -IncludeRoot`.
