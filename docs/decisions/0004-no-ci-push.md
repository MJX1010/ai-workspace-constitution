# ADR-0004: Manual git push only — no GitHub Actions automation

## Status

Accepted — 2026-04-29

## Context

A natural design for "stay current with upstream provider docs" is a
GitHub Actions cron that runs `upstream-watch --apply` weekly and opens
a PR. The author would review and merge.

The author explicitly preferred to do `git pull` and `git push` themselves,
without scheduled bot activity in the repo.

## Decision

No GitHub Actions are configured by default.

The "stay current" workflow runs **locally** instead:

```bash
./scripts/upstream-watch.sh --check    # cheap, read-only HTTP fetch
./scripts/upstream-watch.sh --apply    # save snapshots, but commit/push
                                       # remain manual
```

If the author later wants CI verification on PRs, a `.github/workflows/verify.yml`
that runs the unittest suite on macOS / Linux / Windows is straightforward to
add — but it must not push commits.

## Consequences

**Good:**
- Personal repo stays personal: no automated commits arrive without the
  author's hand on the keyboard.
- No GitHub Actions minutes consumed.
- No risk of an automated bot bringing in upstream changes the author
  hasn't reviewed.
- Works the same on private repos with no Actions runners.
- Deterministic: the constitution at any commit is exactly what the author
  decided to commit, never what a bot decided was probably fine.

**Bad:**
- "I forgot to run `upstream-watch` for three months" is a real failure
  mode. Mitigation: add an entry to whatever calendar / reminder system
  the author already uses, or wire a cron on a personal machine that runs
  `upstream-watch --check` and emails on drift.

## Alternatives considered

- **Cron + auto-PR.** Rejected per author preference.
- **Commit hooks that re-run `verify.sh`.** Could be added to the install
  guide as an opt-in. Rejected as default — would surprise the user the
  first time they make an unrelated commit in this repo.

## Revisit if

- The author wants a multi-machine consistency check: a CI matrix
  running `install.sh` + `verify.sh` on all three OSes per PR. That's
  additive (not push-automation) and benign to add later.
