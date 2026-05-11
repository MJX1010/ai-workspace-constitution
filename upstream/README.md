# Upstream Snapshots

Read-only mirrors of provider documentation and plugin READMEs that this
constitution depends on. Used by `scripts/upstream-watch.{sh,ps1}` to detect
when official sources change so the maintainer can decide whether to absorb
the changes into `governance/`.

## Layout

```text
upstream/
├── sources.yaml             # what to watch
├── .upstream-state.json     # per-source SHA-256 + last-fetched timestamp
├── docs/                    # vendor doc snapshots
│   ├── anthropic/
│   ├── openai/
│   ├── google/
│   ├── mcp/
│   ├── superpowers/
│   └── spec-kit/
├── ecc/                     # everything-claude-code plugin tracking
├── omc/                     # oh-my-claudecode plugin tracking
├── claude-mem/
├── memsearch/
└── superpowers/
```

## Workflow

```bash
# 1. Periodically check (no writes)
./scripts/upstream-watch.sh --check

# 2. Capture new snapshots if anything drifted
./scripts/upstream-watch.sh --apply

# 3. Review the actual change
git diff upstream/

# 4. Decide
#    - Just a wording tweak?  Commit the snapshot only; no governance change.
#    - Substantive change?    Edit the relevant file under governance/,
#                             bump VERSION, add CHANGELOG `Upstream` entry,
#                             commit, push.
```

## Why Not Rely Only on Live Fetches at Install Time?

Three reasons:

1. **Reproducibility**: Every machine should install the same constitution
   from the same point-in-time. Live network fetches at install time would
   make the constitution non-deterministic.
2. **Offline**: Many work machines run behind proxies or air-gaps.
3. **Auditability**: The git history of `upstream/` becomes a timeline of
   what the providers said and when.

## What This Layer Is NOT

- **Not** a sync of official content into `governance/`. The maintainer
  decides what to absorb; `upstream/` is just a mirror with a diff signal.
- **Not** a license-cleared redistribution. Snapshots are kept for personal
  reference. Don't republish them.
- **Not** a substitute for installing the actual plugins (ECC, OMC, etc.).
  See [`docs/plugin-bootstrap.md`](../docs/plugin-bootstrap.md).
