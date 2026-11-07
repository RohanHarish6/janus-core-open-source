"""
tests/test_perplexity_max.py - Comprehensive Unit Tests for
Perplexity Max Intelligence & Multi-Hop Research Engine.
"""

import unittest
from perplexity_max_engine import (
    PerplexityMaxQueryDecomposer,
    PerplexityMaxSearchRetriever,
    PerplexityMaxEngine,
    ResearchSource,
    ResearchTrajectoryStep,
    get_perplexity_max_engine
)


class TestPerplexityMaxEngine(unittest.TestCase):

    def setUp(self):
        self.engine = get_perplexity_max_engine()

    def test_query_decomposition_comparison(self):
        prompt = "Next.js vs Remix performance comparison"
        sub_queries = PerplexityMaxQueryDecomposer.decompose(prompt)
        self.assertTrue(len(sub_queries) >= 3)
        self.assertTrue(any("Next.js" in q for q in sub_queries))
        self.assertTrue(any("Remix" in q for q in sub_queries))

    def test_query_decomposition_guide(self):
        prompt = "how to build a distributed actor system in Rust"
        sub_queries = PerplexityMaxQueryDecomposer.decompose(prompt)
        self.assertTrue(len(sub_queries) >= 3)
        self.assertTrue(any("best practices" in q or "architecture" in q for q in sub_queries))

    def test_perplexity_report_synthesis_structure(self):
        prompt = "Quantum Computing Fault Tolerance"
        mock_sources = [
            ResearchSource(
                index=1,
                title="Quantum Error Correction Overview",
                url="https://en.wikipedia.org/wiki/Quantum_error_correction",
                domain="en.wikipedia.org",
                snippet="Quantum error correction is used in quantum computing to protect quantum information from errors due to decoherence.",
                full_content="Quantum error correction (QEC) is used in quantum computing to protect quantum information from errors due to decoherence and other quantum noise.",
                reliability_score=0.98
            ),
            ResearchSource(
                index=2,
                title="Surface Codes in Superconducting Qubits",
                url="https://example.com/surface-codes",
                domain="example.com",
                snippet="Surface codes offer a realistic path to fault-tolerant quantum computing with a 1 percent error threshold.",
                full_content="Surface codes are a 2D topological quantum error-correcting code capable of protecting qubits with relatively low physical overhead.",
                reliability_score=0.92
            )
        ]
        mock_trajectory = [
            ResearchTrajectoryStep(phase="DECOMPOSE", label="Planning", detail="Decomposed into 4 queries", duration_ms=1.2),
            ResearchTrajectoryStep(phase="SEARCH", label="Retrieval", detail="2 sources retrieved", duration_ms=45.0),
            ResearchTrajectoryStep(phase="READ", label="Ingestion", detail="Scraped 2 sources", duration_ms=30.0),
            ResearchTrajectoryStep(phase="SYNTHESIZE", label="Synthesis", detail="Generated citations", duration_ms=12.0)
        ]

        report = self.engine._synthesize_perplexity_max_report(prompt, mock_sources, mock_trajectory)
        
        # Verify Key Perplexity Max Elements
        self.assertIn("perplexity-thinking-tray", report)
        self.assertIn("perplexity-source-tray", report)
        self.assertIn("[1]", report)
        self.assertIn("[2]", report)
        self.assertIn("Executive Summary", report)
        self.assertIn("Empirical Comparison & Evaluation Matrix", report)
        self.assertIn("Verified Sources & Bibliography", report)

    def test_follow_up_inquiries_generation(self):
        prompt = "GraphQL vs REST in 2026"
        mock_sources = [
            ResearchSource(index=1, title="API Design", url="https://example.com", domain="example.com", snippet="APIs connect systems.")
        ]
        follow_ups = self.engine._generate_follow_up_inquiries(prompt, mock_sources)
        self.assertEqual(len(follow_ups), 3)
        for q in follow_ups:
            self.assertTrue(q.endswith("?"))
            self.assertIn("GraphQL vs REST", q)


if __name__ == "__main__":
    unittest.main()
