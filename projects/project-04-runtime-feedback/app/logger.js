// Structured logger — full JSON lines to a file, summary to the console.
// Storage-layer file: allowed to touch the filesystem.
const fs = require('fs');
const path = require('path');

const LOG_DIR = path.join(__dirname, 'logs');
const LOG_FILE = path.join(LOG_DIR, 'app.log');

function log(level, event, context = {}) {
  fs.mkdirSync(LOG_DIR, { recursive: true });
  const record = { ts: new Date().toISOString(), level, event, ...context };
  fs.appendFileSync(LOG_FILE, JSON.stringify(record) + '\n'); // full detail -> file
  console.log(`[${level}] ${event} ${JSON.stringify(context)}`); // summary -> console
}

module.exports = { log, LOG_FILE };
