// Knowledge-base app (harness run) — built to satisfy feature_list.json.
const http = require('http');
const fs = require('fs');
const path = require('path');

const PORT = process.env.PORT || 3002;
const DATA_DIR = path.join(__dirname, 'data');
const DOCS_DIR = path.join(DATA_DIR, 'documents');

function ensureData() {
  fs.mkdirSync(DOCS_DIR, { recursive: true });
  if (fs.readdirSync(DOCS_DIR).length === 0) {
    writeDoc({ id: 'welcome', title: 'Welcome', body: 'This is your knowledge base.' });
    writeDoc({
      id: 'harness',
      title: 'Harness',
      body: 'A harness wraps a model with tools, verification, and rules.',
    });
  }
}

function writeDoc(doc) {
  fs.writeFileSync(path.join(DOCS_DIR, `${doc.id}.json`), JSON.stringify(doc, null, 2));
}

function listDocs() {
  return fs
    .readdirSync(DOCS_DIR)
    .filter((f) => f.endsWith('.json'))
    .map((f) => JSON.parse(fs.readFileSync(path.join(DOCS_DIR, f), 'utf8')));
}

// feature: qa-panel — grounded answer with a citation
function answer(q) {
  const query = (q || '').toLowerCase().trim();
  const docs = listDocs();
  const hit = docs.find(
    (d) => d.body.toLowerCase().includes(query) || d.title.toLowerCase().includes(query)
  );
  return hit
    ? { answer: hit.body, source: hit.title }
    : { answer: 'No matching document found.', source: null };
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
  if (req.method === 'GET' && req.url === '/') {
    return send(res, 200, fs.readFileSync(path.join(__dirname, 'public', 'index.html'), 'utf8'), 'text/html');
  }
  if (req.method === 'GET' && req.url === '/api/documents') {
    return send(res, 200, listDocs().map((d) => ({ id: d.id, title: d.title })));
  }
  if (req.method === 'POST' && req.url === '/api/ask') {
    const body = await readBody(req);
    let q = '';
    try {
      q = JSON.parse(body || '{}').q || '';
    } catch (_) {
      q = '';
    }
    return send(res, 200, answer(q));
  }
  return send(res, 404, { error: 'not found' });
});

if (require.main === module) {
  ensureData();
  server.listen(PORT, () => console.log(`knowledge-base app on http://localhost:${PORT}`));
}

module.exports = { ensureData, listDocs, writeDoc, answer };
