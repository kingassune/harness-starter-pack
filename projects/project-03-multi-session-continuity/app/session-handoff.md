# SESSION HANDOFF

> Read this first. A fresh session should resume with zero verbal context.

## Project
Knowledge-base app, Project 03 (multi-session continuity). Adds an indexing
pipeline: chunking → metadata → indexing status → grounded Q&A with citations.

## Orient (in order)
1. `claude-progress.md` — what's done + evidence.
2. `feature_list.json` — pass/fail with acceptance criteria.
3. `server.js` — the pipeline (see `indexDoc`, `indexStatus`, `ask`).
4. `clean-state-checklist.md` — run before trusting any verification.

## Run a clean session
```
./init.sh
PORT=3004 node server.js
```

## Data model
- `data/documents/<id>.json` → `{id,title,body}` (raw docs)
- `data/index/<id>.json`     → `{id,title,chunks:[{i,text}],metadata}` (indexed)
- A doc is "pending" until it has an index file. Q&A only sees indexed chunks.

## Current state
- 4/4 features passing with evidence (see `claude-progress.md`).
- Verified across a restart: documents + index persist; Q&A still cites correctly.

## Next steps
- [ ] Auto-index on import (currently indexing is an explicit step).
- [ ] Rank multiple chunk matches instead of first-hit.
- [ ] Project 04: add structured logging + an architecture guard, then fix a
      seeded chunking bug using the logs.

## Gotchas
- `data/` is gitignored (runtime state). `rm -rf data && ./init.sh` to reset.
- Index is NOT auto-refreshed if a doc changes — re-POST `/api/index/:id`.
