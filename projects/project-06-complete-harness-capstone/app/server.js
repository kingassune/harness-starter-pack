// Capstone app — assembles the toggle-aware core (kb.js) + structured logging
// into a runnable knowledge base: import, filter, index, ask.
const http = require('http');
const path = require('path');
const { FLAGS, filterDocs, chunkSource, Store } = require('./kb');
const { log } = require('./logger');

const PORT = process.env.PORT || 3006;
const store = new Store(path.join(__dirname, 'data', 'documents'));
const index = new Store(path.join(__dirname, 'data', 'index'));

function slugify(t) {
  return t.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '') || 'doc';
}

function send(res, code, body, type = 'application/json') {
  res.writeHead(code, { 'Content-Type': type });
  res.end(typeof body === 'string' ? body : JSON.stringify(body));
}
function readBody(req) {
  return new Promise((r) => {
    let d = '';
    req.on('data', (c) => (d += c));
    req.on('end', () => r(d));
  });
}

const server = http.createServer(async (req, res) => {
  const [url, qs] = req.url.split('?');
  if (req.method === 'GET' && url === '/')
    return send(res, 200, require('fs').readFileSync(path.join(__dirname, 'public', 'index.html'), 'utf8'), 'text/html');

  if (req.method === 'GET' && url === '/api/documents') {
    const q = new URLSearchParams(qs || '').get('q') || '';
    return send(res, 200, filterDocs(store.all(), q).map((d) => ({ id: d.id, title: d.title })));
  }
  if (req.method === 'POST' && url === '/api/documents') {
    const { title, body } = JSON.parse((await readBody(req)) || '{}');
    if (!title || !body) return send(res, 400, { error: 'title and body required' });
    const id = slugify(title);
    store.put(id, { id, title, body });
    index.put(id, { id, title, chunks: chunkSource(body).map((text, i) => ({ i, text })) });
    log('info', 'import.document', { id, bodyChars: body.length });
    return send(res, 201, { id, title });
  }
  if (req.method === 'POST' && url === '/api/ask') {
    const q = (JSON.parse((await readBody(req)) || '{}').q || '').toLowerCase().trim();
    for (const rec of index.all()) {
      const hit = rec.chunks.find((c) => c.text.toLowerCase().includes(q));
      if (q && hit) return send(res, 200, { answer: hit.text, citation: { document: rec.title, chunk: hit.i } });
    }
    return send(res, 200, { answer: 'No matching indexed content found.', citation: null });
  }
  return send(res, 404, { error: 'not found' });
});

if (require.main === module) {
  log('info', 'startup', { port: PORT, flags: FLAGS });
  server.listen(PORT, () => console.log(`capstone kb app on http://localhost:${PORT}`));
}
