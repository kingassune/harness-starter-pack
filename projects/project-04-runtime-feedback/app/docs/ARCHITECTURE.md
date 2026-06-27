# ARCHITECTURE — layer boundaries

```
public/index.html   ← UI layer    (browser; HTTP/JSON only)
        │ fetch
server.js           ← API/logic   (routing, import, indexing, ask)
logger.js           ← logging     (structured logs to file)
        │ fs
data/, logs/        ← storage     (JSON docs, index, log files)
```

## Boundaries (enforced by `scripts/check-architecture.sh`)
1. **The UI layer must not use Node or storage APIs.** No `require(...)`,
   `process.*`, `child_process`, or `fs.*` in `public/`. The browser talks to
   the server over HTTP only.
2. **Only the storage-aware files touch the filesystem.** `fs` may be used in
   `server.js` and `logger.js` only — no other top-level module reads/writes disk.

Why: keeping `fs` access on one side of the boundary means a storage bug can
only live in one place, and the UI can never silently couple to disk layout.
