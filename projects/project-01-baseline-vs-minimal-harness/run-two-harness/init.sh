#!/usr/bin/env bash
# Initialize the workspace: check runtime, create the data directory.
set -e

echo "node: $(node --version)"
mkdir -p data/documents
echo "init complete: data/documents ready"
