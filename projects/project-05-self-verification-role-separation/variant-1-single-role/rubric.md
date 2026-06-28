# Evaluator rubric — Variant 1 (single role)

**Score: 1/5** (objective, from `compare.js`)

| Criterion | Result |
|-----------|--------|
| case-insensitive | ❌ `includes(q)` is case-sensitive — 'evals' ≠ 'Evals' |
| title OR body | ❌ title-only |
| empty query => all | ✅ (incidental: `"x".includes("")` is true) |
| missing query => all | ❌ `title.includes(undefined)` → [] |
| whitespace tolerant | ❌ no trim |

## Why it failed
One agent planned, built, and reviewed its own work. Self-review confirmed the
happy path and declared victory. The defects are exactly the cases the author
didn't think to question — the blind spot of grading your own homework.
