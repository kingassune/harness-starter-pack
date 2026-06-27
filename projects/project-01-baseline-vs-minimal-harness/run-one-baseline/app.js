// Knowledge base app (baseline run — built from the bare prompt only).
const http = require('http');
const fs = require('fs');

// make a data folder
if (!fs.existsSync('./data')) fs.mkdirSync('./data');

const docs = ['Welcome.txt', 'Notes.txt']; // sample docs (hardcoded)

const html = `<!doctype html><html><body>
<div style="display:flex">
  <div style="width:200px;border-right:1px solid #ccc">
    <h3>Documents</h3>
    ${docs.map((d) => `<div>${d}</div>`).join('')}
  </div>
  <div style="padding-left:12px">
    <h3>Q&A</h3>
    <input id="q"><button onclick="ask()">Ask</button>
    <div id="a"></div>
  </div>
</div>
<script>
function ask(){
  fetch('/ask?q=' + encodeURIComponent(document.getElementById('q').value))
    .then(r => r.text()).then(t => document.getElementById('a').innerText = t);
}
</script>
</body></html>`;

http.createServer((req, res) => {
  if (req.url.startsWith('/ask')) {
    res.end('You asked: ' + decodeURIComponent((req.url.split('q=')[1] || '')));
    return;
  }
  res.end(html);
}).listen(3001, () => console.log('baseline app on http://localhost:3001'));
