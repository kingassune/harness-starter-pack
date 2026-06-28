// Variant 2 — GENERATOR + EVALUATOR.
// Generator wrote the naive version; an independent evaluator reviewed it and
// filed two defects, which were fixed:
//   - DEFECT: case-sensitive matching (missed 'evals' vs 'Evals')
//   - DEFECT: missing/undefined query returned [] instead of all docs
// The evaluator caught real bugs the solo agent shipped — but, reviewing freely
// (no spec), it didn't think to require BODY matching or whitespace handling.
function filterDocs(docs, q) {
  const query = (q || '').toLowerCase();
  if (!query) return docs; // evaluator fix: empty/missing query => all
  return docs.filter((d) => d.title.toLowerCase().includes(query)); // still title-only
}

module.exports = { filterDocs };
