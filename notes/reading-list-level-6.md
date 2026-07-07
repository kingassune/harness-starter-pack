# Level 6 — Ship to Production: reading list

Links verified.

## State of Agent Engineering 2026 (mind the eval gap)
- LangChain — https://www.langchain.com/state-of-agent-engineering
  > 89% of teams have observability but only 52% have evals — a 37-point gap
  > "where production quality dies." (We closed it at L5: we have BOTH tracing
  > and CI evals.)

## FinOps for Agents + cost optimization
- FinOps for AI (FinOps Foundation) — https://www.finops.org/wg/finops-for-ai-overview/
- Token economics / cost guide — https://zylos.ai/research/2026-02-19-ai-agent-cost-optimization-token-economics/
  > Agents cost 3–10× a plain chat call (multi-turn context, tool overhead, loop
  > iterations). Budget + max-iteration caps are ESSENTIAL, not optional. Prompt
  > caching ~90% off cached input; 30–200× spend variance unoptimized vs tuned.

## Backtesting AI Agents (pass^k)
- pass@k vs pass^k (Phil Schmid) — https://www.philschmid.de/agents-pass-at-k-pass-power-k
- Backtesting for reliability — https://drdroid.io/blog/backtesting-ai-agents-how-sre-teams-prove-reliability-before-production
  > pass@k = solved if ≥1 of k attempts works (capability). pass^k = solved only
  > if ALL k attempts work (consistency, tau-bench). High pass@k + low pass^k =
  > "benchmarks well, fails in production." Ship on pass^k, not pass@k.
