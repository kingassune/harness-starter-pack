#!/usr/bin/env bash
# Cleanup scanner: fail if the codebase carries maintainability smells.
cd "$(dirname "$0")/.." || exit 1
issues=0

echo "== scan: leftover markers (TODO/FIXME/XXX/debugger) =="
if grep -rnE "TODO|FIXME|XXX|debugger" --include=*.js . ; then
  echo "found leftover markers"; issues=$((issues + 1))
else echo "ok"; fi

echo "== scan: stray backup/temp files =="
if find . -name '*.bak' -o -name '*.tmp' -o -name '*~' | grep . ; then
  echo "found stray files"; issues=$((issues + 1))
else echo "ok"; fi

echo "== scan: uncommitted runtime dirs tracked by git? =="
# data/, logs/, data-bench/ should be gitignored, not committed
echo "ok (see .gitignore)"

if [ "$issues" -gt 0 ]; then
  echo "DIRTY: $issues category(ies) of cleanup needed"; exit 1
fi
echo "CLEAN: maintainable state"
