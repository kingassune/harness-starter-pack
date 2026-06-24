# Level 1 — Foundations (reading notes)

Notes distilled from the Level 1 readings. The throughline across all of them:
**Agent = Model + Harness.** The model is the intelligence; the harness is
everything else that turns that intelligence into reliable work.

---

## 1. Harness Engineering — OpenAI ("leveraging Codex in an agent-first world")
- Harness engineering = designing the scaffolding around an agent: context
  delivery, tool interfaces, planning artifacts, verification loops, memory,
  and sandboxes. It's what decides whether the agent succeeds or fails.
- Reframes where effort goes: **code becomes cheap** (agents produce it in
  volume); what's expensive is the quality of the *environment* the agent runs in.
- OpenAI ran a 5-month internal experiment shipping a beta product (~1M LOC)
  with the agent writing the code and humans steering the harness.

## 2. Harness Engineering — Martin Fowler / Birgitta Böckeler ("first thoughts")
- Harnesses = **"cybernetic governors for AI agents"**: feedforward *guides*
  + feedback *sensors* forming control loops around the LLM.
- Two kinds of control:
  - **Computational controls** — deterministic tools (linters, tests, types).
  - **Inferential controls** — LLM-based semantic judgment (e.g. an LLM reviewer).
  - You need both.
- A harness *externalizes the implicit knowledge* a human dev brings — but
  can't fully replace human judgment. It's an evolving discipline, not a
  one-time config: humans steer by **iterating on the harness itself**.

## 3. Building Effective Agents — Anthropic
- Distinguishes **workflows** (LLM + tools on predefined code paths) from
  **agents** (LLM dynamically directs its own process + tool use).
- Five workflow patterns: **Prompt Chaining, Routing, Parallelization,
  Orchestrator–Worker, Evaluator/Optimizer.**
- Golden rule: **find the simplest thing that works.** Don't build an agent if
  a workflow (or no LLM loop at all) will do — agents trade latency + cost for
  flexibility.

## 4. Harness Design for Long-Running Application Development — Anthropic
- Long-running tasks fail in characteristic ways ("context anxiety", poor
  self-assessment). A multi-agent harness mitigates these.
- Example architecture: **Planner → Generator → Evaluator** (GAN-inspired).
  - Planner: turns a short prompt into an ambitious spec.
  - Generator: builds iteratively across rounds.
  - Evaluator: drives a live app (e.g. Playwright MCP), critiques, feeds back.
- Trade-off: more structure = more tokens + latency, but correctness/polish a
  solo model can't reach.

## 5. The Anatomy of an Agent Harness — LangChain
- **Agent = Model + Harness.** The harness is every piece of code, config, and
  execution logic that isn't the model: state, tool execution, feedback loops,
  enforceable constraints.
- Concrete proof it matters: LangChain moved their coding agent from ~Top 30 to
  **Top 5 on Terminal Bench 2.0 by only changing the harness** — same model.
- Frontier directions: hundreds of agents on a shared codebase; agents that
  read their own traces to fix harness-level failures; just-in-time tool/context
  assembly.

---

## Skim notes

### 6. Writing Effective Tools — Anthropic
- Name inputs unambiguously (`user_id`, not `user`). Build **high-leverage**
  tools, not thin API wrappers.
- Five principles: tool selection, namespacing, meaningful (human-readable)
  context, token efficiency (pagination/filtering/truncation), and
  prompt-engineered tool descriptions.
- Process: **Prototype → Evaluate → Collaborate.** Refining tool *descriptions*
  alone measurably improved SWE-bench results.

### 7. Beyond Permission Prompts — Anthropic (Claude Code auto mode)
- The tradeoff: approve every action (kills flow) vs skip permissions (no
  protection). Users accept ~93% of manual prompts anyway.
- Middle path: an **AI classifier** evaluates each tool call — safe actions
  proceed, risky ones get blocked (agent tries an alternative), repeated blocks
  escalate to a manual prompt. Maps to my Level 3 "gate destructive tools".

### 8. Demystifying Evals — Anthropic
- An eval = input + grading logic to measure success. Automated evals run in
  CI on every change/model upgrade — the first line of defense against
  regressions.
- Covers single- vs multi-turn, **trajectory vs outcome** metrics, LLM-judge
  calibration, rubrics. Relevant later at Level 5.

---

## What this means for MY build
- My harness's job: wrap Claude with a **loop + tools + verification +
  permission gate**, and keep it the *smallest* thing that works.
- Use **both** control types: deterministic checks (run a test/linter) AND an
  inferential check where judgment is needed.
- Treat the harness as something I **iterate on**, not configure once.
