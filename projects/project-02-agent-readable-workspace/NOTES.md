# Project 02 — my notes

## The two sessions

### Starter session (thin workspace — no handoff docs)
A fresh agent dropped into just `server.js` + `public/index.html` has to
**rediscover** everything:
- read all of `server.js` to learn the endpoints and the document format
- infer what's done vs. in-progress (no status anywhere)
- guess how to run it and what "done" means
- risk redoing or breaking finished work because nothing says it's finished

→ high rediscovery cost, every session.

### Solution session (readable workspace + handoff)
A fresh agent reads four files and is oriented in seconds:
| Question a cold agent asks | Answered by |
|---|---|
| What is this and why? | `PRODUCT.md` |
| How is it structured? Doc format? Endpoints? | `ARCHITECTURE.md` |
| What's done vs. not, with proof? | `feature_list.json` |
| Where do I pick up? How do I run it? | `session-handoff.md` |

→ near-zero rediscovery. No verbal context needed.

## Resume drill (proof it works)
Without opening any source code, `session-handoff.md` + `feature_list.json` answer:
- **Done?** import, detail, persistence — all passing with evidence.
- **Run it?** `PORT=3003 node server.js` then curl `/api/documents`.
- **Next?** editing/deleting, re-add Q&A, then Project 03.
- **Gotcha?** `data/documents/` is gitignored runtime state; delete to reset.

## Takeaway
Project 01 showed structure beats prompts for *building*. Project 02 shows the
same for *handing off*: the harness mechanism here is "agent-readable workspace +
persistent state files." The docs cost a few minutes to write and erase the
rediscovery tax on every future session — yours or another agent's.
