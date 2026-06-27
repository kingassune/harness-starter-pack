// Knowledge-base app (Project 03) — adds chunking, metadata, indexing status,
// and grounded Q&A with citations on top of the P02 app.
const http = require('http');
const fs = require('fs');
const path = require('path');

const PORT = process.env.PORT || 3004;
const DATA_DIR = path.join(__dirname, 'data');
const DOCS_DIR = path.join(DATA_DIR, 'documents');
const INDEX_DIR = path.join(DATA_DIR, 'index');

function ensureData() {
  fs.mkdirSync(DOCS_DIR, { recursive: true });
  fs.mkdirSync(INDEX_DIR, { recursive: true });
  if (fs.readdirSync(DOCS_DIR).length === 0) {
    writeDoc({
      id: 'welcome',
      title: 'Welcome',
      body: 'This is your knowledge base. A harness wraps a model with tools. Verification gates keep work honest.',
    });
  }
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
function writeDoc(doc) {
  fs.writeFileSync(path.join(DOCS_DIR, `${doc.id}.json`), JSON.stringify(doc, null, 2));
  return doc;
}
function getDoc(id) {
  const f = path.join(DOCS_DIR, `${id}.json`);
  return fs.existsSync(f) ? JSON.parse(fs.readFileSync(f, 'utf8')) : null;
}
function listDocs() {
  return fs.readdirSync(DOCS_DIR).filter((f) => f.endsWith('.json'))
    .map((f) => JSON.parse(fs.readFileSync(path.join(DOCS_DIR, f), 'utf8')));
}
function importDoc({ title, body }) {
  if (!title || !body) return { error: 'title and body are required' };
  return writeDoc({ id: uniqueId(slugify(title)), title, body });
}

// ---- feature: chunking + metadata + index ---------------------------------
function chunk(body) {
  return body.split(/(?<=[.!?])\s+/).map((s) => s.trim()).filter(Boolean);
}
function metadata(body, chunks) {
  return {
    chars: body.length,
    words: body.trim().split(/\s+/).filter(Boolean).length,
    chunkCount: chunks.length,
  };
}
function indexDoc(id) {
  const doc = getDoc(id);
  if (!doc) return null;
  const chunks = chunk(doc.body).map((text, i) => ({ i, text }));
  const rec = { id, title: doc.title, chunks, metadata: metadata(doc.body, chunks) };
  fs.writeFileSync(path.join(INDEX_DIR, `${id}.json`), JSON.stringify(rec, null, 2));
  return rec;
}
function indexedIds() {
  return new Set(fs.readdirSync(INDEX_DIR).filter((f) => f.endsWith('.json')).map((f) => f.replace('.json', '')));
}

// ---- feature: indexing status ---------------------------------------------
function indexStatus() {
  const docs = listDocs();
  const idx = indexedIds();
  let totalChunks = 0;
  idx.forEach((id) => {
    totalChunks += JSON.parse(fs.readFileSync(path.join(INDEX_DIR, `${id}.json`), 'utf8')).chunks.length;
  });
  return {
    totalDocuments: docs.length,
    indexed: docs.filter((d) => idx.has(d.id)).length,
    pending: docs.filter((d) => !idx.has(d.id)).map((d) => d.id),
    totalChunks,
  };
}

// ---- feature: grounded Q&A with citation ----------------------------------
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
  if (req.method === 'GET' && url === '/api/documents')
    return send(res, 200, listDocs().map((d) => ({ id: d.id, title: d.title })));
  if (req.method === 'GET' && url === '/api/index/status') return send(res, 200, indexStatus());
  if (req.method === 'GET' && url.startsWith('/api/documents/')) {
    const doc = getDoc(url.split('/').pop());
    return doc ? send(res, 200, doc) : send(res, 404, { error: 'not found' });
  }
  if (req.method === 'POST' && url === '/api/documents') {
    const r = importDoc(JSON.parse((await readBody(req)) || '{}'));
    return send(res, r.error ? 400 : 201, r);
  }
  if (req.method === 'POST' && url.startsWith('/api/index/')) {
    const rec = indexDoc(url.split('/').pop());
    return rec ? send(res, 200, { indexed: rec.id, chunks: rec.chunks.length, metadata: rec.metadata }) : send(res, 404, { error: 'not found' });
  }
  if (req.method === 'POST' && url === '/api/ask')
    return send(res, 200, ask(JSON.parse((await readBody(req)) || '{}').q));
  return send(res, 404, { error: 'not found' });
});

if (require.main === module) {
  ensureData();
  server.listen(PORT, () => console.log(`kb app (project-03) on http://localhost:${PORT}`));
}
module.exports = { ensureData, importDoc, indexDoc, indexStatus, ask, getDoc, listDocs };
