# CLAUDE.md

Agent-specific pointer. Read `AGENTS.md` first — it holds the operating rules.

Quick commands:
- Init: `./init.sh`
- Run: `PORT=3006 node server.js`
- Benchmark (weak vs strong): `bash scripts/benchmark.sh`
- Ablation (which mechanism matters): `bash scripts/ablation.sh`
- Cleanup gate: `bash scripts/cleanup-scanner.sh`

Do not edit toggle defaults in `kb.js` to "win" the benchmark — the benchmark
sets flags via env per run.
