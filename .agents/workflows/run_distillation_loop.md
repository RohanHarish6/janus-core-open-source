# /run-distillation-loop

Capture frontier teacher reasoning traces, export SFT/DPO datasets, and synthesize Ollama Modelfile.

## Steps
1. Initialize `AutonomousDistillationEngine`.
2. Ingest teacher thought chains and tool execution traces from high-scoring runs.
3. Export ShareGPT and DPO dataset files into `./datasets/distillation/`.
4. Synthesize custom Ollama `Modelfile.distilled` with embedded exemplars and tuned sampling parameters.
5. Benchmark local student frontier equivalence metrics and update persistent memory.
