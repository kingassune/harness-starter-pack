"""Level 5 — lethal-trifecta check + config-lock verification.

The lethal trifecta: an agent is dangerous when it has ALL THREE of
  A) access to private data,
  B) exposure to untrusted content, and
  C) an exfiltration / egress channel.
Any two is survivable; all three means injected instructions in untrusted
content can read private data and send it out (the AWS-cred-exfil scenario from
'How We Contain Claude'). Mitigation: break one leg.

Also verifies the permission gate locks hooks/MCP/settings config from edits.

Run: python trifecta_check.py   (exit 0 if detection + lock behave correctly)
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import htools  # noqa: E402

LEGS = ("private_data", "untrusted_content", "exfil_channel")

# name, config, expected_lethal
CONFIGS = [
    ("vuln-verifier (ours): reads code + untrusted input, NO egress",
     {"private_data": True, "untrusted_content": True, "exfil_channel": False}, False),
    ("email assistant: reads inbox + browses web + can send mail",
     {"private_data": True, "untrusted_content": True, "exfil_channel": True}, True),
    ("sandboxed math fixer: no private data, no egress",
     {"private_data": False, "untrusted_content": True, "exfil_channel": False}, False),
]


def assess(cfg):
    present = [leg for leg in LEGS if cfg.get(leg)]
    return len(present) == 3, present


def main():
    print("== lethal-trifecta detection ==")
    detector_ok = True
    for name, cfg, expected in CONFIGS:
        lethal, present = assess(cfg)
        ok = lethal == expected
        detector_ok = detector_ok and ok
        tag = "LETHAL" if lethal else "ok"
        print(f"  [{tag}] {name}")
        print(f"         legs={present}  detector={'PASS' if ok else 'FAIL'}")
        if lethal:
            print("         -> break a leg: sandbox the data, quarantine untrusted input, or cut egress")

    print("\n== config-lock (hooks/MCP/settings locked from agent edits) ==")
    lock_cases = [
        ("write_file", {"path": "settings.json"}, False),
        ("write_file", {"path": ".mcp.json"}, False),
        ("write_file", {"path": ".claude/hooks.json"}, False),
        ("write_file", {"path": "mathlib.py"}, True),  # ordinary sandbox file: allowed
    ]
    lock_ok = True
    for name, args, expected in lock_cases:
        allowed = htools.check_permission(name, args)[0]
        ok = allowed == expected
        lock_ok = lock_ok and ok
        print(f"  {'PASS' if ok else 'FAIL'}  write {args['path']} -> allowed={allowed}")

    ok = detector_ok and lock_ok
    print("\nRESULT:", "PASS" if ok else "FAIL",
          f"(detector={'ok' if detector_ok else 'BROKEN'}, lock={'ok' if lock_ok else 'BROKEN'})")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
