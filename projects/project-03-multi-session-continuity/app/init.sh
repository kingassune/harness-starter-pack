#!/usr/bin/env bash
# Initialize a fresh session: check runtime, create data dirs.
set -e

echo "node: $(node --version)"
mkdir -p data/documents data/index
echo "init complete: data/documents and data/index ready"
echo "run: PORT=3004 node server.js"
