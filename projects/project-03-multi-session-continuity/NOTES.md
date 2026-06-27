# Project 03 — my notes

## What this project adds over P02
P02 made the repo *readable*. P03 makes the *work itself* resumable mid-stream
by combining three mechanisms:

1. **Scope control** — one feature at a time (chunking → metadata → status → QA).
   No half-finished features scattered around; each is landed before the next.
2. **Verification gates** — `feature_list.json` marks a feature `passing` ONLY
   with a real command + output. "Looks done" never counts.
3. **Handoff artifacts** — `init.sh`, `session-handoff.md`, `claude-progress.md`,
   `clean-state-checklist.md` let a brand-new session resume cold.

## The continuity proof
The real test isn't "does it work" — it's "does it survive a restart and can a
new session pick up." Both verified:
- imported + indexed a 2nd doc, **restarted the server**, and
  `GET /api/index/status` still showed `2/2 indexed, 5 chunks`
- Q&A after restart still answered from the index **with the right citation**

## Why "clean-state-checklist" matters
A pass on dirty state is a lie. If a stale server or leftover `data/` is around,
your evidence is meaningless. The checklist forces: kill stray servers, reset
data, re-run on a known-clean state — *then* record evidence.

## Takeaway
Continuity = scope control + evidence + handoff. Drift happens when an agent
juggles many half-features and trusts "looks done." This project removes both:
finish one, prove it, write down where you are. A restart (or a fresh agent)
loses nothing.
