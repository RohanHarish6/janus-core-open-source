---
trigger: always_on
description: "Core 4-Tier zero-cost model routing, progressive disclosure, and token optimization protocols."
---
# Architecture & Model Routing Rules

1. Every task execution must evaluate complexity before routing:
   - Complexity < 0.2: AST / regex deterministic local execution.
   - Complexity 0.2 - 0.5: Tier 0 Ollama local edge model (`qwen2.5:3b`, `llama3.2:3b`).
   - Complexity 0.5 - 0.75: Tier 1 Colibri MoE v2 NVMe streaming engine.
   - Complexity >= 0.75: Tier 2 FreeLLMAPI or Tier 3 Frontier LLM.

2. Tool Registry:
   - In system prompts, expose ONLY single-line tool manifests (<25 tokens).
   - Resolve detailed JSON/Pydantic schemas dynamically on invocation.

3. State Management:
   - Never dump cumulative raw conversation logs into turns.
   - Compute delta diffs using `DeltaStateReducer` to maintain <500 token overhead.
