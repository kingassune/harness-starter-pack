# Project 06 — my notes (capstone)

## What I assembled
One knowledge-base app carrying all five harness mechanisms, three of them as
env toggles so their value is measurable, not assumed:
- P02/03 persistence, P04 chunking fix + logging, P05 role-separated filtering,
  plus P01 rules/init and P02 readable workspace as the surface files.

## The measurements (reproducible)
| Run | Score |
|-----|-------|
| Strong harness (all on) | **5/5** |
| Weak harness (all off) | **0/5** |

### Ablation — which mechanism carries the weight
| Removed from strong | Score | Drop |
|---------------------|-------|------|
| Role separation (P05) | 2/5 | **−3** |
| Chunking fix (P04) | 4/5 | −1 |
| Persistence (P02/03) | 4/5 | −1 |

Role separation had the largest single impact here (it governs 3 of the 5
functional checks); chunking-fix and persistence each carry one. That's the
point of an ablation: it turns "we added a bunch of harness" into "here is
exactly which part earned its place."

## Cleanup
`scripts/cleanup-scanner.sh` → CLEAN (exit 0): no TODO/FIXME/debugger, no stray
backup files, runtime dirs gitignored.

## Takeaway
A harness isn't faith — it's measurable. Toggle a mechanism, run the benchmark,
read the drop. Keep the pieces that move the number; question the ones that
don't. "The best harness is the smallest one that still works."
