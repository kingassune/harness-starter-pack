"""Run logger — full detail goes to a file; the context window only ever sees
short summaries the harness returns. (Level 3: log full output to a file.)"""
import json
import os

LOG_DIR = os.path.join(os.path.dirname(__file__), "logs")
LOG_FILE = os.path.join(LOG_DIR, "harness-run.log")
CAP = 20000  # never write an unbounded blob


def start():
    """Begin a fresh run log; return its path."""
    os.makedirs(LOG_DIR, exist_ok=True)
    open(LOG_FILE, "w").close()
    return LOG_FILE


def log(event, **data):
    line = json.dumps({"event": event, **data}, default=str)
    with open(LOG_FILE, "a") as fh:
        fh.write(line[:CAP] + "\n")


def summarize(text, limit=200):
    """One-line summary for the context window; full text is already in the log."""
    text = (text or "").strip().replace("\n", " ")
    return text if len(text) <= limit else text[:limit] + f" …(+{len(text) - limit} chars in log)"
