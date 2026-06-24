"""Level 1 build — the smallest possible harness.

A loop that takes input, makes ONE Claude model call per turn, and prints the
reply. That's it. This is the seed the later levels grow:

    Level 2  -> tools + strict schemas + structured output
    Level 3  -> observe -> plan -> act -> verify, PLAN.md, permission gate
    Level 4+ -> sandbox, checkpoint-resume, evals, tracing, budgets

Keep this file readable. Every line we add later is a temporary crutch the
model may not need forever (see AGENTS.md).

Run:
    python loop.py            # interactive REPL
    python loop.py --smoke    # one canned call, used as the verify gate
"""

import os
import sys

from anthropic import Anthropic

MODEL = os.environ.get("MODEL", "claude-sonnet-4-6")
MAX_TOKENS = 1024


def require_key():
    """Fail fast and friendly if the API key is missing."""
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print(
            "error: ANTHROPIC_API_KEY is not set.\n"
            "  cp .env.example .env, paste your key, then:\n"
            "  export $(grep -v '^#' .env | xargs)",
            file=sys.stderr,
        )
        raise SystemExit(2)


def reply(client, messages):
    """One model call. Returns the assistant's text."""
    resp = client.messages.create(
        model=MODEL,
        max_tokens=MAX_TOKENS,
        messages=messages,
    )
    return "".join(block.text for block in resp.content if block.type == "text")


def run_repl():
    """The loop: read -> call model -> print, carrying conversation history."""
    client = Anthropic()  # reads ANTHROPIC_API_KEY from the environment
    messages = []
    print(f"harness loop — model={MODEL}. Type 'exit' to quit.\n")
    while True:
        try:
            user = input("you> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if not user:
            continue
        if user.lower() in {"exit", "quit"}:
            break
        messages.append({"role": "user", "content": user})
        text = reply(client, messages)
        print(f"claude> {text}\n")
        messages.append({"role": "assistant", "content": text})


def run_smoke():
    """Verify gate: prove one successful model call inside the loop.

    Exits 0 on a non-empty reply, 1 otherwise. This is the Level 1 BUILD
    exit check — 'one successful model call inside a loop'.
    """
    client = Anthropic()
    messages = [{"role": "user", "content": "Reply with exactly: harness online"}]
    text = reply(client, messages).strip()
    print(f"smoke reply: {text!r}")
    if not text:
        print("FAIL: empty reply", file=sys.stderr)
        return 1
    print("PASS: one model call succeeded inside the loop")
    return 0


def main():
    require_key()
    if "--smoke" in sys.argv[1:]:
        return run_smoke()
    run_repl()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
