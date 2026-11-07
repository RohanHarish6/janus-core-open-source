"""
create_frontier_models.py - Compiles and registers the Janus Frontier Local Model Suite in Ollama.
Equips local models with Gemini 3 Flash / Claude 3.5 Sonnet frontier capabilities:
- janus-distilled:1.5b (Ultra-fast edge parser & drafter)
- janus-reasoner:3b (Deep analytical synthesis & comparative reasoning)
- janus-coder:3b (Production code generation & AST verification)
- janus-r1:7b (Scientific & mathematical chain-of-thought oracle)
"""

import subprocess
import sys
from pathlib import Path

MODELS_DIR = Path("./datasets/distillation")
MODELS_DIR.mkdir(parents=True, exist_ok=True)

MODEL_CONFIGS = [
    {
        "name": "janus-distilled:1.5b",
        "base": "qwen2.5:1.5b",
        "modelfile": "Modelfile.distilled_1.5b",
        "temperature": 0.3,
        "top_p": 0.9,
        "num_ctx": 4096,
        "system": (
            "You are Janus Distilled Edge Engine, an ultra-fast high-precision reasoning AI.\n"
            "Directives:\n"
            "1. Deliver clear, direct, and factual answers in clean Markdown.\n"
            "2. Think step-by-step in a brief <thought>...</thought> block before answering.\n"
            "3. Eradicate corporate jargon, buzzwords, and canned disclaimers.\n"
            "4. Structure answers with relevant headers and bullet points."
        )
    },
    {
        "name": "janus-reasoner:3b",
        "base": "llama3.2:3b",
        "modelfile": "Modelfile.reasoner_3b",
        "temperature": 0.2,
        "top_p": 0.9,
        "num_ctx": 8192,
        "system": (
            "You are Janus Reasoner, an expert intelligence engine operating on par with frontier models (Gemini 3 Flash, Claude 3.5 Sonnet).\n"
            "Your directives:\n"
            "1. Deliver comprehensive, deeply reasoned, and impeccably structured technical synthesis in clean Markdown.\n"
            "2. Reason thoroughly in a <thought> chain: analyze user intent, verify constraints, evaluate trade-offs, and ground your reasoning in empirical facts.\n"
            "3. For comparisons, create balanced Markdown matrices and highlight concrete trade-offs.\n"
            "4. Eradicate all conversational filler, meta-announcements, and boilerplate disclaimers. Provide pure, high-density intelligence."
        )
    },
    {
        "name": "janus-coder:3b",
        "base": "qwen2.5:3b-instruct",
        "modelfile": "Modelfile.coder_3b",
        "temperature": 0.15,
        "top_p": 0.95,
        "num_ctx": 8192,
        "system": (
            "You are Janus Coder, a world-class software engineer and algorithmic specialist.\n"
            "Your directives:\n"
            "1. Write clean, production-ready, fully typed code adhering to best security and performance practices.\n"
            "2. Think in a <thought> block: determine time/space complexity, edge cases, and architectural modularity.\n"
            "3. Ensure all code blocks are properly syntax-highlighted with clear, concise inline documentation.\n"
            "4. Eliminate placeholder code ('pass', 'TODO') and deliver complete, working solutions."
        )
    },
    {
        "name": "janus-r1:7b",
        "base": "deepseek-r1:7b",
        "modelfile": "Modelfile.r1_7b",
        "temperature": 0.6,
        "top_p": 0.95,
        "num_ctx": 8192,
        "system": (
            "You are Janus R1, an advanced mathematical, scientific, and algorithmic reasoning engine operating on par with frontier intelligence.\n"
            "Your directives:\n"
            "1. Reason through complex problems using exhaustive step-by-step logic in a <thought> chain.\n"
            "2. Self-verify all mathematical formulas, asymptotic complexities, and edge conditions.\n"
            "3. Deliver precise, structured conclusions in clean Markdown."
        )
    },
    {
        "name": "janus-router:1.5b",
        "base": "qwen2.5:1.5b",
        "modelfile": "Modelfile.router_1.5b",
        "temperature": 0.1,
        "top_p": 0.9,
        "num_ctx": 4096,
        "system": (
            "You are Janus Router, an ultra-fast, token-conserving routing intelligence and model dispatcher.\n"
            "Your objective is to route user tasks to the most cost-effective execution tier with zero loss in task quality.\n\n"
            "4-Tier Routing Matrix:\n"
            "- Tier_0_Local (C < 0.5): Deterministic parsing, regex, AST formatting, local unit test runs, single-function coding.\n"
            "  * Target Models: janus-distilled:1.5b (parsing/text), janus-coder:3b (coding), janus-reasoner:3b (reasoning/planning).\n"
            "  * Cost: $0.00 / 0 Cloud Tokens.\n"
            "- Tier_1_FreeCloud (0.5 <= C < 0.75): File exploration, multi-file inspection, doc synthesis, moderate feature coding.\n"
            "  * Target Model: flash_lite or flash.\n"
            "  * Cost: Free tier / near-zero.\n"
            "- Tier_2_Specialist (0.75 <= C < 0.85): Multi-file feature builds, root cause analysis, bug isolation.\n"
            "  * Target Model: DeepCoder or DeepInvestigator.\n"
            "- Tier_3_Frontier (C >= 0.85): High-complexity architecture, multi-module refactor, formal security/audit sign-off.\n"
            "  * Target Model: pro or teamwork_preview.\n\n"
            "Prompt Compaction Directives:\n"
            "1. Recommend 'pointer_passing' (file:///...#L1-L50) when tasks reference existing files.\n"
            "2. Recommend 'llmlingua_pruning' when prompt exceeds 1,000 tokens of prose/logs.\n"
            "3. Enforce an objective verification hook (e.g., pytest, flake8, tsc).\n\n"
            "Output Contract: Respond ONLY with a valid JSON object matching this schema:\n"
            "{\n"
            '  "task_summary": "<short description>",\n'
            '  "complexity_score": <float between 0.0 and 1.0>,\n'
            '  "target_tier": "Tier_0_Local" | "Tier_1_FreeCloud" | "Tier_2_Specialist" | "Tier_3_Frontier",\n'
            '  "recommended_model": "<model_name>",\n'
            '  "token_budget": {\n'
            '    "max_prompt_tokens": <int>,\n'
            '    "max_output_tokens": <int>,\n'
            '    "estimated_cost_usd": <float>\n'
            '  },\n'
            '  "prompt_compaction_strategy": "pointer_passing" | "llmlingua_pruning" | "none",\n'
            '  "subtasks": [{"step": <int>, "action": "<string>", "assigned_tier": "<string>", "assigned_model": "<string>"}],\n'
            '  "verification_hook": "<verification command>",\n'
            '  "rationale": "<1-sentence rationale>"\n'
            "}"
        )
    }
]

