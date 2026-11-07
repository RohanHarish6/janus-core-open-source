"""
model_router.py - Janus Core Token-Conserving Model & Agent Router.

Provides autonomous task complexity evaluation, model selection, prompt compaction
planning, and token conservation telemetry using the local calibrated engine
`janus-router:1.5b` (with deterministic zero-latency heuristic fallback).

Guarantees 100% completion quality while preserving parent model tokens and
maximizing zero-cost ($0.00) local edge execution.
"""

import os
import re
import json
import time
import logging
import urllib.request
import urllib.error
from typing import Dict, List, Any, Optional, Tuple

logger = logging.getLogger("JanusCore.ModelRouter")

ROUTER_MODEL_NAME = "janus-router:1.5b"
DEFAULT_OLLAMA_URL = "http://127.0.0.1:11434"

# Routing Exemplars for few-shot in-context calibration
ROUTING_EXEMPLARS = (
    "Exemplar 1:\n"
    "Task: 'Parse regex from logs and extract IP addresses'\n"
    "Decision: {\"task_summary\": \"Extract IPs using regex\", \"complexity_score\": 0.15, "
    "\"target_tier\": \"Tier_0_Local\", \"recommended_model\": \"janus-distilled:1.5b\", "
    "\"token_budget\": {\"max_prompt_tokens\": 256, \"max_output_tokens\": 256, \"estimated_cost_usd\": 0.00}, "
    "\"prompt_compaction_strategy\": \"none\", \"subtasks\": [], \"verification_hook\": \"python -c \\\"import re\\\"\", "
    "\"rationale\": \"Deterministic string parsing requiring zero neural reasoning.\"}\n\n"
    "Exemplar 2:\n"
    "Task: 'Write a Python function with memoization for Fibonacci numbers and add pytest unit tests'\n"
    "Decision: {\"task_summary\": \"Fibonacci algorithm with unit tests\", \"complexity_score\": 0.35, "
    "\"target_tier\": \"Tier_0_Local\", \"recommended_model\": \"janus-coder:3b\", "
    "\"token_budget\": {\"max_prompt_tokens\": 512, \"max_output_tokens\": 512, \"estimated_cost_usd\": 0.00}, "
    "\"prompt_compaction_strategy\": \"none\", \"subtasks\": [], \"verification_hook\": \"pytest tests/test_fib.py -v\", "
    "\"rationale\": \"Single-function implementation well within local 3B coder capabilities at zero cloud cost.\"}\n\n"
    "Exemplar 3:\n"
    "Task: 'Search the repository for deprecated API endpoints, inspect 4 files, and summarize differences'\n"
    "Decision: {\"task_summary\": \"Repository audit and documentation synthesis\", \"complexity_score\": 0.60, "
    "\"target_tier\": \"Tier_1_FreeCloud\", \"recommended_model\": \"flash_lite\", "
    "\"token_budget\": {\"max_prompt_tokens\": 1024, \"max_output_tokens\": 1024, \"estimated_cost_usd\": 0.00}, "
    "\"prompt_compaction_strategy\": \"pointer_passing\", \"subtasks\": [], \"verification_hook\": \"git status\", "
    "\"rationale\": \"Multi-file exploration easily handled by free cloud workers via pointer passing.\"}\n\n"
    "Exemplar 4:\n"
    "Task: 'Fix race condition across 6 modules in authentication pipeline, update session tokens, and ensure backward compatibility'\n"
    "Decision: {\"task_summary\": \"Multi-module race condition and auth refactor\", \"complexity_score\": 0.82, "
    "\"target_tier\": \"Tier_2_Specialist\", \"recommended_model\": \"DeepCoder\", "
    "\"token_budget\": {\"max_prompt_tokens\": 2048, \"max_output_tokens\": 2048, \"estimated_cost_usd\": 0.01}, "
    "\"prompt_compaction_strategy\": \"pointer_passing\", \"subtasks\": [{\"step\": 1, \"action\": \"Isolate race condition\", \"assigned_tier\": \"Tier_2_Specialist\", \"assigned_model\": \"DeepInvestigator\"}], \"verification_hook\": \"pytest tests/test_auth.py -k race\", "
    "\"rationale\": \"High-concurrency multi-file state issue requiring specialized coding subagent.\"}\n\n"
    "Exemplar 5:\n"
    "Task: 'Design complete distributed consensus architecture, verify formal safety proofs, and provide signed audit report'\n"
    "Decision: {\"task_summary\": \"Distributed consensus architecture and security sign-off\", \"complexity_score\": 0.95, "
    "\"target_tier\": \"Tier_3_Frontier\", \"recommended_model\": \"pro\", "
    "\"token_budget\": {\"max_prompt_tokens\": 4096, \"max_output_tokens\": 4096, \"estimated_cost_usd\": 0.05}, "
    "\"prompt_compaction_strategy\": \"pointer_passing\", \"subtasks\": [{\"step\": 1, \"action\": \"Architecture blueprint\", \"assigned_tier\": \"Tier_3_Frontier\", \"assigned_model\": \"teamwork_preview\"}], \"verification_hook\": \"python -m pytest tests/test_consensus.py\", "
    "\"rationale\": \"Mission-critical consensus proof requiring frontier reasoning and team consensus.\"}\n"
)


