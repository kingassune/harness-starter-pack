# Level 2 — Design Primitives (build notes + exit)

## What I built
Evolved `harness/loop.py` from a chat loop into a **tool-using verification
agent**:
- `tools.py` — 3 tools with strict schemas (`additionalProperties:false` +
  `required` on every one):
  - `read_file` — read-only, returns numbered source
  - `run_command` — read-only evidence gathering (grep/cat/ls)
  - `report_finding` — the verdict, forced through a strict schema with a
    `severity` enum. This is **structured-output enforcement**: we read a
    validated dict, never hand-parse JSON. `validate_finding()` double-checks
    required keys.
- Prompt caching: `cache_control` on the system prompt + last tool def (caches
  the whole tools array). NOTE: the cacheable prefix is currently just under the
  ~1024-token cache minimum, so `cache_read/write` show 0 for now — the wiring
  is correct and engages automatically as the prefix grows.
- `examples/vulnerable_login.py` — a SQL-injection sample as the target.

## E2E result
`python loop.py --smoke` → PASS (exit 0). Agent: read_file → run_command(grep)
→ report_finding = **SQL Injection / critical / line 14**, with evidence,
exploit (`admin' --`), and a parameterized-query fix.

## Exit criterion — the 12 primitives mapped to a loop stage
(Loop = Observe → Plan → Act → Verify. Primitives per `HARNESS_CHECKLIST.md`.)

| # | Primitive | Primary loop stage | Why |
|---|-----------|--------------------|-----|
| 1 | Agent loop | (all four) | It *is* the cycle that runs the rest. |
| 2 | Planning | Plan | Decide the steps before acting. |
| 3 | Context | Observe | What the model sees each turn. |
| 4 | Tools | Act | How the model affects the world. |
| 5 | Permissions | Act (gate) | Checked before a side-effecting act. |
| 6 | Memory & state | Observe | Carries facts across turns into context. |
| 7 | Orchestration | Plan / Act | Coordinating multiple agents/steps. |
| 8 | Verification & CI | Verify | Did the change actually work? |
| 9 | Observability | Verify | See what the system did (traces/metrics). |
| 10 | Sandbox & security | Act (containment) | Bounds the blast radius of acting. |
| 11 | Human-in-the-loop | Verify / Act | Human approval gate on risky acts. |
| 12 | Feedback hygiene | Observe | Only summaries flow back into context. |

Framework run E2E: ✅. All 12 named + mapped: ✅.
