"""Level 5 — lightweight tracing.

A span per inference and per tool call, written as JSON lines (OTel/Langfuse
shaped: name, kind, parent, duration, attrs). Full detail to a file; you read
the tree back with print_tree(). Wrap any step:

    tr = Tracer(path)
    with tr.span("inference", "llm", model=MODEL):
        ...
    with tr.span("tool.read_file", "tool", path=p):
        ...
"""
import json
import os
import time


class Tracer:
    def __init__(self, path):
        self.path = path
        self._id = 0
        self.stack = []
        os.makedirs(os.path.dirname(path), exist_ok=True)
        open(path, "w").close()

    def span(self, name, kind, **attrs):
        return _Span(self, name, kind, attrs)

    def _start(self, name, kind, attrs):
        self._id += 1
        sp = {
            "id": self._id,
            "name": name,
            "kind": kind,
            "parent": self.stack[-1] if self.stack else None,
            "attrs": attrs,
            "_t0": time.perf_counter(),
        }
        self.stack.append(self._id)
        return sp

    def _end(self, sp, out):
        sp["ms"] = round((time.perf_counter() - sp.pop("_t0")) * 1000, 2)
        sp["out"] = out
        self.stack.pop()
        with open(self.path, "a") as fh:
            fh.write(json.dumps(sp) + "\n")


class _Span:
    def __init__(self, tracer, name, kind, attrs):
        self.tracer, self.name, self.kind, self.attrs = tracer, name, kind, attrs
        self.out = {}

    def __enter__(self):
        self.sp = self.tracer._start(self.name, self.kind, self.attrs)
        return self

    def set(self, **out):
        self.out.update(out)

    def __exit__(self, *exc):
        self.tracer._end(self.sp, self.out)
        return False


def print_tree(path):
    spans = [json.loads(line) for line in open(path)]
    by_parent = {}
    for s in spans:
        by_parent.setdefault(s["parent"], []).append(s)

    def walk(parent, depth):
        for s in by_parent.get(parent, []):
            attrs = " ".join(f"{k}={v}" for k, v in s["attrs"].items())
            print(f"{'  ' * depth}• [{s['kind']}] {s['name']} ({s['ms']}ms) {attrs}")
            walk(s["id"], depth + 1)

    walk(None, 0)
    return spans
