# SPRINT CONTRACT — document filtering

The planner defines acceptance up front. The evaluator reviews the generator's
work against THIS list — not vibes. A feature is done only when every item passes.

## Feature
`filterDocs(docs, q)` returns the documents matching query `q`.

## Acceptance criteria
1. **Case-insensitive** — `q="evals"` matches a doc titled "Evals".
2. **Title OR body** — `q="tools"` matches a doc whose body contains "TOOLS".
3. **Empty query → all** — `q=""` returns every document.
4. **Missing query → all** — `q` undefined returns every document.
5. **Whitespace-tolerant** — `q="  prompt "` matches "Prompt Caching".

## Out of scope
Ranking/sorting by relevance; fuzzy/typo matching.
