# Update Policy

This document describes when and how to absorb upstream provider documentation
changes into the constitution.

## The Two Update Loops

```text
┌──────────────────────────────────────────────────────────────────┐
│ Loop A — Re-render on a new machine (consumer flow)              │
│                                                                  │
│   git pull   →   install.sh   →   verify.sh                      │
│                                                                  │
│   Triggered by:  arriving on a new box, after VERSION bump.      │
│   Frequency:     daily / per session.                            │
│   Outcome:       local files match the committed governance/.    │
└──────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────┐
│ Loop B — Absorb upstream drift (author flow)                     │
│                                                                  │
│   upstream-watch --check    →    review URLs in output           │
│        ↓                                                          │
│   upstream-watch --apply    →    git diff upstream/              │
│        ↓                                                          │
│   read the actual diff      →    decide:                          │
│      • cosmetic only?       →    commit upstream/ snapshot only   │
│      • substantive?         →    edit governance/                 │
│                                  bump VERSION                     │
│                                  add CHANGELOG `Upstream` entry   │
│                                  commit, push                     │
│                                                                  │
│   Triggered by:  weekly / monthly cadence, or after a major      │
│                  vendor announcement.                            │
└──────────────────────────────────────────────────────────────────┘
```

## When to Edit `governance/`

Absorb upstream changes into governance only when **all** of the following
are true:

1. The change is **stable** (it won't be reverted next week).
2. It's **broadly applicable** (cross-repo, cross-task, cross-harness).
3. It's **actionable** (it implies a constraint or a workflow, not a slogan).
4. It introduces a **new invariant** the existing rules don't already cover.

If any of those is no, just commit the upstream snapshot and move on. The
diff in `git log -- upstream/` is enough of an audit trail.

## SemVer Rules

```text
MAJOR — Breaks an installed file's public location or layout.
        Examples: rename governance/workspace/ to governance/root/,
        change marker comment format, drop a harness adapter.

MINOR — Adds a new component, skill, harness adapter, or rule.
        Examples: add governance/ for Trae, add new vibe-coding guardrail.

PATCH — Wording tweak, bug fix in scripts/, doc update, minor upstream
        absorption that doesn't change the rule shape.
```

## CHANGELOG Discipline

`CHANGELOG.md` follows [Keep a Changelog 1.1.0](https://keepachangelog.com/en/1.1.0/).

### Sections (in canonical order)

- **Added** — net-new content.
- **Changed** — modifications to existing rules / scripts that don't break callers.
- **Deprecated** — soon-to-be-removed features still present.
- **Removed** — content removed.
- **Fixed** — corrections.
- **Security** — security-relevant changes.
- **Upstream** — drifts pulled from official provider docs. **Always include
  the source URL and the snapshot date** so future-you can re-trace the path.

### Author flow

```bash
# Make changes
$EDITOR governance/...

# Decide version bump (per SemVer rules above)
$EDITOR VERSION

# Move [Unreleased] entries into a new versioned section, dated today
$EDITOR CHANGELOG.md

# Commit and tag
git add VERSION CHANGELOG.md governance/...
git commit -m "feat(governance): <one-line summary>"
git tag v$(cat VERSION)
git push --follow-tags

# Now pull on every other machine
./scripts/update.sh
```

## Frequency Guidelines

| Action | Cadence |
|---|---|
| `update.sh` (pull + re-render) | Daily, or whenever you start work on a new box |
| `verify.sh` | Daily, or on suspicion of drift |
| `upstream-watch --check` | Weekly is plenty for personal use |
| Bumping `VERSION` | When a meaningful governance change ships, not for every commit |
| Tagging | At the same time as the VERSION bump |

## What This Policy Is NOT

- **Not** a service-level commitment. Personal repo, no SLO.
- **Not** a guarantee of compatibility with old plugin versions. If ECC,
  OMC, or Anthropic's plugin marketplace ship breaking changes, re-align
  governance and bump MAJOR.
- **Not** an excuse to re-run `update.sh` while in the middle of a session
  if no machine setup has changed. The cheapest update is the one you skip.
