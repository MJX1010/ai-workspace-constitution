# Architecture Decision Records

Each ADR captures a single significant decision. Format follows
[Michael Nygard's template](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions),
trimmed for personal-repo brevity.

## Index

| # | Title | Status |
|---|---|---|
| [0001](0001-template-syntax.md) | `${VAR}` substitution as the template syntax | Accepted |
| [0002](0002-python-runtime.md) | Python 3.8+ as the install/update runtime | Accepted |
| [0003](0003-user-owned-vs-plugin-managed.md) | User-owned vs plugin-managed content separation | Accepted |
| [0004](0004-no-ci-push.md) | Manual git push only — no GitHub Actions automation | Accepted |

## Adding an ADR

1. Pick the next number.
2. Copy `0001-template-syntax.md` as a template.
3. Status: `Proposed` → `Accepted` (after deciding) → eventually `Superseded by NNNN`.
4. Append to the index above.
