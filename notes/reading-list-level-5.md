# Level 5 — Harden, Verify, Observe: reading list

Links verified.

## Evals
- Demystifying Evals — https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents
- Agent Evaluation Readiness Checklist (LangChain) — https://www.langchain.com/blog/agent-evaluation-readiness-checklist
  > Start with ~20 labeled examples, grow toward ~100 for production confidence.
  > Grade what the agent PRODUCED, not the path it took. Have the grader explain
  > its reasoning. Separate capability evals from regression evals.

## Security / containment
- How We Contain Claude Across Products (Anthropic) — https://www.anthropic.com/engineering/how-we-contain-claude
  > Supervise what the agent CAN do, not what it does: sandboxes, VMs, egress
  > controls. Agent security is a systems problem, not a model problem. Users
  > approve ~93% of permission prompts (so prompts alone don't protect). Red-team
  > test: an injected email got Claude Code to exfiltrate AWS creds 24/25 runs.
- OWASP LLM01: Prompt Injection — https://genai.owasp.org/llmrisk/llm01-prompt-injection/
  > Root cause: instructions and data share one channel; the model can't tell a
  > crafted "instruction" in content from real content. Direct vs indirect
  > (hidden in docs/web/email) injection.

## Skim a sandbox option
- E2B (microVM per session, ~150ms cold start; default for tool-call code exec) — https://e2b.dev
- Daytona (Docker, persistent workspaces; when the sandbox IS the workspace) — https://www.daytona.io
- Comparison — https://northflank.com/blog/daytona-vs-e2b-ai-code-execution-sandboxes

## For the Level 5 BUILD (tracing)
- Langfuse (open-source LLM observability, OTel-based) — https://langfuse.com
- OpenLLMetry (Traceloop, OpenTelemetry instrumentation) — https://www.traceloop.com/openllmetry
