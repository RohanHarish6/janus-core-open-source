# Janus Core Engine: Antigravity Agent Workspace Guidelines

You are an autonomous engineering agent inside Google Antigravity working on **Janus Core**, a production-grade, token-efficient, multi-agent AI engine.

## Core Architectural Invariants (Non-Negotiable)

1. **Hardware Constraints (Dell Inspiron 5410 Baseline)**:
   - Target Platform: Intel Core i5 (11th Gen), 16 GB DDR4 RAM, PCIe NVMe SSD, Windows 11.
   - Max Resident Memory: 4.5 GB RAM hard ceiling.
   - CPU Thermal Tripwire: 85.0°C. Throttle concurrency to 2 threads if exceeded.
   - Default Thread Concurrency: 4 worker threads on AC power; 2 on Battery Saver.

2. **Model Routing Hierarchy (Zero-Cost First)**:
   - **Tier 0 (Local Free)**: Ollama (`janus-coder:3b`, `janus-distilled:3b`, `janus-reasoner:3b`, `janus-distilled:1.5b`, `janus-r1:7b`) — $0.00 / 0 paid tokens.
   - **Tier 1 (Disk-Streaming MoE)**: Colibri MoE v2 (`JustVugg/colibri` GLM-5.2 744B simulation) — 9.9 GB resident dense weights, streaming experts from NVMe SSD with predictive prefetching — $0.00 / 0 paid tokens.
   - **Tier 2 (Free Cloud)**: FreeLLMAPI / HuggingFace free endpoints — $0.00 / 0 paid tokens.
   - **Tier 3 (Frontier Cloud)**: Gemini 1.5 Pro / Claude 3.5 Sonnet / GPT-4o — Used strictly when complexity >= 0.75 or explicit high-stakes reasoning is required.
   - Target Zero-Cost Offload Ratio: >= 75.0%.

3. **Token Optimization Protocols**:
   - **Progressive Disclosure**: Tools must be registered with single-line manifests (<25 tokens/tool) in the prompt. Full Pydantic schemas are expanded only on invocation.
   - **Delta State Reduction**: Transmit only state diffs (<500 tokens/turn) instead of cumulative dialogue history.
   - **Prefix Cache Optimization (APC)**: Maintain static prompt prefixes across turns to ensure >95% cache hit rates on provider APIs.
   - **Context Compaction**: Apply LLMLingua-2 for inputs (>=2x compression) and Traversaal for intermediate outputs (>=3.5x compression).

4. **Security & Governance Standards**:
   - NIST SP 800-218 SSDF v1.1 compliant.
   - OWASP Top 10 for LLMs (2026 Edition):
     - LLM01: Dual-phase prompt injection defense.
     - LLM02: Sensitive data redaction (PII/tokens).
     - LLM06: Unbounded consumption circuit breakers (4k subtask / 16k session token ceilings).
     - LLM10: Improper output handling sanitizer (HTML/JS/XSS stripping).
   - AST / Sandbox Verification: All dynamic code execution must pass AST security vetting before evaluation.

5. **Testing & Code Quality**:
   - Run tests via `python run_tests.py` or `python -m unittest discover tests/`.
   - Never commit code that breaks any of the 115 unit tests.

6. **Speculative Decoding & DAG Swarms (v2.0.0)**:
   - Use  for edge draft acceleration (K=4, >80% acceptance target).
   - Use  for parallel subagent workflows with topological batching and cycle detection.

7. **Hybrid Vector-Graph Memory (v2.0.0)**:
   - Use  for semantic retrieval + knowledge graph subgraph consolidation.
   - Bound recalled context strictly under 300 tokens using  tags.
   - Enforce HMAC-SHA256 signature verification to prevent indirect memory tampering (OWASP LLM08).

8. **Autonomous GitHub Ingestion & Zero-Touch CI/CD (v2.0.0)**:
   - Use  to scan open-source radar and audit candidate patches via AST security verification.
   - Enforce  to generate GitHub Actions workflows and synchronization manifests bridging Google Drive to GitHub.
   - Guard against broken builds with automatic rollback if any of the 115 unit tests fail.

9. **Distributed Edge LAN Federation & P2P MoE Sharding (v2.0.0)**:
   - Use  to shard MoE expert layers across local RFC 1918 LAN devices.
   - Enforce private subnet boundaries (, , ) and HMAC-SHA256 handshake tokens.
   - Maintain seamless fallback to local NVMe disk-streaming if a LAN peer disconnects.

10. **Autonomous Knowledge Distillation & Self-Improving Machine (v2.0.0)**:
   - Use  to capture high-scoring teacher reasoning traces (Gemini/Claude/Llama 70B).
   - Inject distilled few-shot exemplars into local prompt prefixes to elevate 3B models to frontier equivalence.
   - Maintain continuous ShareGPT/DPO datasets and synthesize custom Ollama .

11. **Dynamic Token-Limit & Context-Expansion Handoff (v2.0.0)**:
   - Use  to monitor context capacity and quota buckets in real-time.
   - Pre-emptively shift requests exceeding 85% context to fuller models (8k -> 32k -> 131k -> 1M).
   - Reactively catch 429 rate limits, isolate exhausted providers, and route to the fullest available token bucket.

12. **Unlimited Token Replenishment System (v2.0.0)**:
   - Use  to pool Google AI Studio (1M TPM), Groq, Cloudflare, GitHub Models, and OpenRouter free tiers.
   - Cycle between leaky-bucket replenishing providers to regenerate ~19,666+ tokens/sec at /usr/bin/bash.00.
   - Backed by local Ollama/Colibri as an infinite zero-cost baseline.

13. **ISO/IEC 42001:2023 AI Governance & Edge Multimodal Adaptation (v2.0.0)**:
   - Use  to verify Annex A controls (A.5-A.9) and emit SHA-256 compliance attestations.
   - Use  to downsample vision tokens (>84% compression) and route to local/free vision models at /usr/bin/bash.00.

14. **Unified Zero-Conflict Unlimited Token Orchestrator (v2.0.0)**:
   - Use  to enforce zero conflict across token replenishment, context expansion, speculative drafting, and LAN MoE sharding.
   - Enforce in-tier cloud bucket rotation on 429 errors without premature paid tier jumps.

15. **Autonomous Model Switching & Continuous Task Execution**:
   - Zero-Intervention Invariant: If an active model runs out of output tokens or triggers rate limits (429/ResourceExhausted), the agent MUST NEVER halt or request manual user intervention.
   - Dynamic Downward/Lateral Failover: When higher tiers hit context/token ceilings, automatically cascade to the infinite zero-cost safety net (`ModelTier.LOCAL_OLLAMA`) with zero token drop.
   - Unbroken Execution Loop: Checkpoint active tasks into `state_checkpoint.json` and resume the active breakpoint on the destination engine immediately without prompting the user.
