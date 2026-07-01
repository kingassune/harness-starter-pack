# CLEAN-STATE CHECKLIST (capstone)

- [ ] `rm -rf data logs data-bench` before a clean benchmark.
- [ ] No stray server on the port (`lsof -i :3006`).
- [ ] `bash scripts/cleanup-scanner.sh` → CLEAN.
- [ ] Benchmark run on clean state: strong 5/5, weak 0/5.
- [ ] `data/`, `logs/`, `data-bench/` are gitignored, not committed.
