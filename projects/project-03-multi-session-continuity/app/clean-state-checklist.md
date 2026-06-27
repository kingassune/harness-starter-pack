# CLEAN-STATE CHECKLIST

Run before trusting a verification result, and between test runs. A "pass" on
dirty state is not a pass.

- [ ] No stray server running on the port: `lsof -i :3004` is empty (or `kill` it).
- [ ] Reset data if testing from scratch: `rm -rf data` then `./init.sh`.
- [ ] `data/documents/` and `data/index/` both exist (init.sh creates them).
- [ ] `feature_list.json` evidence was produced on THIS clean state, not a stale one.
- [ ] After a restart, `GET /api/index/status` matches what you expect (continuity check).
- [ ] No uncommitted debug code or console spam left in `server.js`.
