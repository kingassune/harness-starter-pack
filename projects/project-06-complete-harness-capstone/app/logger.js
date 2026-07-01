// Structured logger — full JSON lines to a file, summary to console. (from P04)
const fs = require('fs');
const path = require('path');

const LOG_DIR = path.join(__dirname, 'logs');
const LOG_FILE = path.join(LOG_DIR, 'app.log');

function log(level, event, context = {}) {
  fs.mkdirSync(LOG_DIR, { recursive: true });
  const record = { ts: new Date().toISOString(), level, event, ...context };
  fs.appendFileSync(LOG_FILE, JSON.stringify(record) + '\n');
  if (process.env.HARNESS_QUIET !== 'on') {
    console.log(`[${level}] ${event} ${JSON.stringify(context)}`);
  }
}

module.exports = { log, LOG_FILE };
