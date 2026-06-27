# Project 01 — my notes

## Run One — Baseline (prompt only)
- **Time:** fast (~one shot, no setup).
- **How far it got:** a server that launches with two panels and an echo "Q&A".
- **What went wrong / was missing:**
  - documents were **hardcoded strings**, not read from the data dir
  - data dir was created but **never used** — no persistence
  - "Q&A" just **echoed** the question — no grounding, no citation
  - no setup script, no naming conventions, **no definition of "done"**

## Run Two — With harness (AGENTS.md + init.sh + feature_list.json)
- **Time:** slower up front (write the 3 artifacts first), faster to *correct* completion.
- **How far it got:** all **4/4 features passing with evidence**:
  - window-launch → `GET /` 200
  - document-list-panel → reads `data/documents/*.json`
  - qa-panel → grounded answer **with a citation** (`source`)
  - local-data-persistence → survived a **restart** test
- **What the harness changed:**
  - `feature_list.json` gave **concrete acceptance criteria**, so "done" was
    unambiguous and nothing got skipped.
  - `AGENTS.md` rule "mark passing only with evidence" forced **verification**
    (real curl output), not assumptions.
  - `init.sh` removed setup ambiguity (runtime check + data dir).

## Comparison / takeaway
Same task, same agent — but the **prompt-only run produced a shallow demo** while
the **harness run produced a complete, verified, persistent app**. The harness
cost a few minutes up front and bought correctness, consistency, and evidence.
That gap *is* harness engineering: the structure around the model, not the model,
decided the outcome.
