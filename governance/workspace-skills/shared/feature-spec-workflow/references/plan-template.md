# Plan: <Feature Name>

> Read `spec.md` first. This document is the technical blueprint.

## Architecture Decision

<One paragraph: which approach we chose. If there were viable
 alternatives, list them and the rejection rationale. This is the
 "why" so a future reviewer (or future-you) can avoid relitigating.>

## File Structure

<Decide every file that will exist (new + modified) before writing tasks.
 Per Superpowers v5: deciding file structure upfront catches scope creep
 inside a single file early.>

```
<paths the feature will create or modify, with one-line responsibility each>
```

## Affected Files

| File | Change | Reason |
|---|---|---|
| `<path>` | new / modify / delete | <one-line why> |
| ... | ... | ... |

## Data Model / API Changes

<Only if applicable. Mermaid diagram or pseudo-schema is fine.>

```text
<schema or sequence diagram>
```

## Tech Stack

<List language / framework / libraries this feature touches. Note any new
 dependency that needs to be added to package.json / Cargo.toml / etc.>

## Risks & Mitigations

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| R1: ... | low/med/high | low/med/high | ... |

## Verification Plan

<How we know it works end-to-end.>

- **Unit tests**: ...
- **Integration / E2E**: ...
- **Manual checks**: ...
- **Rollback**: <how to revert if production breaks>

## Dependencies

<External libraries or other in-progress features that must land first.>

- ...

## Out of Scope (referenced in spec)

<Restate spec.md Non-Goals here as a check that they're respected by this plan.>
