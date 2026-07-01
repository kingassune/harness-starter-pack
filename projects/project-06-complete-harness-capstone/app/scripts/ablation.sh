#!/usr/bin/env bash
# Ablation: start from the strong config, remove ONE mechanism at a time, and
# measure the score drop. The bigger the drop, the more that component matters.
cd "$(dirname "$0")/.." || exit 1

run() { HARNESS_ROLE_SEP=$1 HARNESS_FIX_CHUNKING=$2 HARNESS_PERSIST=$3 HARNESS_QUIET=on node scripts/bench.js | grep -oE 'SCORE [0-9]+/[0-9]+'; }

echo "baseline strong (all on):   $(run on on on)"
echo "-- drop one mechanism --"
echo "  - role separation (P05):  $(run off on on)"
echo "  - chunking fix    (P04):  $(run on off on)"
echo "  - persistence     (P02/3):$(run on on off)"
echo "weak (all off):             $(run off off off)"
