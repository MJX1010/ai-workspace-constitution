---
name: github-sync-commit
description: Use when the user asks to sync, commit, or push local repository changes to GitHub, especially from Windows/PowerShell, while avoiding leaked tokens, hardcoded credentials, unsafe git operations, or ambiguous push status.
---

# GitHub Sync Commit

## Overview

Use this skill to turn a local repo change into a verified GitHub commit and push without exposing secrets. Treat GitHub sync as a stateful operation: inspect first, commit only intended files, push with credential-safe methods, then verify the remote moved.

## Workflow

1. Resolve the repo surface:
   - Run `git status --short --branch`.
   - Run `git remote -v`.
   - Run `git log -1 --oneline --decorate`.
   - If the current directory is not a Git repo, locate the nested repo before acting.

2. Inspect before staging:
   - Run `git diff` for unstaged changes.
   - Run `git diff --cached` if anything is already staged.
   - Identify unrelated user changes and leave them unstaged unless the user explicitly included them.

3. Verify the changed surface:
   - Use the smallest relevant check for the changed file type, such as `git diff --check`, a parser, linter, unit test, or the original repro command.
   - Do not claim the fix is complete or push-ready without fresh verification output.

4. Stage and commit narrowly:
   - Stage only intended files, usually by explicit path: `git add path/to/file`.
   - Recheck `git diff --cached`.
   - Commit with a concise imperative message.

5. Push safely:
   - Prefer normal `git push origin <branch>`.
   - If HTTPS credential lookup fails, inspect `gh auth status` before changing configuration.
   - If `gh` is authenticated but Git credential manager fails, use a one-shot credential method that does not write secrets to repo config.

6. Verify the remote:
   - Run `git status --short --branch`.
   - Run `git log -1 --oneline --decorate`.
   - If possible, run `git ls-remote origin refs/heads/<branch>` or another remote check.
   - Report whether the repo is pushed, ahead, blocked, or partially complete.

## Secrets Rules

- Never hardcode GitHub tokens, PATs, passwords, cookies, or session values in files, docs, remotes, commit messages, shell history examples, or final answers.
- Never run `git remote set-url` with an embedded token.
- Never print `gh auth token` output.
- Never paste a real token into a command shown to the user.
- Prefer `gh auth login`, Git Credential Manager, OS keyring, SSH keys, or environment variables.
- If a one-shot token push is necessary, read the token into a local process variable and use it only inside the same command invocation. Do not save it.

PowerShell one-shot pattern:

```powershell
$token = gh auth token
if ([string]::IsNullOrWhiteSpace($token)) { throw "gh auth token returned empty" }
git -c http.sslBackend=openssl push "https://x-access-token:$token@github.com/OWNER/REPO.git" BRANCH
$token = $null
```

Only use this when:
- `gh auth status` confirms the correct account is logged in.
- Normal `git push` failed due to credential transport problems.
- The command output will not echo the URL with the token.

## Windows GitHub Troubleshooting

| Symptom | Likely cause | Safe next step |
|---|---|---|
| `SEC_E_NO_CREDENTIALS` / `AcquireCredentialsHandle failed` | Git Schannel or credential manager cannot initialize credentials | Try `git -c http.sslBackend=openssl push ...` with a safe credential source |
| `could not read Username for 'https://github.com'` | Non-interactive shell cannot prompt | Use `gh auth status`, then a credential helper or one-shot token variable |
| `API rate limit exceeded` while `gh auth status` says logged in | Request may not be using authenticated API path | Prefer Git push path; avoid unauthenticated API loops |
| Repo is `ahead 1` after commit | Local commit exists but remote did not move | Push again with a safe credential method and verify remote branch |

## Reporting Format

Keep the final report factual:

```text
SURFACE
- repo:
- branch:
- remote:

ACTION
- committed:
- pushed:

VERIFY
- commands:
- result:

NOTES
- blockers or warnings:
```

## Common Mistakes

- Staging all files with `git add .` when unrelated user work exists.
- Claiming a push completed after only creating a local commit.
- Fixing auth by writing tokens into remotes, config files, scripts, or docs.
- Re-running failing network commands repeatedly without reading the exact error.
- Using destructive commands such as `git reset --hard`, branch deletion, or force-push without explicit user approval.
