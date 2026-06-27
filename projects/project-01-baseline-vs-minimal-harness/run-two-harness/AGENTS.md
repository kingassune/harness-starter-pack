# AGENTS.md — knowledge-base app (harness run)

## What this is
A minimal local knowledge-base app: a document-list panel, a Q&A panel grounded
in those documents, and a local data directory that persists documents.

## How to work here
1. Run `./init.sh` before anything else — it checks the runtime and creates the
   data directory.
2. Implement features in the order listed in `feature_list.json`, one at a time.
3. Mark a feature `"passing"` ONLY after you have concrete verification evidence
   (a real command + its output). Record that evidence in `claude-progress.md`.
4. Verify by curling the running server — never assume an endpoint works.

## Conventions
- Entry point: `server.js`. UI: `public/index.html`. Data: `data/documents/`.
- Documents are JSON files: `{ "id", "title", "body" }`.
- Lowercase, hyphenated filenames.

## Done means
Every feature in `feature_list.json` is `"passing"` with evidence, and the app
still works after a restart.
