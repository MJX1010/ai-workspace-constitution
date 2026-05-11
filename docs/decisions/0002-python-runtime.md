# ADR-0002: Python 3.8+ as the install/update runtime

## Status

Accepted — 2026-04-29

## Context

The installer needs to:

- Parse YAML manifests
- Walk file trees, render templates, write files
- Compute SHA-256 hashes
- Maintain a JSON state file
- Fetch HTTP(S) for upstream watching
- Work on macOS, Linux, and Windows

We considered three runtimes: pure Bash + PowerShell, Python, and a
compiled Go binary.

## Decision

Use **Python 3.8+** for the actual logic. Provide thin Bash and PowerShell
wrappers (~50 LOC each) that find Python and dispatch.

PyYAML is the only third-party dependency. The wrappers bootstrap it via
`pip install --user --quiet pyyaml` on first run.

## Consequences

**Good:**
- Single source of truth for install / verify / update / upstream-watch
  logic (no dual maintenance burden).
- Python's stdlib covers `pathlib`, `hashlib`, `json`, `subprocess`,
  `urllib.request`, `argparse`, `unittest`. Most of the program is
  zero-dep.
- macOS Big Sur (2020) and newer ship Python 3.8+ by default.
  Most Linux distros include it. Windows users install once via winget
  or python.org.

**Bad:**
- First-run bootstrap on a fresh machine requires either a working pip
  or a manual PyYAML wheel.
- Python 3.8 is the floor. macOS Catalina (2019) and earlier need a
  manual `brew install python3`.

## Alternatives considered

- **Pure Bash + PowerShell duo.** Each platform reads its native YAML.
  Rejected: YAML parsing in Bash is fragile (regex-driven), HTTP via
  `curl` differs subtly from `Invoke-WebRequest`, and we'd be writing
  every algorithm twice.
- **Single compiled Go binary.** Cross-compile per OS. Rejected: a
  per-OS binary in a personal repo is unnecessary friction; reading
  the source becomes harder; Go isn't already on every personal box.
- **Node.js.** Cross-platform, easy YAML/HTTP. Rejected: Node is not
  preinstalled on macOS or many Linux servers; Python is.
- **Ruby.** macOS-traditional, fading. Not on most Linux or Windows
  boxes.

## Revisit if

- A target machine cannot install Python 3.8+ and cannot run pip.
- The personal-repo scope grows enough that one-binary distribution
  becomes worth the complexity.
