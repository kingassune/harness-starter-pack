# AGENTS.md

> Project-level operating instructions for any AI agent working in this repo.
> Keep this file SHORT, STABLE, and HIGH-SIGNAL. It is loaded into the system
> prompt and survives context compaction — so put the rules here that must
> never be forgotten, not things the agent can discover by reading code.
>
> Rule of thumb: if losing a line mid-task would cause a bug, it belongs here.
> If the agent could figure it out from the codebase, leave it out.

---

## 1. What this project is

<!-- One paragraph. What the codebase does, who uses it, what "done" looks like. -->
- **Product:**
- **Primary language / runtime:**
- **Package manager:**
- **Where the entrypoint lives:**

## 2. How to work here (the loop)

The agent must follow this cycle on every task:

1. **Read** `PLAN.md` (if present) before doing anything. If absent, create one.
2. **Plan** — write/update milestones in `PLAN.md` before writing code.
3. **Act** — make the smallest change that advances the current milestone.
4. **Verify** — run the verification command below after every change.
5. **Record** — append decisions and deviations to `IMPLEMENT.md`.
6. Repeat until all milestones are `[x]`.

## 3. Commands

<!-- Exact, copy-pasteable. The agent should never guess these. -->
| Action            | Command                          |
|-------------------|----------------------------------|
| Install deps      | `…`                              |
| Run / dev server  | `…`                              |
| **Verify (tests)**| `…`  ← run after every change    |
| Lint / format     | `…`                              |
| Typecheck         | `…`                              |
| Build             | `…`                              |

> **Verification is mandatory.** A change is not complete until the verify
> command passes. Emit only summary lines to context; log full output to a file.

## 4. Conventions

- **Code style:**
- **Naming:**
- **File layout / where things go:**
- **Tests live in:**
- **Commit message format:**
- **Do NOT touch:** <!-- generated files, vendored dirs, lockfiles, etc. -->

## 5. Tool & permission boundaries

- **Allowed without asking:** read files, run tests, lint, typecheck, search.
- **Ask first (or open a PR for review):** schema/migration changes, deleting
  files, editing CI config, anything touching secrets or auth, network calls
  to external services, installing new dependencies.
- **Never:** commit secrets, force-push, edit this file's rules to widen its
  own permissions, modify hooks/sandbox config, or disable verification.

## 6. Definition of done

A task is done when **all** of the following are true:
- [ ] All `PLAN.md` milestones are checked off.
- [ ] The verify command passes cleanly.
- [ ] Lint + typecheck pass.
- [ ] No debug code, no commented-out blocks, no TODOs left for this task.
- [ ] `IMPLEMENT.md` records what changed and any open questions.

---

<!--
Maintainer notes:
- Review this file whenever the agent repeatedly makes the same mistake — that
  mistake is usually a missing line here.
- The shorter this file is, the more reliably the model honors it.
- Anything the model can now do reliably on its own should be DELETED. Every
  rule here is a temporary crutch; remove crutches as models improve.
-->
