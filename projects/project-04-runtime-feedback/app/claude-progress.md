# Progress log (Project 04)

## Deliverables
| Item | Status | Evidence |
|------|--------|----------|
| Structured logger | ✅ | `logger.js` → JSON lines in `logs/app.log` + console summary |
| Architecture docs | ✅ | `docs/ARCHITECTURE.md` (layers + boundaries) |
| Architecture guard | ✅ | `scripts/check-architecture.sh` — PASS clean, FAIL (exit 1) on injected `fs` violation |
| Seeded bug fixed | ✅ | removed `slice(0,500)` cap in `indexDoc` |
| Cleanup procedures | ✅ | `clean-state-checklist.md` |

## Bug: diagnosis → fix (via runtime feedback)
- **Symptom:** asking for content at the END of a large doc returned nothing.
- **Diagnosed by log, not code-reading:**
  `index.document {bodyChars:1521, indexedChars:500, truncated:true}` — the doc
  was 1521 chars but only 500 were indexed.
- **Root cause:** `const source = doc.body.slice(0, MAX_INDEX_CHARS)` capped input.
- **Fix:** index the full body.
- **Verified:** re-index → `{indexedChars:1521, truncated:false, chunks:29}`;
  ask "zebra_sentinel" → found at chunk 28.

Architecture guard green throughout (the bug was a logic defect, not a boundary
violation — different tools for different failure classes).
