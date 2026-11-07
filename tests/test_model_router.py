"""
test_model_router.py - Unit test suite for Janus Core TokenConservingModelRouter and janus-router:1.5b.
Validates 4-tier complexity routing, token conservation calculations, prompt compaction planning,
ACRO-V specification generation, and REST API endpoint handlers.
"""

import unittest
import json
import io
from model_router import TokenConservingModelRouter, GLOBAL_TOKEN_ROUTER, ROUTER_MODEL_NAME


class TestTokenConservingModelRouter(unittest.TestCase):
    def setUp(self):
        self.router = TokenConservingModelRouter()

    def test_router_model_name_and_init(self):
        self.assertEqual(self.router.model_name, "janus-router:1.5b")
        self.assertEqual(ROUTER_MODEL_NAME, "janus-router:1.5b")
        self.assertIsNotNone(self.router.ollama_url)

    def test_heuristic_route_tier0_parsing(self):
        prompt = "Parse regex from log file and extract IP addresses"
        res = self.router.heuristic_route(prompt)
        self.assertIn("target_tier", res)
        self.assertEqual(res["target_tier"], "Tier_0_Local")
        self.assertIn(res["recommended_model"], ["janus-distilled:1.5b", "janus-coder:3b"])
        self.assertLessEqual(res["complexity_score"], 0.50)
        self.assertEqual(res["token_budget"]["estimated_cost_usd"], 0.00)

    def test_heuristic_route_tier0_coding(self):
        prompt = "Write a Python function with memoization for Fibonacci numbers"
        res = self.router.heuristic_route(prompt)
        self.assertEqual(res["target_tier"], "Tier_0_Local")
        self.assertEqual(res["recommended_model"], "janus-coder:3b")
        self.assertLess(res["complexity_score"], 0.50)
        self.assertEqual(res["token_budget"]["estimated_cost_usd"], 0.00)

    def test_heuristic_route_tier1_exploration(self):
        prompt = "Search across all files for deprecated APIs, synthesize results, and evaluate differences"
        res = self.router.heuristic_route(prompt, files=["api1.py", "api2.py", "api3.py", "api4.py"])
        self.assertIn(res["target_tier"], ["Tier_1_FreeCloud", "Tier_2_Specialist"])
        self.assertGreaterEqual(res["complexity_score"], 0.50)

    def test_heuristic_route_tier2_specialist(self):
        prompt = "Isolate bug and fix race condition across 5 files in async queue"
        res = self.router.heuristic_route(prompt, files=["q1.py", "q2.py", "q3.py", "q4.py", "q5.py"])
        self.assertIn(res["target_tier"], ["Tier_2_Specialist", "Tier_3_Frontier"])
        self.assertGreaterEqual(res["complexity_score"], 0.70)

    def test_heuristic_route_tier3_frontier(self):
        prompt = "Design distributed consensus architecture, verify formal safety proofs, and generate cryptographic audit sign-off"
        res = self.router.heuristic_route(prompt)
        self.assertEqual(res["target_tier"], "Tier_3_Frontier")
        self.assertEqual(res["recommended_model"], "pro")
        self.assertGreaterEqual(res["complexity_score"], 0.85)

    def test_compaction_strategy_pointer_passing(self):
        prompt = "Check implementation in file:///C:/project/app.py#L1-L100"
        res = self.router.heuristic_route(prompt)
        self.assertEqual(res["prompt_compaction_strategy"], "pointer_passing")

    def test_compaction_strategy_pruning_on_large_prompt(self):
        large_prompt = "Analyze the following log trace: " + ("Error at line 42: Timeout. " * 150)
        res = self.router.heuristic_route(large_prompt)
        self.assertEqual(res["prompt_compaction_strategy"], "llmlingua_pruning")

    def test_token_savings_calculation_zero_cost(self):
        route = {
            "target_tier": "Tier_0_Local",
            "recommended_model": "janus-coder:3b",
            "token_budget": {"max_prompt_tokens": 512, "max_output_tokens": 512, "estimated_cost_usd": 0.00}
        }
        savings = self.router.calculate_token_savings(route, prompt_char_len=800)
        self.assertTrue(savings["is_zero_cost"])
        self.assertEqual(savings["actual_cloud_tokens"], 0)
        self.assertGreater(savings["cloud_tokens_saved"], 1000)
        self.assertEqual(savings["cloud_tokens_saved_pct"], 100.0)

    def test_token_savings_calculation_frontier(self):
        route = {
            "target_tier": "Tier_3_Frontier",
            "recommended_model": "pro",
            "token_budget": {"max_prompt_tokens": 2000, "max_output_tokens": 1500, "estimated_cost_usd": 0.04}
        }
        savings = self.router.calculate_token_savings(route, prompt_char_len=2000)
        self.assertFalse(savings["is_zero_cost"])
        self.assertEqual(savings["estimated_cost_usd"], 0.04)

    def test_format_acro_v_specification(self):
        route = {
            "task_summary": "Implement binary search",
            "target_tier": "Tier_0_Local",
            "recommended_model": "janus-coder:3b",
            "token_budget": {"max_prompt_tokens": 512, "max_output_tokens": 512},
            "prompt_compaction_strategy": "pointer_passing",
            "verification_hook": "pytest -q tests/test_search.py"
        }
        raw_prompt = "Write a binary search function in Python"
        acro_v = self.router.format_acro_v_specification(route, raw_prompt)

        self.assertIn("<role>", acro_v)
        self.assertIn("Tier_0_Local (janus-coder:3b)", acro_v)
        self.assertIn("<context>", acro_v)
        self.assertIn("<objective>", acro_v)
        self.assertIn("<operational_protocol>", acro_v)
        self.assertIn("<constraints>", acro_v)
        self.assertIn("<verification_hook>", acro_v)
        self.assertIn("pytest -q tests/test_search.py", acro_v)
        self.assertIn("<task_prompt>", acro_v)

    def test_route_task_caching(self):
        prompt = "Deterministic test prompt for cache validation"
        d1 = self.router.route_task(prompt)
        d2 = self.router.route_task(prompt)
        self.assertEqual(d1, d2)
        cache_key = f"{prompt}::0"
        self.assertIn(cache_key, self.router._cache)

    def test_desktop_app_router_endpoints(self):
        from desktop_app import CityscapeRequestHandler
        import http.server

        # Test router evaluate endpoint handler mock
        class MockRequest:
            def makefile(self, *args, **kwargs):
                return io.BytesIO(b"")
            def getsockname(self):
                return ("127.0.0.1", 8765)

        class MockServer:
            hardware_config = None
            workbench_history = []
            session_artifacts = []

        handler = CityscapeRequestHandler.__new__(CityscapeRequestHandler)
        handler.headers = {"Content-Length": "88", "Origin": "http://127.0.0.1:8765"}
        handler.client_address = ("127.0.0.1", 54321)
        handler.server = MockServer()
        handler.wfile = io.BytesIO()
        handler.rfile = io.BytesIO(json.dumps({"prompt": "Write a unit test for router"}).encode("utf-8"))

        handler._set_headers = lambda mime="application/json", status_code=200: None
        handler._handle_router_evaluate()

        output_bytes = handler.wfile.getvalue()
        self.assertTrue(len(output_bytes) > 0)
        parsed = json.loads(output_bytes.decode("utf-8"))
        self.assertEqual(parsed["status"], "SUCCESS")
        self.assertIn("route", parsed)
        self.assertIn("token_savings", parsed)
        self.assertIn("acro_v_specification", parsed)


if __name__ == "__main__":
    unittest.main()
