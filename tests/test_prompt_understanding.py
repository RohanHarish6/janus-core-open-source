"""
tests/test_prompt_understanding.py - Comprehensive Unit Tests for
Janus Core Prompt Understanding Engine & Distillation Training Manager.
"""

import unittest
from prompt_understanding import (
    PromptUnderstandingEngine,
    UserIntent,
    GleanedInformation,
    DistillationTrainingManager,
    AutoSessionDistillationManager
)


class TestPromptUnderstanding(unittest.TestCase):

    def test_intent_classification(self):
        cases = [
            ("find info on smartphones", UserIntent.FACTUAL_LOOKUP),
            ("search for quantum computing breakthroughs", UserIntent.FACTUAL_LOOKUP),
            ("compare electric and hybrid vehicles", UserIntent.COMPARATIVE_ANALYSIS),
            ("PostgreSQL vs MongoDB for high write loads", UserIntent.COMPARATIVE_ANALYSIS),
            ("explain how photosynthesis works", UserIntent.CONCEPT_EXPLANATION),
            ("what is a transformer neural network", UserIntent.CONCEPT_EXPLANATION),
            ("how to build a docker container", UserIntent.TUTORIAL_HOWTO),
            ("guide to setting up git hooks", UserIntent.TUTORIAL_HOWTO),
            ("write a python script to parse json safely", UserIntent.CODE_IMPLEMENTATION),
            ("implement binary search algorithm", UserIntent.CODE_IMPLEMENTATION),
        ]
        for prompt, expected_intent in cases:
            intent = PromptUnderstandingEngine.classify_intent(prompt)
            self.assertEqual(intent, expected_intent, f"Failed on prompt: {prompt}")

    def test_comparative_entity_extraction(self):
        prompt = "compare electric cars and hybrid vehicles"
        decomp = PromptUnderstandingEngine.extract_entities_and_subqueries(prompt, UserIntent.COMPARATIVE_ANALYSIS)
        self.assertEqual(len(decomp["entities"]), 2)
        self.assertIn("electric cars", decomp["entities"])
        self.assertIn("hybrid vehicles", decomp["entities"])
        self.assertIn("vs", decomp["clean_topic"])

    def test_code_entity_extraction(self):
        prompt = "write a python function to parse json safely"
        decomp = PromptUnderstandingEngine.extract_entities_and_subqueries(prompt, UserIntent.CODE_IMPLEMENTATION)
        self.assertTrue(len(decomp["entities"]) > 0)
        self.assertIn("json", decomp["clean_topic"].lower())

    def test_knowledge_gleaning_and_scaffolding(self):
        sources = [
            {
                "title": "Smartphone",
                "snippet": "A smartphone is a portable computer device that combines mobile telephone functions and computing functions. Modern smartphones feature touchscreen interfaces and cellular network access."
            },
            {
                "title": "Mobile Technology",
                "snippet": "Mobile technology powers billions of devices globally, using ARM-based System-on-Chips and advanced battery management."
            }
        ]
        gleaned = PromptUnderstandingEngine.glean_information("find info on smartphones", sources)
        self.assertEqual(gleaned.intent, UserIntent.FACTUAL_LOOKUP)
        self.assertTrue(len(gleaned.key_facts) > 0)
        
        sys_p, user_p = PromptUnderstandingEngine.scaffold_local_model_prompt(gleaned)
        self.assertIn("Janus Local Engine", sys_p)
        self.assertIn("Factual Lookup", user_p)
        self.assertIn("Gleaned Reference Knowledge", user_p)

    def test_deterministic_synthesis_no_corporate_boilerplate(self):
        sources = [
            {
                "title": "Photosynthesis",
                "snippet": "Photosynthesis is a biological process used by plants and other organisms to convert light energy into chemical energy."
            }
        ]
        gleaned = PromptUnderstandingEngine.glean_information("explain photosynthesis", sources)
        md = PromptUnderstandingEngine.synthesize_structured_markdown(gleaned)
        self.assertIn("Photosynthesis", md)
        self.assertNotIn("Decoupled Control & State Planes", md)
        self.assertNotIn("NIST SSDF provenance standards", md)
        self.assertNotIn("Intelligence Dossier", md)

    def test_distillation_status_metrics(self):
        status = DistillationTrainingManager.get_training_status()
        self.assertIn("status", status)
        self.assertIn("distilled_traces_count", status)
        self.assertIn("frontier_parity_score", status)
        self.assertIn("auto_distill_enabled", status)
        self.assertIn("session_traces_pending", status)
        self.assertGreater(status["distilled_traces_count"], 0)
        self.assertGreater(status["frontier_parity_score"], 70.0)

    def test_auto_session_distillation_record_and_trigger(self):
        mgr = AutoSessionDistillationManager.get_instance()
        initial_pending = mgr.traces_pending
        mgr.record_session_trace(
            prompt="analyze algorithmic time complexity of quicksort",
            response="Quicksort achieves O(n log n) average time complexity using divide-and-conquer partitioning.",
            task_category="code",
            teacher_model="janus-reasoner:3b",
            thought_chain="Trace partition recurrence relations.",
            critic_score=0.99
        )
        self.assertGreaterEqual(mgr.traces_pending, initial_pending + 1)
        res = mgr.trigger_post_session_distillation(reason="UNIT_TEST_TRIGGER", compile_ollama=False)
        self.assertEqual(res["status"], "AUTO_DISTILLATION_COMPLETED")
        self.assertEqual(mgr.traces_pending, 0)
        self.assertGreater(res["frontier_parity_score"], 80.0)
        self.assertIn("sft_dataset", res)

    def test_auto_session_status_payload(self):
        mgr = AutoSessionDistillationManager.get_instance()
        status = mgr.get_session_status()
        self.assertIn("session_id", status)
        self.assertIn("auto_distill_enabled", status)
        self.assertIn("traces_pending", status)
        self.assertIn("total_session_traces", status)
        self.assertTrue(status["auto_distill_enabled"])


if __name__ == "__main__":
    unittest.main()
