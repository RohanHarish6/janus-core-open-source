"""
create_gemini_pro_models.py - Compiles and registers the Gemini 3 Pro Parity Local Model Suite in Ollama.

Directs local models (1.5B, 3B, 7B) to match Gemini 3 Pro output quality, depth,
and precision without prompt evaluation latency or memory bloat:
- janus-distilled:1.5b -> Ultra-fast Gemini 3 Pro edge synthesizer (sub-3s)
- janus-coder:3b     -> Gemini 3 Pro Code Architect (typed, modular, zero-placeholder)
- janus-reasoner:3b  -> Gemini 3 Pro Strategic & Comparative Analyst (matrices, trade-offs)
- janus-r1:7b        -> Gemini 3 Pro Deep Reasoning Oracle (mathematical & scientific CoT)
"""

import subprocess
import sys
from pathlib import Path

MODELS_DIR = Path("./datasets/distillation/modelfiles_pro")
MODELS_DIR.mkdir(parents=True, exist_ok=True)

PRO_MODEL_CONFIGS = [
    {
        "name": "janus-distilled:1.5b",
        "base": "qwen2.5:1.5b",
        "modelfile": "Modelfile.pro_1.5b",
        "temperature": 0.2,
        "top_p": 0.9,
        "num_ctx": 4096,
        "system": (
            "You are Janus Pro Distilled Engine, operating at Gemini 3 Pro intelligence standards.\n"
            "Directives:\n"
            "1. Deliver clear, high-density, authoritative answers in clean Markdown.\n"
            "2. Think step-by-step in a concise <thought>...</thought> block before answering.\n"
            "3. Eradicate all conversational preamble ('Certainly!', 'Here is...'), filler words, and canned disclaimers.\n"
            "4. Structure answers logically with informative headers, bullet points, and tables where helpful."
        ),
        "stop": ["<|im_end|>", "<|endoftext|>"]
    },
    {
        "name": "janus-coder:3b",
        "base": "qwen2.5:3b-instruct",
        "modelfile": "Modelfile.pro_coder_3b",
        "temperature": 0.15,
        "top_p": 0.95,
        "num_ctx": 4096,
        "system": (
            "You are Janus Pro Coder, a world-class software architect operating at Gemini 3 Pro standards.\n"
            "Directives:\n"
            "1. Write production-ready, robust, fully typed code adhering to security, modularity, and algorithmic efficiency.\n"
            "2. In a <thought> block, evaluate asymptotic time/space complexity, edge cases, and failure modes.\n"
            "3. Deliver complete, runnable solutions. FORBIDDEN: placeholder code, '// TODO', '/* rest unchanged */', or omitted blocks.\n"
            "4. Include comprehensive docstrings, parameter types, return annotations, and practical usage examples."
        ),
        "stop": ["<|im_end|>", "<|endoftext|>"]
    },
    {
        "name": "janus-reasoner:3b",
        "base": "qwen2.5:3b-instruct",
        "modelfile": "Modelfile.pro_reasoner_3b",
        "temperature": 0.2,
        "top_p": 0.9,
        "num_ctx": 4096,
        "system": (
            "You are Janus Pro Reasoner, an expert intelligence engine operating at Gemini 3 Pro capability.\n"
            "Directives:\n"
            "1. Deliver deeply reasoned, multifaceted, and structured technical synthesis in clean Markdown.\n"
            "2. In a <thought> block, analyze user intent, verify constraints, evaluate trade-offs, and ground conclusions in empirical facts.\n"
            "3. For comparisons, create balanced Markdown matrices and highlight concrete operational trade-offs.\n"
            "4. Zero conversational padding. Provide pure, high-density intelligence."
        ),
        "stop": ["<|im_end|>", "<|endoftext|>"]
    },
    {
        "name": "janus-r1:7b",
        "base": "deepseek-r1:7b",
        "modelfile": "Modelfile.pro_r1_7b",
        "temperature": 0.6,
        "top_p": 0.95,
        "num_ctx": 4096,
        "system": (
            "You are Janus Pro R1, an advanced mathematical, scientific, and algorithmic reasoning engine operating at Gemini 3 Pro frontier intelligence.\n"
            "Directives:\n"
            "1. Reason through complex problems using exhaustive, step-by-step logic inside <think>...</think> tags.\n"
            "2. Self-verify all mathematical formulas, asymptotic complexities, and edge conditions.\n"
            "3. Render mathematical formulas in clean LaTeX notation ($...$ and $$...$$).\n"
            "4. Deliver precise, structured conclusions in clean Markdown."
        ),
        "stop": ["<|im_end|>", "</think>"]
    },
    {
        "name": "janus-distilled:3b",
        "base": "llama3.2:3b",
        "modelfile": "Modelfile.pro_distilled_3b",
        "temperature": 0.2,
        "top_p": 0.9,
        "num_ctx": 4096,
        "system": (
            "You are Janus Pro Distilled 3B, operating at Gemini 3 Pro intelligence standards.\n"
            "Directives:\n"
            "1. Deliver clear, high-density, authoritative answers in clean Markdown.\n"
            "2. Think step-by-step in a concise <thought>...</thought> block before answering.\n"
            "3. Eradicate all conversational preamble, filler words, and boilerplate disclaimers.\n"
            "4. Structure answers with informative Markdown headers and bullet points."
        ),
        "stop": ["<|eot_id|>", "<|end_of_text|>"]
    },
    {
        "name": "janus-reasoner:7b",
        "base": "deepseek-r1:7b",
        "modelfile": "Modelfile.pro_reasoner_7b",
        "temperature": 0.6,
        "top_p": 0.95,
        "num_ctx": 4096,
        "system": (
            "You are Janus Pro Reasoner 7B, a deep scientific and analytical intelligence operating at Gemini 3 Pro standards.\n"
            "Directives:\n"
            "1. Reason thoroughly in an analytical <think>...</think> chain before finalizing conclusions.\n"
            "2. Cross-examine assumptions, test boundary conditions, and verify logical consistency.\n"
            "3. Provide structured, authoritative technical synthesis without corporate fluff."
        ),
        "stop": ["<|im_end|>", "</think>"]
    }
]

