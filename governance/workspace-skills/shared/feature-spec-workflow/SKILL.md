---
name: feature-spec-workflow
description: "Per-feature spec / plan / tasks workflow for any non-trivial change. Use when starting a new feature, resuming a session after interruption, or receiving an ambiguous request. Creates and maintains `specs/<NNN-name>/{spec,plan,tasks}.md` so multiple AI tools (Claude / Codex / Gemini / Cursor) share the same persistent state. Triggered by keywords like 'add feature', 'implement', 'resume', 'continue', 'where did we stop', or any request that isn't describable as a one-line diff."
---

# Feature Spec Workflow

## When to Use

**Use this skill when:**

- The user requests a non-trivial change — multiple files, new behaviour, anything not describable in one sentence.
- A previous session was interrupted and you need to resume.
- The request is ambiguous and needs a written agreement before code.
- You are an AI tool other than the one that started the feature (Codex picking up Claude's work, Gemini picking up Codex's, ...) — read the spec files first.

**Skip this skill when:**

- The change is a one-line fix or rename.
- Quoting Anthropic's official best practices: *"If you could describe the diff in one sentence, skip the plan."*
- The user explicitly asks for an unplanned quick edit.

## File Layout

Every meaningful feature lives in its own numbered directory:

```
${WORKSPACE_ROOT}/
└── specs/
    ├── 001-add-payment-flow/
    │   ├── spec.md       # status + intent + acceptance criteria
    │   ├── plan.md       # technical blueprint
    │   ├── tasks.md      # - [ ] checkbox list
    │   └── research.md   # optional: prior art, links, sources
    └── 002-refactor-auth/
        └── ...
```

**Numbering convention:**

- Zero-padded 3-digit prefix (`001`, `002`, …, expands to `1000+` automatically).
- Kebab-case slug after the dash.
- `ls specs/` → take the highest existing number, increment.

This naming is borrowed from GitHub Spec Kit so any tool that already understands Spec Kit conventions can resume work.

## Three Approval Gates

The workflow is intentionally gated. Don't skip the gates — the ETH Zurich
study (Feb 2026) found unreviewed LLM-generated context files **reduce**
agent success by ~3%, while human-reviewed ones improve it by ~4%.

```
user request
    │
    ▼
[Gate 1]  Write spec.md      → user reads/approves intent
    │
    ▼
[Gate 2]  Write plan.md      → user reads/approves approach
    │
    ▼
[Gate 3]  Write tasks.md     → user reads/approves task list
    │
    ▼
implementation begins (mark `- [x]` per task, commit per task)
```

If the human is impatient and skips a gate, that's their call — but state in
the conversation that you skipped it, so the spec records it.

## Resume Protocol (Critical)

When you arrive at a workspace and the user says "continue", "resume",
"keep going", or "where were we":

1. `ls specs/` — find the most recently modified directory by mtime.
2. Read its `spec.md` first. Check the `status:` frontmatter field.
   - `Draft` / `InProgress` / `Review`: resume.
   - `Done` / `Abandoned`: ask the user before doing anything.
3. Open `tasks.md`. Find the first `- [ ]` unchecked item.
4. Read enough `plan.md` context to execute that one task safely.
5. Implement. Mark `- [x]`. Commit with a message that references the task ID
   (e.g. `feat(payment): T003 implement Stripe webhook`).
6. Loop to next unchecked task. Repeat.

If the user is vague about which feature, list the in-progress ones (`status:
InProgress`) and ask.

## Authoring Protocol (Starting Fresh)

1. **Pick NNN**: `ls specs/ 2>/dev/null | tail -1` → increment, default `001`.
2. **Create directory**: `specs/NNN-<slug>/`.
3. **Write spec.md** from `references/spec-template.md`. Show to user.
4. **After approval**, write `plan.md` from `references/plan-template.md`. Show to user.
5. **After approval**, write `tasks.md` from `references/tasks-template.md`. Show to user.
6. **Begin implementation**. One task at a time. Commit per task.

## Status Field

Every `spec.md` starts with YAML frontmatter:

```yaml
---
status: Draft        # Draft | InProgress | Review | Done | Abandoned
owner: <user-handle or 'AI'>
created: 2026-05-11
updated: 2026-05-11
---
```

Update `updated` and `status` as the feature progresses. Status transitions:

```
Draft ──approved──▶ InProgress ──tests pass──▶ Review ──merged──▶ Done
  │                      │                          │
  └──user kills──────────┴──────────────────────────┴──▶ Abandoned
```

## Tasks.md Format

Strictly machine-parsable so any tool can scan it:

```markdown
- [ ] T001 <description> (<file>:<line if applicable>)
- [ ] T002 [P] <description that can run in parallel with other [P] tasks>
- [x] T003 ~~<crossed-out, no longer needed>~~
```

`[P]` marker: safe to dispatch as a parallel subagent. Tasks **within** the
same phase that are `[P]` can run concurrently. Tasks **across** phases stay
sequential.

## Compatible Toolchains

This skill is a thin **convention layer**. It doesn't reimplement; it points
at the tool the user prefers:

| Toolchain in this workspace | Equivalent invocation |
|---|---|
| ECC (Everything Claude Code) | `/prp-prd` → `/prp-plan` → `/prp-implement` (works with our `spec.md`/`plan.md`/`tasks.md` layout) |
| Superpowers (obra) | `brainstorming` → `writing-plans` → `executing-plans` (uses `docs/superpowers/` paths; can be redirected here) |
| GitHub Spec Kit | `/speckit.constitution` → `/specify` → `/plan` → `/tasks` (drop-in compatible — our layout *is* Spec Kit's) |
| Kiro (AWS) | three-phase workflow (`requirements.md` ≈ our `spec.md`, `design.md` ≈ `plan.md`, `tasks.md` identical) |
| Plain Claude Code / Codex / Gemini | use templates directly, no slash commands needed |

The point of this skill: **the directory layout is the contract**. Whatever
tool writes the file, the next tool can read it.

## What This Skill Does NOT Do

- Implement features. The implementing tool / sub-agent does that.
- Lock you into one harness. All four toolchains above work.
- Replace the workspace `AGENTS.md`. That file references this convention; this skill defines it.

## References

- `references/spec-template.md` — fill-in template for the intent doc
- `references/plan-template.md` — fill-in template for the technical blueprint
- `references/tasks-template.md` — fill-in template for the task list
- `references/convention-sources.md` — upstream conventions this consolidates
