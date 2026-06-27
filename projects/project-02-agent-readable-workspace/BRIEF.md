# Project 02 — Agent-Readable Workspace

**Harness lesson:** a readable repo + persistent state files let a fresh agent
understand structure and resume work without anyone re-explaining it.

## Background
Builds on Project 01. The challenge: a new agent session should grasp the
project and current progress from the *repository state alone*.

## Objective
"Add 'readability' to the repo so a new agent can quickly understand the project
structure, know the current progress, and pick up work." Spans two separate
agent sessions to prove continuity via checked-in docs.

## Core tasks
- **Run two comparison sessions:**
  1. **Starter session** — work against the thinner workspace (no
     `session-handoff.md`); measure how much rediscovery happens.
  2. **Solution session** — work against the expanded workspace (full docs +
     handoff); verify a fresh agent resumes with no verbal context.
- **Implement three product features:**
  - document import,
  - document detail/content viewing,
  - persistence across restarts.

## Starter / what you create
- Expand the workspace with `ARCHITECTURE.md`, `PRODUCT.md`,
  `feature_list.json`, and `session-handoff.md`.

## Success criteria
- A second session understands prior progress from repo state alone.
- All three features function across restarts.
- Documentation supports handoff without external explanation.

---
*Record both sessions + what the handoff doc had to contain in `NOTES.md`.*
