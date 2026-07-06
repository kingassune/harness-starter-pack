// P05 close-out: the WINNING variant (V3, plan-gen-eval) wired into a real app.
// Exposes document filtering over HTTP so the 5/5 logic runs in production, not
// just in compare.js.
const http = require('http');
const { filterDocs } = require('../variant-3-plan-gen-eval/filter.js');

const PORT = process.env.PORT || 3007;
const docs = [
  { id: 'a', title: 'Prompt Caching', body: 'Cache the system prompt to cut cost.' },
  { id: 'b', title: 'Evals', body: 'Tests for agents run in CI.' },
  { id: 'c', title: 'Harness', body: 'Wrap a model with TOOLS and verification.' },
];

const server = http.createServer((req, res) => {
  const [url, qs] = req.url.split('?');
  if (req.method === 'GET' && url === '/api/documents') {
    const q = new URLSearchParams(qs || '').get('q') || '';
    res.writeHead(200, { 'Content-Type': 'application/json' });
    return res.end(JSON.stringify(filterDocs(docs, q).map((d) => ({ id: d.id, title: d.title }))));
  }
  res.writeHead(404, { 'Content-Type': 'application/json' });
  res.end('{"error":"not found"}');
});

if (require.main === module) {
  server.listen(PORT, () => console.log(`p05 filter app on http://localhost:${PORT}`));
}
