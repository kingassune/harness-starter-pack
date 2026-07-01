#!/usr/bin/env bash
# Run the benchmark for the STRONG (all-on) and WEAK (all-off) harness configs.
cd "$(dirname "$0")/.." || exit 1

run() { HARNESS_ROLE_SEP=$1 HARNESS_FIX_CHUNKING=$2 HARNESS_PERSIST=$3 HARNESS_QUIET=on node scripts/bench.js | grep SCORE; }

echo "strong harness (all on): $(run on on on)"
echo "weak harness   (all off): $(run off off off)"
