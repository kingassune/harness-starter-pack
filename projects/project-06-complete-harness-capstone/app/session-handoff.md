# SESSION HANDOFF — capstone

## State
Capstone assembled. All 5 harness mechanisms present; 3 are measurable toggles.
- Benchmark: strong 5/5, weak 0/5.
- Ablation: role-sep 5→2, chunking-fix 5→4, persistence 5→4.
- Cleanup scanner: CLEAN.

## Run
```
./init.sh
PORT=3006 node server.js
# app smoke:
curl -s -X POST -H 'Content-Type: application/json' \
  -d '{"title":"Harness","body":"Wrap a model with tools and verification."}' \
  http://localhost:3006/api/documents
curl -s -X POST -H 'Content-Type: application/json' \
  -d '{"q":"verification"}' http://localhost:3006/api/ask
```

## Measure
- `bash scripts/benchmark.sh`  — weak vs strong
- `bash scripts/ablation.sh`   — which mechanism carries weight
- `bash scripts/cleanup-scanner.sh`

## Next
- [ ] Add readable-workspace + verification as measurable toggles too (currently
      static/meta), so all 5 appear in the ablation.
- [ ] Wire more product features and re-benchmark.
