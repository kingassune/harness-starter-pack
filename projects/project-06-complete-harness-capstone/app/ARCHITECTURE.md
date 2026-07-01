# ARCHITECTURE

```
public/index.html   ← UI (HTTP/JSON only)
server.js           ← API: import, filter, index, ask
kb.js               ← core mechanisms (toggle-aware): filter, chunk, Store
logger.js           ← structured logging
data/, logs/        ← storage
scripts/            ← benchmark.sh, ablation.sh, cleanup-scanner.sh, bench.js
```

## Mechanism → toggle → project
| Mechanism | Env toggle | From |
|-----------|-----------|------|
| Filtering quality | `HARNESS_ROLE_SEP` | P05 |
| Full-doc indexing | `HARNESS_FIX_CHUNKING` | P04 |
| Persistence | `HARNESS_PERSIST` | P02/03 |

## Boundary
Only `server.js`, `kb.js`, `logger.js` touch the filesystem. UI is HTTP-only.
