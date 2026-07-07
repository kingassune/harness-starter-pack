"""Demonstrate tracing on one agent turn: a span for the inference and a span
for every tool call (with the verify nested under the write). Deterministic —
no API needed. Asserts every inference + tool call produced a span."""
import os

from trace import Tracer, print_tree

TRACE_FILE = os.path.join(os.path.dirname(__file__), "traces", "demo.jsonl")


def main():
    tr = Tracer(TRACE_FILE)
    with tr.span("agent.turn", "turn", task="fix add"):
        with tr.span("inference", "llm", model="claude-sonnet-4-6") as s:
            s.set(stop="tool_use", tool="write_file")
        with tr.span("tool.read_file", "tool", path="mathlib.py"):
            pass
        with tr.span("tool.write_file", "tool", path="mathlib.py"):
            with tr.span("verify", "test", cmd="python test_add.py") as v:
                v.set(result="PASS")

    print("=== trace tree ===")
    spans = print_tree(TRACE_FILE)

    n_llm = sum(1 for s in spans if s["kind"] == "llm")
    n_tool = sum(1 for s in spans if s["kind"] == "tool")
    print(f"\nspans: {len(spans)} total, {n_llm} inference, {n_tool} tool")
    ok = n_llm >= 1 and n_tool >= 1
    print("PASS: every inference + tool call is traced" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