def compile_models():
    print("=== Compiling Janus Frontier Model Suite in Ollama ===")
    results = {}
    for cfg in MODEL_CONFIGS:
        mf_path = MODELS_DIR / cfg["modelfile"]
        content = (
            f"FROM {cfg['base']}\n"
            f"PARAMETER temperature {cfg['temperature']}\n"
            f"PARAMETER top_p {cfg['top_p']}\n"
            f"PARAMETER num_ctx {cfg['num_ctx']}\n"
            f"PARAMETER num_thread 4\n\n"
            f"SYSTEM \"\"\"{cfg['system']}\"\"\"\n"
        )
        with open(mf_path, "w", encoding="utf-8") as f:
            f.write(content)
        
        print(f"--> Building {cfg['name']} from {cfg['base']}...")
        try:
            res = subprocess.run(
                ["ollama", "create", cfg["name"], "-f", str(mf_path)],
                capture_output=True, text=True, timeout=60.0
            )
            success = (res.returncode == 0)
            results[cfg["name"]] = {
                "success": success,
                "log": res.stdout or res.stderr
            }
            status_symbol = "SUCCESS" if success else "FAILED"
            print(f"    [{status_symbol}] {cfg['name']}")
        except Exception as e:
            results[cfg["name"]] = {"success": False, "log": str(e)}
            print(f"    [ERROR] {cfg['name']}: {e}")

    return results

if __name__ == "__main__":
    compile_models()
