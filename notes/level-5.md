# Level 5 — Harden, Verify, Observe (notes + exit)

## READ
- *Demystifying Evals* + *Agent Evaluation Readiness Checklist*: grade what the
  agent produced, not the path; ~20 examples → ~100 for production; keep
  **capability** evals separate from **regression** evals.
- *How We Contain Claude* + *OWASP LLM01*: supervise what the agent CAN do
  (sandbox/VM/egress), not what it does; users approve ~93% of prompts;
  injection works because instructions + data share one channel. Red-team got
  Claude Code to exfiltrate AWS creds 24/25 runs.
- Sandbox skim: E2B (microVM) vs Daytona (persistent workspaces).

## BUILD
### ① CI evals — capability vs regression (`harness/evals/`)
- `run_evals.py`: CAPABILITY suite (informational) + REGRESSION suite (blocking).
  Regression failure → exit 1 so CI blocks the ship.
- Proof of the exit: `--demo-regression` reintroduces the old `"dd"`-substring
  bug → CI exits 1. Clean run → exit 0.
- **The suite caught a real latent bug immediately:** `WORKSPACE` was a relative
  path, so `within_workspace()` (comparing an absolute resolved path) wrongly
  denied legitimate sandbox writes when htools was imported from a subdir. Fixed
  by anchoring WORKSPACE with `os.path.abspath`. (Evals earning their keep.)

### ② Tracing — every inference + tool call (`harness/trace.py`)
- Span per step (name, kind, parent, duration, attrs) → JSONL; `print_tree()`
  reads it back. `trace_demo.py` shows a turn: inference + read + write(+verify
  nested), asserting every inference and tool call produced a span.

### ③ Lethal-trifecta check + config lock (`harness/security/trifecta_check.py`)
- Flags any config with ALL THREE legs (private data + untrusted content +
  egress) — the exfil scenario. Any two is survivable; break one leg.
- Extended the permission gate: writes to `settings.json` / `.mcp.json` /
  `hooks` / `.claude/` are DENIED — the agent can't widen its own permissions.

## Exit
> A regression is caught by CI before it ships; every step is traceable. ✅
CI exits 1 on an injected regression; the tracer emits a span for every
inference and tool call.
