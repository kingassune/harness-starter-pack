# PROGRESS.md — Zero to Hero Checklist

> Your single tracker for the **Harness Engineering: Zero to Hero** field manual.
> Each level has two columns of work: **READ** (absorb the concept) and **BUILD**
> (do it with your hands). Don't advance a level until both sides are checked.
>
> Check a box the moment it's true. Keep this file in your repo root next to
> `AGENTS.md` — your agent can read your progress too.

---

## How to use this
- Work top to bottom. The levels build on each other.
- A level isn't done until its **exit criterion** at the bottom is met.
- The BUILD tasks accumulate into one real, shippable harness by Level 6.
- Stuck on a BUILD task? The matching READ item tells you where to look.

---

## ▢ Level 0 — Orientation

**READ**
- [ ] Read the Orientation + Mental Model pages.
- [ ] Write your own one-paragraph definition of "harness."
- [ ] Draw the loop (observe → plan → act → verify) and the 5 primitives from memory.

**BUILD**
- [ ] Pick the task your first harness will tackle (one concrete, verifiable thing).
- [ ] Pick your stack: model/provider + framework (Claude Agent SDK or LangGraph).

**Exit:** you can explain what a harness is and why every component is temporary.

---

## ▢ Level 1 — Foundations

**READ**
- [ ] Both *Harness Engineering* essays (OpenAI + Fowler).
- [ ] *Building Effective Agents* (Anthropic).
- [ ] *Harness Design for Long-Running Application Development*.
- [ ] *The Anatomy of an Agent Harness* (LangChain).
- [ ] Skim *Writing Effective Tools* / *Beyond Permission Prompts* / *Demystifying Evals*.

**BUILD**
- [ ] Install your chosen framework; run its quickstart end to end.
- [ ] Confirm you can make one successful model call inside a loop.

**Exit:** you can name the 4 loop steps, 5 primitives, and why assumptions expire.

---

## ▢ Level 2 — Design Primitives

**READ** — one pass per primitive
- [ ] Agent Loop (ReAct + LangGraph low-level).
- [ ] Planning (Plan-and-Execute).
- [ ] Context (Compaction + Prompt Caching).
- [ ] Tool Design (Writing Effective Tools + Tool Annotations).
- [ ] Skills & MCP (MCP intro + Code Execution with MCP).
- [ ] Permissions (Beyond Permission Prompts + OWASP LLM06).
- [ ] Memory (Letta / mem0).
- [ ] Skim: Orchestration, Verification, Observability, Debugging, HITL.

**BUILD**
- [ ] Define 3–5 tools with clear names + strict schemas.
- [ ] Add structured-output enforcement (no ad-hoc JSON parsing).
- [ ] Turn on prompt caching for system prompt + tool defs.

**Exit:** all 12 primitives named, each mapped to a loop stage, framework run E2E.

---

## ▢ Level 3 — Build Your First Harness

**READ**
- [ ] Work through *Learn Harness Engineering* course (or shareAI-lab/learn-claude-code).
- [ ] Read smolagents or rasbt/mini-coding-agent core, front to back.
- [ ] Read *Skill Issue: Harness Engineering for Coding Agents*.

**BUILD — the "Hello, Harness" milestone**
- [ ] Loop runs observe → plan → act → verify.
- [ ] Writes a `PLAN.md` and updates it each turn.
- [ ] Destructive tools gated behind a permission check.
- [ ] Runs a test after every change; feeds **only summary lines** back to context.
- [ ] Logs full output to a file, not the context window.

**Exit:** a single-agent harness completes your Level 0 task on its own.

---

## ▢ Level 4 — Scale & Orchestrate

**READ**
- [ ] *Choosing the Right Multi-Agent Architecture*.
- [ ] *Effective Harnesses for Long-Running Agents*.
- [ ] The protocol map (MCP / A2A / AG-UI).

**BUILD**
- [ ] Add a sandbox (E2B or Daytona) for code execution.
- [ ] Add a second specialized agent **only if** isolation/parallelism earns it.
- [ ] Add checkpoint-resume so a long task survives a restart.

**Exit:** harness handles a task bigger than one context window without losing progress.

---

## ▢ Level 5 — Harden, Verify, Observe

**READ**
- [ ] *Demystifying Evals* + *Agent Evaluation Readiness Checklist*.
- [ ] *How We Contain Claude* + OWASP LLM01 (prompt injection).
- [ ] Skim a sandbox option (E2B / Daytona / NVIDIA OpenShell).

**BUILD**
- [ ] Add promptfoo CI evals — capability evals separate from regression evals.
- [ ] Add tracing (Langfuse or OpenLLMetry) on every inference + tool call.
- [ ] Run the lethal-trifecta check; lock hooks/MCP config from agent edits.

**Exit:** a regression is caught by CI before it ships; every step is traceable.

---

## ▢ Level 6 — Ship to Production

**READ**
- [ ] *State of Agent Engineering 2026* (mind the eval gap).
- [ ] *FinOps for Agents* + a cost-optimization guide.
- [ ] *Backtesting AI Agents* (pass^k).

**BUILD**
- [ ] Gateway budget caps: loop/step limits, tool-call caps, token + wall-clock limits.
- [ ] Backtest with pass^k (dataset: 20% golden / 30% edge / 20% adversarial / 30% regression).
- [ ] Wire a self-heal path: detect regression → attribute → open fix PR.

**Exit:** harness runs unattended within budget and recovers from its own failures.

---

## ▢ Final — Hero Gate

- [ ] Walk every item in `HARNESS_CHECKLIST.md`; no honest box left unchecked.
- [ ] Copy + customize all four starter files (`AGENTS.md`, `PLAN.md`, `IMPLEMENT.md`, `HARNESS_CHECKLIST.md`).
- [ ] For every component, ask: *what is this assuming the model can't do?* Delete the crutches it no longer needs.
- [ ] **Ship it.**

---

### Scorecard
| Level | Read | Build | Exit met |
|-------|------|-------|----------|
| 0 — Orientation | ☐ | ☐ | ☐ |
| 1 — Foundations | ☐ | ☐ | ☐ |
| 2 — Primitives  | ☐ | ☐ | ☐ |
| 3 — Build       | ☐ | ☐ | ☐ |
| 4 — Scale       | ☐ | ☐ | ☐ |
| 5 — Harden      | ☐ | ☐ | ☐ |
| 6 — Ship        | ☐ | ☐ | ☐ |
| Hero Gate       | — | — | ☐ |

> The best harness is the smallest one that still works.
