# harness/ — the accumulating build

This directory is the real harness the PROGRESS.md BUILD column grows, level by
level. It starts as one model call inside a loop and ends (Level 6) as a
budget-capped, self-healing, evaluated agent.

**Stack:** Python + the raw Anthropic SDK (Messages API). We build the loop by
hand on purpose — that's the Level 3 lesson.

## Setup

```bash
cd harness
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env          # then paste your real ANTHROPIC_API_KEY into .env
```

Load the key into your shell (or use a tool like `direnv`/`python-dotenv`):

```bash
export $(grep -v '^#' .env | xargs)
```

## Run

```bash
python loop.py            # interactive REPL — chat with Claude in a loop
python loop.py --smoke    # one canned call; the Level 1 verify gate
```

## Verify

A change isn't done until this passes (needs ANTHROPIC_API_KEY):

```bash
python loop.py --smoke    # exits 0 and prints "PASS" on one successful call
```

## Level map (what gets added here)

| Level | Added to this dir |
|-------|-------------------|
| 1 | `loop.py` — one model call inside a loop ✅ |
| 2 | tools w/ strict schemas, structured output, prompt caching |
| 3 | observe→plan→act→verify, writes `PLAN.md`, permission gate, test-after-change |
| 4 | sandbox, checkpoint-resume |
| 5 | CI evals, tracing, injection hardening |
| 6 | budget caps, pass^k backtest, self-heal → fix PR |
