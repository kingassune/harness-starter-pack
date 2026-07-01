// Capstone core — every harness mechanism is a toggle so the ablation can
// measure each one's causal impact. Toggles are env vars; "off" disables.
//
//   HARNESS_ROLE_SEP    (P05)  filtering: strong V3 logic vs weak V1 logic
//   HARNESS_FIX_CHUNKING(P04)  indexing: full body vs the seeded 500-char cap
//   HARNESS_PERSIST     (P02/3) storage: on disk (survives restart) vs in-memory
const fs = require('fs');
const path = require('path');

const FLAGS = {
  roleSep: process.env.HARNESS_ROLE_SEP !== 'off',
  fixChunking: process.env.HARNESS_FIX_CHUNKING !== 'off',
  persist: process.env.HARNESS_PERSIST !== 'off',
};

// ---- filtering (P05: role separation) -------------------------------------
function filterDocs(docs, q) {
  if (FLAGS.roleSep) {
    const query = (q || '').trim().toLowerCase();
    if (!query) return docs;
    return docs.filter(
      (d) => d.title.toLowerCase().includes(query) || d.body.toLowerCase().includes(query)
    );
  }
  return docs.filter((d) => d.title.includes(q)); // weak: case-sensitive, title-only
}

// ---- chunking (P04: runtime-feedback bug fix) -----------------------------
function chunkSource(body) {
  const source = FLAGS.fixChunking ? body : body.slice(0, 500);
  return source.split(/(?<=[.!?])\s+/).map((s) => s.trim()).filter(Boolean);
}

// ---- storage (P02/P03: persistence / continuity) --------------------------
class Store {
  constructor(dir) {
    this.dir = dir;
    this.mem = {};
    if (FLAGS.persist) fs.mkdirSync(dir, { recursive: true });
  }
  put(id, doc) {
    if (FLAGS.persist) fs.writeFileSync(path.join(this.dir, `${id}.json`), JSON.stringify(doc));
    else this.mem[id] = doc;
  }
  all() {
    if (FLAGS.persist) {
      return fs
        .readdirSync(this.dir)
        .filter((f) => f.endsWith('.json'))
        .map((f) => JSON.parse(fs.readFileSync(path.join(this.dir, f), 'utf8')));
    }
    return Object.values(this.mem);
  }
}

module.exports = { FLAGS, filterDocs, chunkSource, Store };
