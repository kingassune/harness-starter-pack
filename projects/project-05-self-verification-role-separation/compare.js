// Shared evaluator: run every variant against the same cases, score objectively.
const docs = [
  { id: 'a', title: 'Prompt Caching', body: 'Cache the system prompt to cut cost.' },
  { id: 'b', title: 'Evals', body: 'Tests for agents run in CI.' },
  { id: 'c', title: 'Harness', body: 'Wrap a model with TOOLS and verification.' },
];

const cases = [
  { name: "case-insensitive title ('evals')", q: 'evals', expect: ['b'] },
  { name: "body match ('tools')", q: 'tools', expect: ['c'] },
  { name: 'empty query => all', q: '', expect: ['a', 'b', 'c'] },
  { name: 'missing query => all', q: undefined, expect: ['a', 'b', 'c'] },
  { name: "whitespace ('  prompt ')", q: '  prompt ', expect: ['a'] },
];

const variants = ['variant-1-single-role', 'variant-2-gen-eval', 'variant-3-plan-gen-eval'];

for (const v of variants) {
  const { filterDocs } = require(`./${v}/filter.js`);
  let pass = 0;
  console.log(`\n== ${v} ==`);
  for (const c of cases) {
    let got;
    try {
      got = filterDocs(docs, c.q).map((d) => d.id).sort();
    } catch (e) {
      got = `ERROR:${e.message}`;
    }
    const ok = JSON.stringify(got) === JSON.stringify([...c.expect].sort());
    if (ok) pass++;
    console.log(`${ok ? 'PASS' : 'FAIL'}  ${c.name} -> [${got}]`);
  }
  console.log(`score: ${pass}/${cases.length}`);
}
