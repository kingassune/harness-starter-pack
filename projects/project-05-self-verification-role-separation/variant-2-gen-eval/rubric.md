# Evaluator rubric — Variant 2 (generator + evaluator)

**Score: 3/5** (objective, from `compare.js`)

| Criterion | Result |
|-----------|--------|
| case-insensitive | ✅ evaluator filed it; generator fixed (`toLowerCase`) |
| title OR body | ❌ still title-only |
| empty query => all | ✅ evaluator fix (`if (!query) return docs`) |
| missing query => all | ✅ same guard |
| whitespace tolerant | ❌ no trim |

## What changed vs Variant 1
An **independent** evaluator reviewed the generator's output and filed two real
defects (case-sensitivity, missing-query). Fixing them lifted the score 1→3.

## Why it didn't reach 5
The evaluator reviewed freely, with **no contract**. It caught what looked
obviously wrong, but had no checklist forcing it to ask "should body match?" or
"what about whitespace?" Independent review beats self-review — but unguided
review still misses requirements nobody wrote down.
