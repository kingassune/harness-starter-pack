# Harness Starter Pack

Drop-in files to make any AI coding-agent session more reliable. Copy them
into the root of your repo, fill in the bracketed blanks, and your agent runs on
structure instead of vibes.

Companion to the **Harness Engineering: Zero to Hero** field manual
([included in this repo](./Harness-Engineering-Zero-to-Hero.pdf)).

## The files

| File | What it is | When the agent touches it |
|------|------------|---------------------------|
| `AGENTS.md` | Stable, high-signal repo rules. Loaded into the system prompt; survives compaction. | Read once at session start; rarely edited. |
| `PLAN.md` | The current task's milestones + verification gates. Durable task memory. | Created at task start; **updated every turn**. |
| `IMPLEMENT.md` | Running log of what was done, decisions, deviations, open questions. | Appended as work happens. |
| `HARNESS_CHECKLIST.md` | Pre-production review gate, grouped by harness primitive. | Walked before shipping. |
| `PROGRESS.md` | Zero-to-Hero leveling tracker (READ/BUILD tasks + scorecard). | Checked off as you learn + build. |
| `Harness-Engineering-Zero-to-Hero.pdf` | The full field manual this pack accompanies. | Reference; read alongside `PROGRESS.md`. |

## How they fit together

```
AGENTS.md          \u2192 the rules of the house (stable)
   \u2502
   \u25bc
PLAN.md            \u2192 what we're doing now + how we'll verify it (per task)
   \u2502  observe \u2192 plan \u2192 act \u2192 verify \u2192 record
   \u25bc
IMPLEMENT.md       \u2192 what actually happened + why (history)
   \u2502
   \u25bc
HARNESS_CHECKLIST  \u2192 are we safe to ship? (gate)

PROGRESS.md        \u2192 your Zero-to-Hero learning + build tracker (alongside it all)
```

`AGENTS.md` is intent that never changes. `PLAN.md` is intent for *this* task.
`IMPLEMENT.md` is the history that explains the diff. `HARNESS_CHECKLIST.md` is
the gate before production. `PROGRESS.md` tracks your journey through the field
manual.

## Quick start

1. Copy the starter files to your repo root.
2. Fill in every `<\u2026>` and bracketed blank in `AGENTS.md` \u2014 especially the
   **verify command**. That single line does most of the work.
3. Point your agent at the repo. In its first message, tell it:
   *"Read AGENTS.md, then create PLAN.md for: <your task>."*
4. Let it run the loop. Review `IMPLEMENT.md` instead of watching every step.
5. Before merging anything user-facing, walk `HARNESS_CHECKLIST.md`.
6. Track your own learning + build progress in `PROGRESS.md`.

## The one principle

Every line in these files exists because the model can't do something reliably
*yet*. Those assumptions expire. When the model can do something on its own,
delete the rule. The best harness is the smallest one that still works.

## License

Released under [CC0 1.0 Universal](./LICENSE) \u2014 public domain, no rights reserved.
Adapted from the templates in `ai-boost/awesome-harness-engineering` (CC0).
