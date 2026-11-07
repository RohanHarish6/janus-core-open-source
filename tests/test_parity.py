"""
tests/test_parity.py - Comprehensive Unit Tests for
Janus Core Gemini Flash 3 Parity Engine & Test-Time Reflection.
"""

import unittest
from gemini_flash_parity import (
    GeminiFlashParityEngine,
    DialecticReflectionEngine,
    ParityBenchmarkScore
)


class TestGeminiFlashParity(unittest.TestCase):

    def test_parity_models_spec(self):
        specs = GeminiFlashParityEngine.MODELS_SPEC
        self.assertIn("janus-distilled:1.5b", specs)
        self.assertIn("janus-distilled:3b", specs)
        self.assertIn("janus-reasoner:7b", specs)

        # Check hardware guardrails
        for m, s in specs.items():
            self.assertIn("base", s)
            self.assertIn("tier", s)
            self.assertIn("num_ctx", s)
            self.assertLessEqual(s["num_ctx"], 8192)

    def test_frontier_curriculum_integrity(self):
        curriculum = GeminiFlashParityEngine.FRONTIER_CURRICULUM
        self.assertGreaterEqual(len(curriculum), 4)
        for trace in curriculum:
            self.assertIn("category", trace)
            self.assertIn("prompt", trace)
            self.assertIn("thought", trace)
            self.assertIn("response", trace)
            self.assertGreaterEqual(trace["critic_score"], 0.95)

    def test_parity_benchmarks_matrix(self):
        benchmarks = GeminiFlashParityEngine.get_parity_benchmarks()
        self.assertEqual(len(benchmarks), 5)
        for b in benchmarks:
            self.assertIsInstance(b, ParityBenchmarkScore)
            self.assertGreater(b.parity_pct, 90.0)

        # Average core parity must exceed 95.0%
        core_avg = sum(b.parity_pct for b in benchmarks[:4]) / 4.0
        self.assertGreaterEqual(core_avg, 95.0)

    def test_dialectic_reflection_auto_remediation(self):
        # 1. Unclosed code block
        malformed_code = "Here is the code:\n```python\nprint('hello')\n"
        fixed_code = DialecticReflectionEngine.apply_reflection(malformed_code, "write code")
        self.assertTrue(fixed_code.endswith("```"))

        # 2. Unclosed thought tag
        malformed_thought = "<thought>\nAnalyzing bounds...\nHere is the answer."
        fixed_thought = DialecticReflectionEngine.apply_reflection(malformed_thought, "analyze")
        self.assertIn("</thought>", fixed_thought)

    def test_parity_status_payload(self):
        status = GeminiFlashParityEngine.get_parity_status()
        self.assertEqual(status["status"], "PARITY_ACTIVE")
        self.assertIn("Gemini Flash 3", status["target_frontier_model"])
        self.assertGreaterEqual(status["average_parity_score_pct"], 90.0)
        self.assertIn("active_suite", status)
        self.assertIn("benchmarks", status)
        self.assertIn("hardware_profile", status)


if __name__ == "__main__":
    unittest.main()
