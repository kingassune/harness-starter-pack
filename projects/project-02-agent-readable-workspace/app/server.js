// Knowledge-base app (Project 02) — adds import + detail view to the P01 app.
const http = require('http');
const fs = require('fs');
const path = require('path');

const PORT = process.env.PORT || 3003;
const DATA_DIR = path.join(__dirname, 'data');
const DOCS_DIR = path.join(DATA_DIR, 'documents');

function ensureData() {
  fs.mkdirSync(DOCS_DIR, { recursive: true });
  if (fs.readdirSync(DOCS_DIR).length === 0) {
    writeDoc({ id: 'welcome', title: 'Welcome', body: 'This is your knowledge base.' });
  }
}

function slugify(title) {
  return title.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '') || 'doc';
}

function uniqueId(base) {
  let id = base;
  let n = 1;
  while (fs.existsSync(path.join(DOCS_DIR, `${id}.json`))) id = `${base}-${++n}`;
  return id;
}

function writeDoc(doc) {
  fs.writeFileSync(path.join(DOCS_DIR, `${doc.id}.json`), JSON.stringify(doc, null, 2));
  return doc;
}

function getDoc(id) {
  const file = path.join(DOCS_DIR, `${id}.json`);
  return fs.existsSync(file) ? JSON.parse(fs.readFileSync(file, 'utf8')) : null;
}

function listDocs() {
  return fs
    .readdirSync(DOCS_DIR)
    .filter((f) => f.endsWith('.json'))
    .map((f) => JSON.parse(fs.readFileSync(path.join(DOCS_DIR, f), 'utf8')));
}

// feature: document-import — persist a new document from {title, body}
function importDoc({ title, body }) {
  if (!title || !body) return { error: 'title and body are required' };
  const id = uniqueId(slugify(title));
  return writeDoc({ id, title, body });
}

function send(res, code, body, type = 'application/json') {
  res.writeHead(code, { 'Content-Type': type });
  res.end(typeof body === 'string' ? body : JSON.stringify(body));
}

function readBody(req) {
  return new Promise((resolve) => {
    let data = '';
    req.on('data', (c) => (data += c));
    req.on('end', () => resolve(data));
  });
}

const server = http.createServer(async (req, res) => {
  const url = req.url.split('?')[0];

  if (req.method === 'GET' && url === '/') {
    return send(res, 200, fs.readFileSync(path.join(__dirname, 'public', 'index.html'), 'utf8'), 'text/html');
  }
  if (req.method === 'GET' && url === '/api/documents') {
    return send(res, 200, listDocs().map((d) => ({ id: d.id, title: d.title })));
  }
  // feature: document-detail — GET /api/documents/:id
  if (req.method === 'GET' && url.startsWith('/api/documents/')) {
    const doc = getDoc(url.split('/').pop());
    return doc ? send(res, 200, doc) : send(res, 404, { error: 'not found' });
  }
  // feature: document-import — POST /api/documents
  if (req.method === 'POST' && url === '/api/documents') {
    const body = await readBody(req);
    let payload = {};
    try {
      payload = JSON.parse(body || '{}');
    } catch (_) {
      return send(res, 400, { error: 'invalid JSON' });
    }
    const result = importDoc(payload);
    return send(res, result.error ? 400 : 201, result);
  }

  return send(res, 404, { error: 'not found' });
});

if (require.main === module) {
  ensureData();
  server.listen(PORT, () => console.log(`kb app (project-02) on http://localhost:${PORT}`));
}

module.exports = { ensureData, importDoc, getDoc, listDocs };
