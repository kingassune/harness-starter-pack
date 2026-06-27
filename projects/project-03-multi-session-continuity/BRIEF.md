# Project 03 — Multi-Session Continuity

**Harness lesson:** scope control + verification gates + handoff artifacts stop
agents from drifting across features or losing context on restart.

## Background
Builds on Project 02. Agents often drift or lose context when sessions restart.
Four product features anchor the work:
- document chunking,
- metadata extraction,
- indexing status UI,
- grounded Q&A with citations.

## Objective
Implement scope control, verification gates, and multi-session handoff. Track
progress in `feature_list.json`, completing **one feature at a time** and marking
items complete **only when concrete verification evidence exists** — never on
assumption.

## Step-by-step tasks
1. Set up from the starter (partial indexing, unfinished grounded QA).
2. Implement document chunking.
3. Extract + store metadata.
4. Build the indexing progress display.
5. Develop the citation-based Q&A flow.
6. Create handoff artifacts: `init.sh`, `session-handoff.md`,
   `claude-progress.md`, `clean-state-checklist.md`.
7. Update `feature_list.json` — mark features only after documented evidence.

## Success criteria
- One feature at a time, no drift.
- State persists across restarts.
- Every "passing" feature has concrete verification evidence.
- Handoff artifacts let another session resume seamlessly.
- Final `feature_list.json` reflects only verified features.

---
*Key idea to capture in `NOTES.md`: "verified, with evidence" ≠ "looks done".*
