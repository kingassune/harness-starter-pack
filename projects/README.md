# Learn Harness Engineering — Projects Workbook

Local, self-contained version of the 6 hands-on projects from
[Learn Harness Engineering](https://walkinglabs.github.io/learn-harness-engineering/en/projects/),
brought into this repo so they can be completed here.

> **Note on the starter code:** the upstream course layers each project on a
> shared Electron knowledge-base app (document import → indexing → grounded
> Q&A). The course states that app is "a teaching vehicle, not for its
> complexity." The upstream repo can't be cloned from this environment (network
> is scoped to this repo), so this workbook reproduces what actually teaches the
> lesson — **the harness artifacts and the tasks** — and lets you build them
> against our own `harness/` agent (or any product code) as the substrate.

## How to use
1. Open a project's `BRIEF.md` and read the objective + tasks.
2. Do the work in that project's `starter/` folder (create the harness
   artifacts the brief asks for).
3. Capture results/answers in `NOTES.md` inside the project folder.
4. Check the box below and commit.

## The 6 projects

| # | Project | Harness lesson | Status |
|---|---------|----------------|--------|
| 1 | [Prompt-Only vs. Rules-First](./project-01-baseline-vs-minimal-harness/BRIEF.md) | Rules/checklists/init beat raw prompts | ☑ |
| 2 | [Agent-Readable Workspace](./project-02-agent-readable-workspace/BRIEF.md) | Readable repo + handoff docs | ☑ |
| 3 | [Multi-Session Continuity](./project-03-multi-session-continuity/BRIEF.md) | State files + verification-gated progress | ☑ |
| 4 | [Runtime Feedback & Scope Control](./project-04-runtime-feedback/BRIEF.md) | Structured logging + architecture guards | ☑ |
| 5 | [Self-Verification & Role Separation](./project-05-self-verification-role-separation/BRIEF.md) | Plan/Gen/Eval split catches defects | ☐ |
| 6 | [Complete Harness (Capstone)](./project-06-complete-harness-capstone/BRIEF.md) | Assemble all five + benchmark + ablation | ☐ |

> These map directly onto the PROGRESS.md **Level 3** READ item
> ("Work through *Learn Harness Engineering*").
