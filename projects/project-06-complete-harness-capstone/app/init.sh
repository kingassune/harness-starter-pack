#!/usr/bin/env bash
set -e
echo "node: $(node --version)"
mkdir -p data/documents data/index logs
echo "init complete. run: PORT=3006 node server.js"
