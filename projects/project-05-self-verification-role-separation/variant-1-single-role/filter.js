// Variant 1 — SINGLE ROLE.
// One agent planned, implemented, and self-reviewed this. It "looks fine" on the
// happy path, so it was declared done. (Self-review misses its own blind spots.)
function filterDocs(docs, q) {
  return docs.filter((d) => d.title.includes(q)); // case-sensitive, title-only
}

module.exports = { filterDocs };
