"""
Test fixtures and mock harness for Agentic Cityscape.
Provides deterministic mock clients for Ollama, Colibri, FreeLLMAPI, and Paid Frontier.
"""

import asyncio
import json
from typing import Any, Dict, Optional, Tuple


class MockOllamaClient:
    def __init__(self, should_fail: bool = False, confidence: float = 0.95) -> None:
        self.should_fail = should_fail
        self.confidence = confidence
        self.model = "mock-llama3.2:3b"

    async def generate(self, prompt: str, schema: Optional[Dict[str, Any]] = None) -> Tuple[str, Dict[str, Any], float, int, int]:
        if self.should_fail:
            raise ConnectionError("Mock Ollama daemon offline (port 11434)")
        data = {"status": "MOCK_OLLAMA_SUCCESS", "records_parsed": 120}
        return json.dumps(data), data, self.confidence, 40, 30


class MockColibriClient:
    def __init__(self, should_fail: bool = False, confidence: float = 0.98) -> None:
        self.should_fail = should_fail
        self.confidence = confidence
        self.model = "mock-colibri/glm-5.2-moe"

    async def generate(self, prompt: str, schema: Optional[Dict[str, Any]] = None) -> Tuple[str, Dict[str, Any], float, int, int]:
        if self.should_fail:
            raise TimeoutError("Mock Colibri server timeout (port 8080)")
        data = {"status": "MOCK_COLIBRI_SUCCESS", "var_99": 0.0418, "capital_pct": 26.0}
        return json.dumps(data), data, self.confidence, 65, 45


class MockFreeLLMAPIClient:
    def __init__(self, should_fail: bool = False, confidence: float = 0.92) -> None:
        self.should_fail = should_fail
        self.confidence = confidence
        self.model = "mock-freellmapi/llama-3.3-70b"

    async def generate(self, prompt: str, schema: Optional[Dict[str, Any]] = None) -> Tuple[str, Dict[str, Any], float, int, int]:
        if self.should_fail:
            raise RuntimeError("Mock FreeLLMAPI proxy rate limit (port 8000)")
        data = {"status": "MOCK_FREELLMAPI_SUCCESS", "heuristic_score": 0.94}
        return json.dumps(data), data, self.confidence, 50, 35


class MockPaidFrontierClient:
    def __init__(self, confidence: float = 0.999) -> None:
        self.confidence = confidence
        self.model = "mock-claude-3-5-sonnet"

    async def generate(self, prompt: str, schema: Optional[Dict[str, Any]] = None) -> Tuple[str, Dict[str, Any], float, int, int]:
        data = {"status": "MOCK_PAID_FRONTIER_SUCCESS", "audit_verdict": "APPROVED"}
        return json.dumps(data), data, self.confidence, 80, 50