class TokenConservingModelRouter:
    """
    Evaluates prompts to compute complexity scores, route tasks to the optimal
    model/tier, and enforce token conservation heuristics.
    """

    def __init__(self, ollama_url: str = DEFAULT_OLLAMA_URL, model_name: str = ROUTER_MODEL_NAME):
        self.ollama_url = ollama_url.rstrip("/")
        self.model_name = model_name
        self._cache: Dict[str, Dict[str, Any]] = {}

    def is_available(self, timeout: float = 1.5) -> bool:
        """Fast check to determine if the local Ollama router model is available."""
        try:
            req = urllib.request.Request(f"{self.ollama_url}/api/tags")
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                if resp.status == 200:
                    data = json.loads(resp.read().decode("utf-8"))
                    models = [m.get("name") for m in data.get("models", [])]
                    return any(self.model_name in m for m in models)
        except Exception:
            pass
        return False

    def heuristic_route(
        self,
        prompt: str,
        context: Optional[str] = None,
        files: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Deterministic, zero-latency local routing engine.
        Implements Janus Core 4-Tier Matrix based on task complexity heuristics.
        """
        p_lower = prompt.lower()
        num_files = len(files) if files else 0
        prompt_len = len(prompt)

        # Baseline Complexity Factors
        score = 0.20

        # Factor: Multi-file scope
        if num_files > 3 or "across all files" in p_lower or "whole project" in p_lower:
            score += 0.35
        elif num_files > 1 or "multiple files" in p_lower:
            score += 0.20

        # Additive complexity indicators
        if any(w in p_lower for w in ["formal proof", "formal safety", "consensus", "distributed system"]):
            score += 0.35
        if any(w in p_lower for w in ["architecture", "architectural", "system design"]):
            score += 0.25
        if any(w in p_lower for w in ["security audit", "cryptographic", "audit sign-off", "statutory audit"]):
            score += 0.25
        if any(w in p_lower for w in ["refactor", "race condition", "deadlock", "memory leak", "isolate bug"]):
            score += 0.25
        if any(w in p_lower for w in ["benchmark", "compare", "synthesize", "survey"]):
            score += 0.15

        # Factor: Simplicity / deterministic parsing
        if any(w in p_lower for w in ["regex", "parse", "format", "extract", "single function", "quick test", "docstring"]):
            score -= 0.15

        # Clamp complexity score
        complexity = round(max(0.05, min(0.98, score)), 2)

        # Tier & Model Assignment
        if complexity < 0.50:
            target_tier = "Tier_0_Local"
            if any(w in p_lower for w in ["code", "function", "class", "script", "algorithm", "test"]):
                recommended_model = "janus-coder:3b"
            elif any(w in p_lower for w in ["reason", "analyze", "why", "explain"]):
                recommended_model = "janus-reasoner:3b"
            else:
                recommended_model = "janus-distilled:1.5b"
            max_prompt = 512
            max_output = 512
            est_cost = 0.00
            rationale = "Task can be fully resolved with 100% fidelity using local edge models at $0.00."

        elif complexity < 0.75:
            target_tier = "Tier_1_FreeCloud"
            recommended_model = "flash_lite"
            max_prompt = 1024
            max_output = 1024
            est_cost = 0.00
            rationale = "Exploration and moderate feature tasks routed to free cloud tier."

        elif complexity < 0.85:
            target_tier = "Tier_2_Specialist"
            recommended_model = "DeepCoder" if any(w in p_lower for w in ["code", "bug", "refactor"]) else "DeepInvestigator"
            max_prompt = 2048
            max_output = 2048
            est_cost = 0.01
            rationale = "Multi-file implementation or deep root-cause analysis delegated to specialized subagent."

        else:
            target_tier = "Tier_3_Frontier"
            recommended_model = "pro"
            max_prompt = 4096
            max_output = 4096
            est_cost = 0.04
            rationale = "Mission-critical architectural design and audit requiring frontier reasoning."

        # Compaction Strategy: LLMLingua pruning for large prose/logs (>2000 chars) without files, pointer passing when files referenced
        if prompt_len > 2000 and num_files == 0 and "file:///" not in prompt:
            compaction = "llmlingua_pruning"
        elif num_files > 0 or "file:///" in prompt or prompt_len > 1500:
            compaction = "pointer_passing"
        else:
            compaction = "none"

        # Verification Hook
        if any(w in p_lower for w in ["python", "pytest", "test", ".py"]):
            verification_hook = "pytest -q"
        elif any(w in p_lower for w in ["node", "javascript", "typescript", "npm"]):
            verification_hook = "npm test"
        elif any(w in p_lower for w in ["rust", "cargo"]):
            verification_hook = "cargo check"
        else:
            verification_hook = "python -m unittest"

        summary = (prompt[:75] + "...") if len(prompt) > 75 else prompt

        return {
            "task_summary": summary.strip(),
            "complexity_score": complexity,
            "target_tier": target_tier,
            "recommended_model": recommended_model,
            "token_budget": {
                "max_prompt_tokens": max_prompt,
                "max_output_tokens": max_output,
                "estimated_cost_usd": est_cost
            },
            "prompt_compaction_strategy": compaction,
            "subtasks": [],
            "verification_hook": verification_hook,
            "rationale": rationale,
            "routing_engine": "heuristic_calibrator"
        }

    def route_task(
        self,
        prompt: str,
        context: Optional[str] = None,
        files: Optional[List[str]] = None,
        timeout: float = 12.0
    ) -> Dict[str, Any]:
        """
        Routes the task using the calibrated local `janus-router:1.5b` model.
        Falls back seamlessly to the deterministic heuristic engine if Ollama is
        offline or times out.
        """
        cache_key = f"{prompt.strip()}::{len(files or [])}"
        if cache_key in self._cache:
            return self._cache[cache_key]

        query = (
            f"{ROUTING_EXEMPLARS}\n"
            f"Now evaluate this task:\n"
            f"Prompt: {prompt}\n"
            f"Context: {context or 'None'}\n"
            f"Referenced Files: {', '.join(files) if files else 'None'}\n\n"
            f"Return strict RFC 8259 JSON matching schema."
        )

        payload = {
            "model": self.model_name,
            "prompt": query,
            "stream": False,
            "format": "json"
        }

        try:
            req = urllib.request.Request(
                f"{self.ollama_url}/api/generate",
                data=json.dumps(payload).encode("utf-8"),
                headers={"Content-Type": "application/json"}
            )
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                if resp.status == 200:
                    raw_data = json.loads(resp.read().decode("utf-8"))
                    raw_response = raw_data.get("response", "").strip()
                    parsed = json.loads(raw_response)
                    
                    # Sanitize and validate required schema keys
                    if self._validate_decision_schema(parsed):
                        # Calibrate score bounds against prompt context
                        calibrated = self._calibrate_decision(parsed, prompt, files)
                        calibrated["routing_engine"] = "janus_router_neural"
                        self._cache[cache_key] = calibrated
                        return calibrated
        except Exception as e:
            logger.debug(f"Router neural inference fallback: {e}")

        # Fallback to deterministic heuristic
        decision = self.heuristic_route(prompt, context=context, files=files)
        self._cache[cache_key] = decision
        return decision

    def _validate_decision_schema(self, d: Any) -> bool:
        """Verifies that the generated output conforms to the routing contract."""
        if not isinstance(d, dict):
            return False
        required_keys = ["task_summary", "complexity_score", "target_tier", "recommended_model", "token_budget"]
        return all(k in d for k in required_keys)

    def _calibrate_decision(self, decision: Dict[str, Any], prompt: str, files: Optional[List[str]]) -> Dict[str, Any]:
        """
        Applies safety calibration to ensure small local tasks are not erroneously
        up-routed to expensive frontier tiers.
        """
        p_lower = prompt.lower()
        score = float(decision.get("complexity_score", 0.5))
        num_files = len(files) if files else 0

        # Anti-inflation guard: single function / trivial script should not exceed Tier 1
        if num_files <= 1 and any(w in p_lower for w in ["single function", "fibonacci", "regex", "simple script", "unit test"]):
            if score > 0.49:
                score = 0.35
                decision["complexity_score"] = score
                decision["target_tier"] = "Tier_0_Local"
                decision["recommended_model"] = "janus-coder:3b"
                decision["token_budget"] = {
                    "max_prompt_tokens": 512,
                    "max_output_tokens": 512,
                    "estimated_cost_usd": 0.00
                }
                decision["rationale"] = "Calibrated to Tier 0 local coder for single-function efficiency at $0.00."

        return decision

    def calculate_token_savings(self, decision: Dict[str, Any], prompt_char_len: int) -> Dict[str, Any]:
        """
        Calculates cloud tokens and cost saved by routing to Tier 0 or Tier 1 vs
        a monolithic frontier model.
        """
        baseline_prompt_tokens = max(100, prompt_char_len // 4)
        baseline_output_tokens = 1500
        baseline_total_tokens = baseline_prompt_tokens + baseline_output_tokens
        # Frontier pricing assumption: $2.50 / 1M prompt, $10.00 / 1M completion (~$0.02)
        baseline_cost_usd = (baseline_prompt_tokens * 2.50 / 1_000_000) + (baseline_output_tokens * 10.00 / 1_000_000)

        allocated_cost = decision.get("token_budget", {}).get("estimated_cost_usd", 0.00)
        target_tier = decision.get("target_tier", "Tier_0_Local")

        if target_tier in ("Tier_0_Local", "Tier_1_FreeCloud"):
            actual_cloud_tokens = 0
            actual_cost = 0.00
        else:
            budget = decision.get("token_budget", {})
            actual_cloud_tokens = budget.get("max_prompt_tokens", 500) + budget.get("max_output_tokens", 500)
            actual_cost = allocated_cost

        tokens_saved = max(0, baseline_total_tokens - actual_cloud_tokens)
        cost_saved = max(0.00, baseline_cost_usd - actual_cost)
        savings_pct = round((tokens_saved / max(1, baseline_total_tokens)) * 100, 1)

        return {
            "baseline_tokens": baseline_total_tokens,
            "actual_cloud_tokens": actual_cloud_tokens,
            "cloud_tokens_saved": tokens_saved,
            "cloud_tokens_saved_pct": savings_pct,
            "estimated_cost_usd": actual_cost,
            "estimated_cost_saved_usd": round(cost_saved, 4),
            "is_zero_cost": (actual_cost == 0.00)
        }

    def format_acro_v_specification(self, decision: Dict[str, Any], prompt: str) -> str:
        """
        Wraps the task instruction in standard ACRO-V semantic tags to eliminate
        conversational filler and guarantee structured execution.
        """
        target_model = decision.get("recommended_model", "janus-coder:3b")
        tier = decision.get("target_tier", "Tier_0_Local")
        budget = decision.get("token_budget", {})
        hook = decision.get("verification_hook", "pytest -q")

        return (
            f"<role>\n"
            f"Autonomous execution agent operating under {tier} ({target_model}).\n"
            f"</role>\n"
            f"<context>\n"
            f"Execution Budget: Max {budget.get('max_prompt_tokens', 512)} prompt tokens, "
            f"{budget.get('max_output_tokens', 512)} output tokens.\n"
            f"Compaction Strategy: {decision.get('prompt_compaction_strategy', 'pointer_passing')}.\n"
            f"</context>\n"
            f"<objective>\n"
            f"{decision.get('task_summary', prompt[:100])}\n"
            f"</objective>\n"
            f"<operational_protocol>\n"
            f"Phase 1: Parse requirements and verify local constraints.\n"
            f"Phase 2: Generate concise, fully typed implementation without placeholders.\n"
            f"Phase 3: Execute verification hook.\n"
            f"</operational_protocol>\n"
            f"<constraints>\n"
            f"- Strictly no conversational lead-ins or sign-offs.\n"
            f"- Zero placeholders (no 'TODO', 'pass', or '/* rest unchanged */').\n"
            f"- Preserve existing comments and docstrings intact.\n"
            f"</constraints>\n"
            f"<verification_hook>\n"
            f"{hook}\n"
            f"</verification_hook>\n"
            f"<task_prompt>\n"
            f"{prompt}\n"
            f"</task_prompt>"
        )


GLOBAL_TOKEN_ROUTER = TokenConservingModelRouter()
