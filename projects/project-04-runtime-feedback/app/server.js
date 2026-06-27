// Knowledge-base app (Project 04) — adds structured logging around the indexing
// pipeline. NOTE: ships with a SEEDED chunking bug that fails on large files;
// the logs are what let us find it. (Fixed in a later step.)
const http = require('http');
const fs = require('fs');
const path = require('path');
const { log } = require('./logger');

const PORT = process.env.PORT || 3005;
const DATA_DIR = path.join(__dirname, 'data');
const DOCS_DIR = path.join(DATA_DIR, 'documents');
const INDEX_DIR = path.join(DATA_DIR, 'index');

function ensureData() {
  fs.mkdirSync(DOCS_DIR, { recursive: true });
  fs.mkdirSync(INDEX_DIR, { recursive: true });
}

// ---- documents -------------------------------------------------------------
function slugify(t) {
  return t.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '') || 'doc';
}
function uniqueId(base) {
  let id = base, n = 1;
  while (fs.existsSync(path.join(DOCS_DIR, `${id}.json`))) id = `${base}-${++n}`;
  return id;
}
function getDoc(id) {
  const f = path.join(DOCS_DIR, `${id}.json`);
  return fs.existsSync(f) ? JSON.parse(fs.readFileSync(f, 'utf8')) : null;
}
function importDoc({ title, body }) {
  if (!title || !body) return { error: 'title and body are required' };
  const id = uniqueId(slugify(title));
  fs.writeFileSync(path.join(DOCS_DIR, `${id}.json`), JSON.stringify({ id, title, body }, null, 2));
  log('info', 'import.document', { id, bodyChars: body.length });
  return { id, title, body };
}

// ---- indexing --------------------------------------------------------------
function chunk(text) {
  return text.split(/(?<=[.!?])\s+/).map((s) => s.trim()).filter(Boolean);
}
function indexDoc(id) {
  const doc = getDoc(id);
  if (!doc) return null;
  const source = doc.body; // fixed: index the full document (was capped at 500)
  const chunks = chunk(source).map((text, i) => ({ i, text }));
  log('info', 'index.document', {
    id,
    bodyChars: doc.body.length,
    indexedChars: source.length,
    chunks: chunks.length,
    truncated: source.length < doc.body.length,
  });
  fs.writeFileSync(path.join(INDEX_DIR, `${id}.json`), JSON.stringify({ id, title: doc.title, chunks }, null, 2));
  return { id, chunks: chunks.length };
}
function ask(q) {
  const query = (q || '').toLowerCase().trim();
  for (const f of fs.readdirSync(INDEX_DIR).filter((x) => x.endsWith('.json'))) {
    const rec = JSON.parse(fs.readFileSync(path.join(INDEX_DIR, f), 'utf8'));
    const hit = rec.chunks.find((c) => c.text.toLowerCase().includes(query));
    if (query && hit) return { answer: hit.text, citation: { document: rec.title, chunk: hit.i } };
  }
  return { answer: 'No matching indexed content found.', citation: null };
}

// ---- http ------------------------------------------------------------------
function send(res, code, body, type = 'application/json') {
  res.writeHead(code, { 'Content-Type': type });
  res.end(typeof body === 'string' ? body : JSON.stringify(body));
}
function readBody(req) {
  return new Promise((resolve) => {
    let d = '';
    req.on('data', (c) => (d += c));
    req.on('end', () => resolve(d));
  });
}

const server = http.createServer(async (req, res) => {
  const url = req.url.split('?')[0];
  if (req.method === 'GET' && url === '/')
    return send(res, 200, fs.readFileSync(path.join(__dirname, 'public', 'index.html'), 'utf8'), 'text/html');
  if (req.method === 'POST' && url === '/api/documents') {
    const r = importDoc(JSON.parse((await readBody(req)) || '{}'));
    return send(res, r.error ? 400 : 201, r);
  }
  if (req.method === 'POST' && url.startsWith('/api/index/')) {
    const r = indexDoc(url.split('/').pop());
    return r ? send(res, 200, r) : send(res, 404, { error: 'not found' });
  }
  if (req.method === 'POST' && url === '/api/ask')
    return send(res, 200, ask(JSON.parse((await readBody(req)) || '{}').q));
  return send(res, 404, { error: 'not found' });
});

if (require.main === module) {
  ensureData();
  log('info', 'startup', { port: PORT });
  server.listen(PORT, () => console.log(`kb app (project-04) on http://localhost:${PORT}`));
}
module.exports = { ensureData, importDoc, indexDoc, ask };
