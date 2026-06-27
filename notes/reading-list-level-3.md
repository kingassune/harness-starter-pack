# Level 3 — Build Your First Harness: reading list

Links verified June 2026.

## Work through a "Learn Harness Engineering" course
- Learn Harness Engineering (walkinglabs course, 6 hands-on projects) —
  https://walkinglabs.github.io/learn-harness-engineering/en/
- shareAI-lab/learn-claude-code ("Bash is all you need", 0→1 nano agent) —
  https://github.com/shareAI-lab/learn-claude-code

## Read a small agent core, front to back
- smolagents (HuggingFace; agent logic in ~1,000 lines) —
  https://github.com/huggingface/smolagents
- Sebastian Raschka (rasbt) coding-agent work —
  https://github.com/rasbt  ·  https://magazine.sebastianraschka.com/p/using-local-coding-agents
  > Note: the manual cites "rasbt/mini-coding-agent"; an exact repo by that name
  > wasn't found — closest is rasbt/local-coding-agent-evals. smolagents is the
  > reliable "read a small core front to back" target.

## Skill Issue: Harness Engineering for Coding Agents
- HumanLayer blog —
  https://www.humanlayer.dev/blog/skill-issue-harness-engineering-for-coding-agents
  > Thesis: weak agent results are usually *harness* problems, not *model*
  > problems. Context structure, tool clarity, constraint architecture > model
  > choice. Sub-agents for context control. A well-engineered harness "floats
  > on any model."
