# HARNESS_CHECKLIST.md

> Review checklist before shipping a harness to production. Walk it top to
> bottom. A box you can't honestly check is a risk you're shipping. Grouped by
> the harness primitive each item belongs to.
>
> Mirrors the "Hero Checklist" from the Harness Engineering field manual.

---

## Agent loop
- [ ] Explicit observe → plan → act → verify loop with **hard termination conditions**.
- [ ] Loop-detection / repeat-action guard in place.
- [ ] Reasoning concentrated at plan + verify phases ("reasoning sandwich").
- [ ] Thinking/scratch state preserved correctly across tool results.

## Planning
- [ ] Persistent planning artifact (`PLAN.md`) updated **each turn**, not just at the end.
- [ ] Replanning only triggers when the executor stalls — not on every step.
- [ ] Cross-session handoff state exists (commits, feature list, test gates).

## Context
- [ ] Compaction strategy in place (server-side or agent-controlled).
- [ ] Prompt caching enabled on system prompt + tool definitions.
- [ ] Critical rules live in `AGENTS.md` (survive compaction), not buried in history.
- [ ] Durable facts live in a structured store, **not** the context window.

## Tools
- [ ] Every tool: clear name, strict schema, useful error surface.
- [ ] Tool count minimized — no unused or rarely-used tools bloating context.
- [ ] Structured-output enforcement (no ad-hoc JSON parsing).
- [ ] Risk annotations present (read-only / destructive / idempotent / open-world).

## Permissions
- [ ] Least-privilege audit done (vs. OWASP LLM06 — Excessive Agency).
- [ ] Destructive actions gated; deny-by-default for headless / unattended runs.
- [ ] **Lethal-trifecta check:** no single agent has private-data access +
      untrusted-content exposure + external-comms ability unguarded.
- [ ] Agent cannot edit its own permission/hook/sandbox config.

## Memory & state
- [ ] Cross-session state defined and tested for resume-after-crash.
- [ ] Memory writes validated/gated (defends against prompt-injection writes).
- [ ] Stale-memory invalidation: facts are re-verified against current state.

## Orchestration
- [ ] Topology justified by isolation/parallelism need — not added for show.
- [ ] Checkpoint-resume works for long / multi-day tasks.
- [ ] Provider fallback on 429/500 (e.g. via a gateway/proxy).
- [ ] Per-run budgets: loop/step limits, tool-call caps, token + wall-clock limits.

## Verification & CI
- [ ] Verification runs **in-loop**, not only post-hoc.
- [ ] Capability evals separated from regression evals.
- [ ] CI gate blocks deploy on regression.
- [ ] Reliability measured with pass^k (all trials succeed), not single-shot.

## Observability
- [ ] Every inference + tool call traced (OTel GenAI conventions for portability).
- [ ] Cost / token attribution per run.
- [ ] Failure analysis surfaces **why** it failed, not just **that** it failed.

## Sandbox & security
- [ ] Agent code runs in an isolated sandbox (microVM / container / kernel policy).
- [ ] Network egress restricted; secrets injected outside the runtime.
- [ ] Hooks / MCP config protected from agent modification.
- [ ] Prompt-injection defenses applied to all untrusted input sources.

## Human-in-the-loop
- [ ] Human gates on high-risk actions, with "approve-with-changes" available.
- [ ] Humans **on** the loop (maintaining the harness), not reviewing every output.

## Feedback hygiene
- [ ] Test/tool output emits summary lines to context; full detail logged to file.

---

## The one question
> For every component above: **what is this assuming the model can't do?**
> If the answer is "nothing anymore" — delete it.
> The best harness is the smallest one that still works.
