// Variant 3 — PLANNER + GENERATOR + EVALUATOR.
// Built to sprint-contract.md and reviewed against each of its 5 criteria:
//   1 case-insensitive  2 title OR body  3 empty => all  4 missing => all
//   5 whitespace-tolerant
function filterDocs(docs, q) {
  const query = (q || '').trim().toLowerCase(); // crit 4 (||''), crit 5 (trim), crit 1 (lower)
  if (!query) return docs; // crit 3 + 4
  return docs.filter(
    (d) =>
      d.title.toLowerCase().includes(query) || // crit 1 + 2
      d.body.toLowerCase().includes(query)
  );
}

module.exports = { filterDocs };
