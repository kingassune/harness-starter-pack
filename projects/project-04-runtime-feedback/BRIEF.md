# Project 04 — Runtime Feedback & Scope Control

**Harness lesson:** observable runtime signals + architecture guardrails let an
agent diagnose and fix bugs through structured feedback instead of blind search.

## Background
Builds on Project 03. A seeded indexing defect makes large-file chunking fail.
The agent must diagnose it — fast — using logs and boundaries, not guesswork.

## Objective
Add runtime observability and architecture constraints that prevent cross-layer
violations and speed up debugging.

## Step-by-step tasks
1. **Examine the starter** — note the weak diagnostics + missing architecture validation.
2. **Structured logging** — add a logger service that captures startup, import,
   and indexing events (timestamps, severity, context).
3. **Architecture docs** — write layer boundaries in `docs/ARCHITECTURE.md`.
4. **Architecture validation script** — `scripts/check-architecture.sh` to
   enforce boundaries and catch violations.
5. **Fix the seeded bug** — repair the chunking logic that fails on large files.
6. **Cleanup procedures** — `clean-state-checklist.md` for state reset between runs.

## Success criteria
- Runtime logs pinpoint root cause without exhaustive code review.
- The architecture script catches layer violations before they compound.
- Resolution time drops measurably vs. the starter.
- Fixes stay non-invasive and localized.

---
*In `NOTES.md`: which log line found the bug, and which boundary the guard enforces.*
