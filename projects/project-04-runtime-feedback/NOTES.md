# Project 04 — my notes

## The problem
A silent bug: large documents only got their first 500 chars indexed, so Q&A
couldn't find anything past that. Nothing crashed — it just quietly failed.
Silent bugs are the expensive ones.

## Two different feedback tools, two different failure classes
| Tool | Catches | How it helped here |
|------|---------|--------------------|
| **Structured logging** | logic / runtime defects | one log line (`indexedChars:500, truncated:true`) pinpointed the truncation |
| **Architecture guard** | cross-layer / structural defects | enforced "only storage files touch `fs`"; stayed green (this bug wasn't structural) |

The lesson: don't reach for one tool for every problem. Logs find *what the code
did at runtime*; the guard prevents *whole categories* of coupling before they happen.

## Why logging beat code-reading
Without the log, finding this means reading `indexDoc`, suspecting the slice,
reasoning about lengths. With the log, the mismatch `bodyChars:1521` vs
`indexedChars:500` *is* the diagnosis — instant. Observability turns "hunt
through code" into "read the signal."

## Full output to file, summary to console
`logger.js` writes complete JSON records to `logs/app.log` but prints only a
short summary to the console — so the context window (or terminal) isn't flooded,
while the full detail is still on disk to grep. (Same principle as the main
harness: log full output to a file, feed only summaries back.)

## Takeaway
Runtime feedback = make the program tell you what it's doing. A good log line is
a pre-written diagnosis. A good guard is a bug that can never be written. Both
beat blind exploration.
