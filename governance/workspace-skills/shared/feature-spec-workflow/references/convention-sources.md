# Convention Sources

This skill consolidates conventions from seven existing systems. Whichever
toolchain the human happens to use today, the on-disk artifacts are
compatible.

## GitHub Spec Kit

Authoritative reference. Our `specs/NNN-<slug>/{spec,plan,tasks}.md`
directory layout is intentionally identical to Spec Kit's so the
`/specify`, `/plan`, and `/tasks` commands work unmodified.

- Repo: <https://github.com/github/spec-kit>
- Spec-driven doc: <https://github.com/github/spec-kit/blob/main/spec-driven.md>
- Plan template: <https://github.com/github/spec-kit/blob/main/templates/plan-template.md>

Spec Kit additions we omit by default (you can add per-feature if needed):

- `constitution.md` — we already have one at workspace level (`AGENTS.md`).
- `research.md` — optional under each feature dir.
- `data-model.md`, `quickstart.md`, `contracts/` — optional, add when feature complexity warrants.

## Kiro (AWS)

Three-file workflow (`requirements.md`, `design.md`, `tasks.md`).
Mapping to our layout:

| Kiro | Ours |
|---|---|
| `requirements.md` | `spec.md` |
| `design.md` | `plan.md` |
| `tasks.md` | `tasks.md` |

Kiro uses EARS notation for requirements; we don't enforce a notation, but
keep acceptance criteria testable.

- Specs docs: <https://kiro.dev/docs/specs/>
- Best practices: <https://kiro.dev/docs/specs/best-practices/>

## BMAD Method

Multi-agent workflow with named personas (Analyst, PM, Architect, SM, Dev).
Artifacts: `docs/prd.md`, `docs/architecture.md`,
`{epicNum}.{storyNum}.story.md`.

We borrow:

- **State lives in versioned files, not chat** — BMAD's hardest-won lesson.
- **Fresh chat per workflow** — each session starts by reading the spec, not by carrying chat history.

We don't borrow:

- Named agent personas (heavyweight for a solo developer).
- YAML workflow orchestration.

- Repo: <https://github.com/bmad-code-org/BMAD-METHOD>

## PRP (Product Requirement Prompt)

A PRP = PRD + curated codebase intelligence + agent runbook. Pattern:
`INITIAL.md` → `PRPs/<feature>.md`. Our `spec.md` + `plan.md` together cover
the same surface; we just split them so the gates are explicit.

- Original framework: <https://github.com/Wirasm/PRPs-agentic-eng>
- Context engineering intro: <https://github.com/coleam00/context-engineering-intro>

## Superpowers (obra) v5

Pipeline: `brainstorming` → `writing-plans` → `executing-plans`.
Plans saved under `docs/superpowers/plans/YYYY-MM-DD-<feature>.md`.

We adopt:

- **File Structure decided before tasks** (v5 addition).
- **Plans assume zero context** — explicit file paths, code snippets, verification steps.
- **Adversarial review** — a subagent reads the planning doc for completeness before implementation begins.

We don't adopt:

- Date-prefixed filenames (we use numbered dirs for stable ordering).

- writing-plans SKILL: <https://github.com/obra/superpowers/blob/main/skills/writing-plans/SKILL.md>
- executing-plans SKILL: <https://github.com/obra/superpowers/blob/main/skills/executing-plans/SKILL.md>
- v5 release notes: <https://blog.fsck.com/2026/03/09/superpowers-5/>

## Anthropic Plan Mode (official)

4-phase workflow: **Explore → Plan → Implement → Commit**.
Anthropic's recommendation: "If you could describe the diff in one sentence,
skip the plan." That sentence is the canonical guard against over-applying
this skill.

- Best practices: <https://code.claude.com/docs/en/best-practices>
- How Anthropic teams use Claude Code (PDF): <https://www-cdn.anthropic.com/58284b19e702b49db9302d5b6f135ad8871e7658.pdf>

## AGENTS.md cross-tool standard

The Sourcegraph-led, OpenAI/Google-supported open standard for
project-level instructions. 60K+ repos. Claude Code still on `CLAUDE.md`
but symlink works:

```bash
mv CLAUDE.md AGENTS.md && ln -s AGENTS.md CLAUDE.md
```

We keep both filenames live (per workspace) so every harness reads its
preferred name. The workspace `AGENTS.md` references this skill's
convention so any tool entering the workspace knows where to find
in-progress work.

- Standard intro: <https://tessl.io/blog/the-rise-of-Users\user1ad83966\projects\agents-a43a494ccb-an-open-standard-and-single-source-of-truth-for-ai-coding-agents/>

## Reverse-Provenance Note

When a feature absorbs a meaningful pattern from one of these sources
(e.g. a new template section, a new gate), record it in this file with
the date and source URL. That keeps the convention auditable as the
ecosystem evolves.

## ETH Zurich Finding (Feb 2026)

Empirical study on AGENTS.md / CLAUDE.md context files:

- **LLM-generated, unreviewed** context files: **-3% task success**, **+20% token cost**.
- **Human-reviewed** context files: **+4% task success**.

Conclusion: **the spec / plan / tasks gates are not bureaucracy — they pay for themselves.**
