# Harness Starter Pack

Four drop-in files to make any AI coding-agent session more reliable. Copy them
into the root of your repo, fill in the bracketed blanks, and your agent runs on
structure instead of vibes.

Companion to the **Harness Engineering: Zero to Hero** field manual.

## The files

| File | What it is | When the agent touches it |
|------|------------|---------------------------|
| `AGENTS.md` | Stable, high-signal repo rules. Loaded into the system prompt; survives compaction. | Read once at session start; rarely edited. |
| `PLAN.md` | The current task's milestones + verification gates. Durable task memory. | Created at task start; **updated every turn**. |
| `IMPLEMENT.md` | Running log of what was done, decisions, deviations, open questions. | Appended as work happens. |
| `HARNESS_CHECKLIST.md` | Pre-production review gate, grouped by harness primitive. | Walked before shipping. |

## How they fit together

```
AGENTS.md          → the rules of the house (stable)
   │
   ▼
PLAN.md            → what we're doing now + how we'll verify it (per task)
   │  observe → plan → act → verify → record
   ▼
IMPLEMENT.md       → what actually happened + why (history)
   │
   ▼
HARNESS_CHECKLIST  → are we safe to ship? (gate)
```

`AGENTS.md` is intent that never changes. `PLAN.md` is intent for *this* task.
`IMPLEMENT.md` is the history that explains the diff. `HARNESS_CHECKLIST.md` is
the gate before production.

## Quick start

1. Copy all four files to your repo root.
2. Fill in every `<…>` and bracketed blank in `AGENTS.md` — especially the
   **verify command**. That single line does most of the work.
3. Point your agent at the repo. In its first message, tell it:
   *"Read AGENTS.md, then create PLAN.md for: <your task>."*
4. Let it run the loop. Review `IMPLEMENT.md` instead of watching every step.
5. Before merging anything user-facing, walk `HARNESS_CHECKLIST.md`.

## The one principle

Every line in these files exists because the model can't do something reliably
*yet*. Those assumptions expire. When the model can do something on its own,
delete the rule. The best harness is the smallest one that still works.

---
Adapted from the templates in `ai-boost/awesome-harness-engineering` (CC0).
