#!/usr/bin/env bash
# CI gate: run the eval suites. Non-zero exit blocks the ship on a regression.
cd "$(dirname "$0")"
python run_evals.py