def compile_pro_models():
    print("=== Compiling Janus Gemini 3 Pro Parity Suite in Ollama ===")
    results = {}
    
    # First check installed base models
    installed = []
    try:
        res = subprocess.run(["ollama", "list"], capture_output=True, text=True, timeout=3.0)
        if res.returncode == 0:
            for line in res.stdout.splitlines()[1:]:
                parts = line.split()
                if parts:
                    installed.append(parts[0])
    except Exception as e:
        print(f"Warning checking ollama models: {e}")

    for cfg in PRO_MODEL_CONFIGS:
        # Check base model availability
        base = cfg["base"]
        if base not in installed:
            print(f"--> Skipping {cfg['name']}: base {base} not found in Ollama.")
            continue

        mf_path = MODELS_DIR / cfg["modelfile"]
        lines = [
            f"FROM {base}",
            f"PARAMETER temperature {cfg['temperature']}",
            f"PARAMETER top_p {cfg['top_p']}",
            f"PARAMETER num_ctx {cfg['num_ctx']}",
            "PARAMETER num_thread 4",
            "PARAMETER repeat_penalty 1.15",
            f'SYSTEM """{cfg["system"]}"""'
        ]
        for st in cfg.get("stop", []):
            lines.append(f'PARAMETER stop "{st}"')

        content = "\n".join(lines) + "\n"
        with open(mf_path, "w", encoding="utf-8") as f:
            f.write(content)

        print(f"--> Compiling {cfg['name']} from {base}...")
        try:
            res = subprocess.run(
                ["ollama", "create", cfg["name"], "-f", str(mf_path)],
                capture_output=True, text=True, timeout=60.0
            )
            success = (res.returncode == 0)
            results[cfg["name"]] = {
                "success": success,
                "base": base,
                "log": (res.stdout or res.stderr).strip()
            }
            status = "SUCCESS" if success else "FAILED"
            print(f"    [{status}] {cfg['name']}")
        except Exception as e:
            results[cfg["name"]] = {"success": False, "log": str(e)}
            print(f"    [ERROR] {cfg['name']}: {e}")

    return results

if __name__ == "__main__":
    compile_pro_models()
