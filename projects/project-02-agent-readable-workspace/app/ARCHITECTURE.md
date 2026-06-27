# ARCHITECTURE

A single-process Node HTTP app. No framework, no build step.

## Layers
```
public/index.html   ← UI (renders panels, calls the API via fetch)
        │ HTTP/JSON
server.js           ← API + logic (routing, import, detail, list)
        │ fs read/write
data/documents/*.json   ← storage (one JSON file per document)
```

## Rules
- The UI talks to `server.js` only over HTTP/JSON — it never touches `data/`.
- `server.js` is the only layer that reads/writes `data/documents/`.
- A document is a JSON file: `{ "id", "title", "body" }`. Filename is `<id>.json`.
- `id` is a slug of the title, made unique by appending `-2`, `-3`, …

## Endpoints
| Method | Path | Purpose |
|--------|------|---------|
| GET | `/` | serve the UI |
| GET | `/api/documents` | list `{id,title}` |
| GET | `/api/documents/:id` | full document, or 404 |
| POST | `/api/documents` | import `{title,body}` → 201 with new doc |

## Run
`PORT=3003 node server.js` → http://localhost:3003
