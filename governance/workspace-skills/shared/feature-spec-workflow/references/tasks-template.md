# Tasks: <Feature Name>

> Read `spec.md` and `plan.md` first.
>
> Format: `- [ ] T<NNN> [P?] <description> (file:line if specific)`
>
> `[P]` marks tasks that can run in parallel with other `[P]` tasks
> **within the same phase**. Tasks across phases stay sequential.
>
> Mark `- [x]` immediately upon completion and commit. The state of this
> file IS the progress tracker — never rely on the chat session.

## Phase 1: Foundation (set up the structure, no behaviour yet)

- [ ] T001 Create file skeleton — `<path>`
- [ ] T002 [P] Create test skeleton (failing tests, TDD red) — `<path>`
- [ ] T003 [P] Add dependency / migration / config — `<file>`

## Phase 2: Implementation (make it work)

- [ ] T004 Implement <unit> — `<path>:<lines>`
- [ ] T005 Implement <unit> — `<path>:<lines>`
- [ ] T006 Make Phase 1 tests pass (TDD green)

## Phase 3: Integration (wire it up)

- [ ] T007 Call <new code> from <existing caller> — `<path>:<line>`
- [ ] T008 Add integration test — `<path>`
- [ ] T009 [P] Update docs — `<path>`

## Phase 4: Verification (prove it's done)

- [ ] T010 Run full test suite, all green
- [ ] T011 Run linter / type-check, clean
- [ ] T012 Manual smoke per `plan.md` Verification Plan
- [ ] T013 Update `CHANGELOG.md`
- [ ] T014 Update `spec.md` status: InProgress → Review

## Phase 5: Land (only after human review)

- [ ] T015 Open PR with summary referencing this spec
- [ ] T016 Address review comments
- [ ] T017 Merge
- [ ] T018 Update `spec.md` status: Review → Done

---

## Notes & Discoveries

<Append unstructured notes here as work progresses — surprises, follow-ups,
 ideas that aren't urgent enough to derail the current task. Triage them
 into new specs/ entries when the feature is done.>
