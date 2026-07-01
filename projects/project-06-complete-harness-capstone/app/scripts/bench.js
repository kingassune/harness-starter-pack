// Benchmark: score the CURRENT toggle config against a fixed functional suite.
// Each check maps to a harness mechanism, so turning a mechanism off drops the
// score in a measurable, causal way. Prints "SCORE x/y".
const path = require('path');
const fs = require('fs');
const { filterDocs, chunkSource, Store } = require(path.join(__dirname, '..', 'kb'));

const docs = [
  { id: 'a', title: 'Prompt Caching', body: 'Cache the system prompt to cut cost.' },
  { id: 'b', title: 'Evals', body: 'Tests for agents run in CI.' },
  { id: 'c', title: 'Harness', body: 'Wrap a model with TOOLS and verification.' },
];

let pass = 0;
let total = 0;
function check(name, cond) {
  total++;
  if (cond) pass++;
  console.log(`${cond ? 'PASS' : 'FAIL'}  ${name}`);
}
const ids = (arr) => arr.map((d) => d.id).sort().join(',');

// filtering (role separation)
check('filter: case-insensitive', ids(filterDocs(docs, 'evals')) === 'b');
check('filter: body match', ids(filterDocs(docs, 'tools')) === 'c');
check('filter: whitespace tolerant', ids(filterDocs(docs, '  prompt ')) === 'a');

// chunking (runtime-feedback bug fix): a large doc's END must still be indexed
const big = 'A harness wraps a model with tools. '.repeat(30) + 'The keyword is ZEBRA_SENTINEL.';
check('indexing: full large doc', chunkSource(big).join(' ').includes('ZEBRA_SENTINEL'));

// persistence (continuity): survives a simulated restart (new Store, same dir)
const dir = path.join(__dirname, '..', 'data-bench');
fs.rmSync(dir, { recursive: true, force: true });
const s1 = new Store(dir);
s1.put('x', { id: 'x', title: 'X', body: 'y' });
const s2 = new Store(dir); // "restart"
check('persistence: survives restart', s2.all().length === 1);
fs.rmSync(dir, { recursive: true, force: true });

console.log(`SCORE ${pass}/${total}`);
