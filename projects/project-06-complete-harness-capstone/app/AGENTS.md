# AGENTS.md — capstone knowledge-base app

The whole harness in one place. Each rule traces to a project.

## What this is
A local knowledge base: import → index → filter → ask (grounded, cited). The
five harness mechanisms are toggles in `kb.js` so their value can be measured.

## How to work here (the loop)
1. Run `./init.sh` before anything. [P01: rules/init beat raw prompts]
2. Orient from `session-handoff.md` + `feature_list.json`. [P02: readable workspace]
3. Do ONE feature at a time; mark passing only with evidence. [P03: continuity]
4. Diagnose with logs (`logs/app.log`); keep layer boundaries. [P04: feedback]
5. Split roles for anything substantive: plan → generate → evaluate vs a
   contract. [P05: role separation]
6. Before "done": `scripts/benchmark.sh`, `scripts/cleanup-scanner.sh`.

## Boundaries
- Only `server.js`, `kb.js`, `logger.js` touch the filesystem.
- The UI (`public/`) talks HTTP/JSON only.

## Done means
Strong benchmark = 5/5, cleanup scan CLEAN, every `feature_list.json` item
passing with evidence.
