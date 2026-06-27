# CLEAN-STATE CHECKLIST (Project 04)

Between test runs, and before trusting any result:

- [ ] Kill stray servers on the port: `lsof -i :3005` empty (or `kill`).
- [ ] Reset runtime state: `rm -rf data logs` then start fresh.
- [ ] Re-create state by running the server (it ensures `data/` + writes `logs/`).
- [ ] Diagnose with logs first: `grep index.document logs/app.log` — check
      `truncated` and `indexedChars` vs `bodyChars`.
- [ ] Run the architecture guard: `bash scripts/check-architecture.sh` → PASS.
- [ ] Evidence in `claude-progress.md` was produced on THIS clean state.
