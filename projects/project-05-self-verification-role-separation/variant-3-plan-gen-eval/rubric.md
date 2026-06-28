# Evaluator rubric — Variant 3 (planner + generator + evaluator)

**Score: 5/5** (objective, from `compare.js`)

| Criterion (from sprint-contract.md) | Result |
|-------------------------------------|--------|
| 1. case-insensitive | ✅ |
| 2. title OR body | ✅ |
| 3. empty query => all | ✅ |
| 4. missing query => all | ✅ |
| 5. whitespace tolerant | ✅ |

## What changed vs Variant 2
A **planner** wrote `sprint-contract.md` *before* coding — turning fuzzy "filter
documents" into 5 explicit, checkable criteria. The generator built to the
contract; the evaluator reviewed **against each line**. Nothing was left to
"seemed fine."

## The lesson
Self-review (V1) misses your blind spots. Unguided independent review (V2) misses
unwritten requirements. A contract + independent review (V3) closes both gaps:
the planner makes requirements explicit, the evaluator makes "done" provable.
