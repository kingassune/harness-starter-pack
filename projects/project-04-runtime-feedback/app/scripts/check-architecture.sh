#!/usr/bin/env bash
# Enforce the layer boundaries documented in docs/ARCHITECTURE.md.
# Run from the app/ directory.
violations=0

echo "== rule 1: UI layer (public/) must not use Node/storage APIs =="
if grep -rnE "require\(|process\.|child_process|\bfs\." public/ ; then
  echo "VIOLATION: UI references server-only APIs"
  violations=$((violations + 1))
else
  echo "ok"
fi

echo "== rule 2: only server.js and logger.js may touch the filesystem =="
for f in *.js; do
  case "$f" in
    server.js | logger.js) continue ;;
  esac
  if grep -nE "\bfs\.|require\(['\"]fs['\"]\)" "$f" ; then
    echo "VIOLATION: $f touches the filesystem but is not a storage-layer file"
    violations=$((violations + 1))
  fi
done
echo "ok"

if [ "$violations" -gt 0 ]; then
  echo "FAIL: $violations architecture violation(s)"
  exit 1
fi
echo "PASS: architecture boundaries respected"
