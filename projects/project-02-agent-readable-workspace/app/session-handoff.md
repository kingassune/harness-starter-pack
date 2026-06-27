# SESSION HANDOFF

> Read this first. It tells a fresh agent exactly where things stand and what to
> do next — no verbal context required.

## Project
Knowledge-base app, Project 02 (agent-readable workspace). Goal: import +
detail-view + persistence, plus docs that make the repo self-explaining.

## How to get oriented (in order)
1. `PRODUCT.md` — what we're building and why.
2. `ARCHITECTURE.md` — layers, the document format, and the endpoints.
3. `feature_list.json` — current pass/fail status with evidence.
4. This file — current state + next steps.

## How to run / verify
```
PORT=3003 node server.js
curl -s http://localhost:3003/api/documents
curl -s -X POST -H 'Content-Type: application/json' \
  -d '{"title":"T","body":"B"}' http://localhost:3003/api/documents
```

## Current state
- All 3 features in `feature_list.json` are **passing with evidence**.
- Seed data: a `welcome` document is created on first launch.
- Q&A endpoint from P01 is NOT carried into this project's server (scope: P02 is
  import/detail/persistence). Re-add `POST /api/ask` if needed.

## Next steps (suggested)
- [ ] Add document editing/deleting (currently out of scope).
- [ ] Re-introduce grounded Q&A (`/api/ask`) on top of imported docs.
- [ ] Move to Project 03 (multi-session continuity): add `init.sh`,
      `clean-state-checklist.md`, and one-feature-at-a-time gating.

## Gotchas
- `data/documents/` is gitignored (runtime state). Delete it to reset to seed.
- `id` is a slug of the title; duplicate titles get `-2`, `-3` suffixes.
