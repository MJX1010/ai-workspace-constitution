# ADR-0001: `${VAR}` substitution as the template syntax

## Status

Accepted — 2026-04-29

## Context

Templates need to carry placeholders for paths and identifiers that vary
per machine: workspace root, home, username, constitution version. The
templates are mostly Markdown / TOML / JSON files that are read by humans
and AI agents.

## Decision

Use plain `${VAR}` placeholders. The renderer is a multi-pass string
replace over a `dict[str, str]`. No real templating engine.

```python
def resolve_vars(text, vars):
    for _ in range(8):  # multi-pass for ${A}=${B} chains
        prev = text
        for k, v in vars.items():
            text = text.replace(f"${{{k}}}", v)
        if text == prev: break
    return text
```

## Consequences

**Good:**
- Zero external dependencies.
- Identical behaviour on macOS / Linux / Windows.
- The placeholder syntax matches POSIX shell variable expansion, so
  authors can mentally test substitution.
- Templates remain valid Markdown / TOML / JSON files when viewed raw,
  so editors don't choke on them.

**Bad:**
- No conditionals, no loops, no string filters. If we ever need
  per-OS branches inside a template, we'd need to introduce a real
  engine.
- A literal `${X}` in the *content* of a template will be replaced if
  `X` happens to be a variable name. So far this hasn't bitten —
  variables are uppercase and namespaced (`WORKSPACE_ROOT`,
  `CONSTITUTION_VERSION`); content is unlikely to collide.

## Alternatives considered

- **Jinja2** — proper templating, but adds a Python dep beyond stdlib +
  PyYAML and is overkill for the simple substitutions we do.
- **Mustache (chevron)** — similar dep cost, plus `{{var}}` is awkward
  in Markdown which uses `{{` for nothing meaningful but `${}` reads as
  natural shell syntax.
- **Handlebars** — same as Mustache, plus it's not Python-native.

## Revisit if

- We need per-OS conditional content inside a single template file.
- A user-content collision happens (a template legitimately needs to
  contain a literal `${SOMETHING}` that should not be replaced).
