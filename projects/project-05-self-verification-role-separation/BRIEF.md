# Project 05 — Self-Verification & Role Separation

**Harness lesson:** one agent that plans, builds, *and* reviews declares victory
early and misses defects. Splitting roles — an evaluator independent of the
generator — catches what the solo agent overlooks.

## Background
Builds on Project 04. Implement the **same feature** three ways and measure the
quality each added role buys.

## Step-by-step tasks
1. **Pick one substantive feature** (e.g. multi-turn conversation history,
   citation panel redesign, or document filtering) — keep it identical across all runs.
2. **Variant 1 — Single Role:** one agent plans, implements, self-reviews.
3. **Variant 2 — Gen-Eval:** a generator implements; an evaluator reviews and
   documents revision evidence.
4. **Variant 3 — Plan-Gen-Eval:** add a planner before the generator; the
   evaluator reviews against a sprint contract.
5. **Compare** all three with the evaluation rubric.

## Reference scores (upstream)
- single-role ≈ **1.6/5**
- gen-eval ≈ **3.3/5**
- plan-gen-eval ≈ **4.9/5**

## Success criteria
- Scores improve as roles are added.
- The evaluator finds concrete defects the generator missed.
- Gen-eval clearly beats single-role.
- Plan-gen-eval is highest via explicit sprint contracting.
- Evidence shows role separation reduces premature "done" calls.

---
*In `NOTES.md`: a rubric per variant + the defect the evaluator caught.*
