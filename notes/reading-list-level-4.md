# Level 4 — Scale & Orchestrate: reading list

Links verified. Note: the long-running-agents piece describes almost exactly
what we built in Projects 3–6 (feature_list.json, init.sh, progress notes,
one-feature-per-session) — good confirmation we're on the right track.

## Choosing the Right Multi-Agent Architecture
- LangChain — https://www.langchain.com/blog/choosing-the-right-multi-agent-architecture
- Companion (Anthropic, how a real one is built) — https://www.anthropic.com/engineering/multi-agent-research-system
  > Multi-agent (Opus lead + Sonnet subagents) beat single-agent by ~90% on
  > their research evals — BUT: not a fit when all agents need the same context
  > or have many interdependencies. Add a 2nd agent only when isolation/
  > parallelism earns it.

## Effective Harnesses for Long-Running Agents
- Anthropic — https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents
  > An initializer agent runs once (writes feature_list.json + init.sh); a coding
  > agent is woken repeatedly, each session making incremental progress on ONE
  > feature, running tests, leaving a progress note, committing. Fresh context
  > each session; state recovered from the progress file + git history.

## The protocol map (MCP / A2A / AG-UI)
- Google Developers guide — https://developers.googleblog.com/developers-guide-to-ai-agent-protocols/
- MCP (agent ↔ tools) — https://modelcontextprotocol.io
- A2A (agent ↔ agent) — https://a2a-protocol.org
- AG-UI (agent ↔ human/UI) — https://docs.ag-ui.com
  > Complementary layers, not competitors: A2A coordinates agents, MCP connects
  > tools, AG-UI drives the interface. Like TCP/HTTP/HTML.
