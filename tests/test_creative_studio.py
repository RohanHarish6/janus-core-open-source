"""
Tests for Creative Studio (Aesthetic PDF, DOCX, Infographics, Web Images, and Short Videos).
Includes tests for Triple-Skill enhancements (taste-skill, prompt-optimizer, fine-tuning-expert).
"""

import os
import unittest
import tempfile
import shutil
import json

from creative_studio import (
    AestheticPDFGenerator,
    AestheticDocxGenerator,
    HighQualityInfographicGenerator,
    WebImageGenerator,
    ShortVideoGenerator,
    CreativeStudio,
    CreativePromptOptimizer,
    CreativeStudioFineTuningPipeline,
    AestheticThemeEngine,
    ClaudeArtifactAnimationEngine,
    GPTStylePromptExpander,
    ZeroTokenImageRouter,
    AestheticVibeCodeGenerator
)


class TestCreativeStudio(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_high_quality_infographic_generation(self):
        out_png = os.path.join(self.temp_dir, "test_infographic.png")
        res = HighQualityInfographicGenerator.generate_kpi_dashboard(
            title="Capital Solvency & Architecture Telemetry",
            metrics=[{"tokens": 80}, {"tokens": 65}, {"tokens": 90}, {"tokens": 40}],
            output_path=out_png,
            dpi=150
        )
        self.assertTrue(os.path.exists(res))
        self.assertGreater(os.path.getsize(res), 50000)

    def test_radar_benchmark_generation(self):
        out_radar = os.path.join(self.temp_dir, "test_radar.png")
        res = HighQualityInfographicGenerator.generate_radar_benchmark(
            title="Agentic Capability Radar",
            dimensions=["Cost Efficiency", "Latency", "Accuracy", "Memory Safety", "Security", "Alignment"],
            scores=[9.5, 9.0, 9.8, 9.2, 10.0, 9.6],
            output_path=out_radar,
            dpi=150,
            theme_name="emerald_growth"
        )
        self.assertTrue(os.path.exists(res))
        self.assertGreater(os.path.getsize(res), 20000)

    def test_aesthetic_pdf_generation(self):
        out_pdf = os.path.join(self.temp_dir, "test_report.pdf")
        out_chart = os.path.join(self.temp_dir, "test_chart.png")
        HighQualityInfographicGenerator.generate_kpi_dashboard(
            title="Chart",
            output_path=out_chart,
            dpi=100
        )

        res = AestheticPDFGenerator.generate_report(
            output_path=out_pdf,
            title="Janus Core Operational Review",
            subtitle="Autonomous Multi-Agent Telemetry & Verification",
            author="Janus Core Lead Architect",
            organization="Autonomous Intelligence Labs",
            kpis=[
                {"value": "73.7%", "label": "Cost Savings"},
                {"value": "75.0%", "label": "Zero-Cost Offload"},
                {"value": "3.8x", "label": "Output Compression"}
            ],
            sections=[
                {
                    "heading": "1. Executive Summary",
                    "callout": "Strategic mandate: Maximize zero-cost model offload while guaranteeing mathematical correctness.",
                    "content": "Janus Core successfully dispatches multi-agent tasks across heterogeneous compute tiers without unbounded context bloat."
                }
            ],
            table_title="Model Routing Matrix",
            table_data=[
                ["Tier Name", "Compute Target", "Cost / 1K Tokens", "Status"],
                ["Tier 0", "Local Ollama (llama3.2)", "$0.000", "ACTIVE"],
                ["Tier 1", "Colibri MoE (NVMe)", "$0.000", "ACTIVE"],
                ["Tier 2", "FreeLLMAPI Cloud", "$0.000", "ACTIVE"],
                ["Tier 3", "Frontier API", "$0.015", "GATED"]
            ],
            chart_image_path=out_chart,
            theme_name="cobalt_tech"
        )
        self.assertTrue(os.path.exists(res))
        self.assertGreater(os.path.getsize(res), 5000)

    def test_aesthetic_docx_generation(self):
        out_docx = os.path.join(self.temp_dir, "test_document.docx")
        out_chart = os.path.join(self.temp_dir, "test_chart.png")
        HighQualityInfographicGenerator.generate_kpi_dashboard(
            title="Chart",
            output_path=out_chart,
            dpi=100
        )

        res = AestheticDocxGenerator.generate_document(
            output_path=out_docx,
            title="Janus Core Technical Specification",
            subtitle="Autonomous ReAct Model Router & Security Matrix",
            author="Janus Core Lead Architect",
            organization="Autonomous Intelligence Labs",
            kpis=[
                {"value": "2.19 GB", "label": "Peak RAM"},
                {"value": "4 Cores", "label": "Concurrency Cap"},
                {"value": "85.0°C", "label": "Thermal Tripwire"}
            ],
            sections=[
                {
                    "heading": "1. Architectural Constraints",
                    "callout": "All worker thread pools are capped at physical core topology to eliminate thermal throttling.",
                    "content": "Testing on the Dell Inspiron 5410 baseline demonstrates sustained all-core boost clocks without fan whine."
                }
            ],
            table_title="Hardware Profile Table",
            table_data=[
                ["Component", "Constraint", "Enforcement Engine"],
                ["CPU", "4 Threads Max", "DellInspiron5410Config"],
                ["RAM", "4.5 GB Ceiling", "DynamicMemoryWatchdog"],
                ["Power", "Battery Failover", "HardwareProfileDetector"]
            ],
            chart_image_path=out_chart,
            theme_name="charcoal_amber"
        )
        self.assertTrue(os.path.exists(res))
        self.assertGreater(os.path.getsize(res), 20000)

    def test_web_image_generation(self):
        out_img = os.path.join(self.temp_dir, "test_concept.png")
        res = WebImageGenerator.generate_image(
            prompt="Futuristic autonomous AI multi-agent skyscraper network",
            output_path=out_img,
            width=640,
            height=360
        )
        self.assertTrue(os.path.exists(res))
        self.assertGreater(os.path.getsize(res), 5000)

    def test_short_video_generation(self):
        out_mp4 = os.path.join(self.temp_dir, "test_brief.mp4")
        video_path, gif_path = ShortVideoGenerator.generate_video_brief(
            output_mp4_path=out_mp4,
            title="Janus Core Motion Brief",
            subtitle="Autonomous Multi-Agent ReAct Telemetry",
            kpi_text="Offload: 75.0%",
            duration_sec=2,
            fps=15,
            width=640,
            height=360,
            include_audio=True
        )
        self.assertTrue(os.path.exists(video_path))
        self.assertTrue(os.path.exists(gif_path))
        self.assertGreater(os.path.getsize(video_path), 5000)
        self.assertGreater(os.path.getsize(gif_path), 5000)

    def test_prompt_optimizer_creative_brief(self):
        raw_prompt = "build me an aesthetic quarterly risk presentation with clean charts"
        brief = CreativePromptOptimizer.optimize_creative_brief(raw_prompt)
        self.assertEqual(brief["role"], "Autonomous Executive Media Director & Visual Communication Engineer")
        self.assertEqual(brief["design_variance"], 7)
        self.assertIn("pdf_margins_pt", brief["verifiable_constraints"])
        self.assertEqual(brief["verifiable_constraints"]["infographic_dpi"], 300)

    def test_fine_tuning_artifacts_export(self):
        ft_dir = os.path.join(self.temp_dir, "fine_tuning_export")
        artifacts = CreativeStudioFineTuningPipeline.export_training_artifacts(ft_dir)
        self.assertTrue(os.path.exists(artifacts["dataset"]))
        self.assertTrue(os.path.exists(artifacts["config"]))
        self.assertTrue(os.path.exists(artifacts["modelfile"]))

        with open(artifacts["dataset"], "r") as f:
            lines = f.readlines()
            self.assertGreater(len(lines), 0)
            sample = json.loads(lines[0])
            self.assertIn("messages", sample)

    def test_creative_studio_produce_executive_package(self):
        studio = CreativeStudio(output_root=self.temp_dir)
        package = studio.produce_executive_package(
            title="Q4 Model Optimization Package",
            subtitle="Multi-Agent Token Efficiency & Security Audit",
            kpis=[
                {"value": "73.7%", "label": "Cost Savings"},
                {"value": "100%", "label": "Cache Hit Rate"}
            ],
            sections=[
                {
                    "heading": "1. Operational Highlights",
                    "callout": "Convergence verified across all 4 inference tiers with zero AST violations.",
                    "content": "All execution artifacts generated with 300 DPI clarity and executive-grade typography."
                }
            ],
            table_data=[
                ["Metric", "Target", "Achieved"],
                ["Token Offload", ">=70%", "75.0%"],
                ["Cost Savings", ">=65%", "73.7%"]
            ]
        )
        expected_keys = [
            "pdf_report", "word_document", "infographic_300dpi", "radar_benchmark",
            "concept_image", "video_brief_mp4", "video_preview_gif",
            "sft_dataset_jsonl", "qlora_config_yaml", "ollama_modelfile"
        ]
        for key in expected_keys:
            self.assertIn(key, package)
            path = package[key]
            self.assertTrue(os.path.exists(path), f"File {key} at {path} does not exist!")
            self.assertGreater(os.path.getsize(path), 100, f"File {key} is too small!")

    def test_claude_interactive_artifact_generation(self):
        out_html = os.path.join(self.temp_dir, "test_interactive_artifact.html")
        res = ClaudeArtifactAnimationEngine.generate_interactive_artifact(
            title="Janus Swarm Intelligence",
            subtitle="Autonomous Multi-Agent Kinetic Field",
            archetype="particle_swarm",
            theme_name="slate_sky",
            output_path=out_html
        )
        self.assertTrue(os.path.exists(res))
        self.assertGreater(os.path.getsize(res), 5000)
        with open(res, "r", encoding="utf-8") as f:
            html = f.read()
            self.assertIn('<canvas id="artifact-canvas">', html)
            self.assertIn("Claude-Tier Artifact", html)
            self.assertIn("Zero Paid Tokens", html)
            self.assertIn("play-pause-btn", html)
            self.assertIn("snapshot-btn", html)
            self.assertIn("archetype-select", html)

    def test_claude_animation_video_and_gif(self):
        out_mp4 = os.path.join(self.temp_dir, "test_claude_motion.mp4")
        mp4_path, gif_path = ClaudeArtifactAnimationEngine.generate_animation_video_and_gif(
            output_mp4_path=out_mp4,
            title="Janus Swarm Simulation",
            subtitle="Claude-Level Physics Simulation",
            archetype="neural_synapse",
            duration_sec=2,
            fps=15,
            width=640,
            height=360
        )
        self.assertTrue(os.path.exists(mp4_path))
        self.assertTrue(os.path.exists(gif_path))
        self.assertGreater(os.path.getsize(mp4_path), 5000)
        self.assertGreater(os.path.getsize(gif_path), 5000)

    def test_gpt_style_prompt_expander(self):
        raw = "autonomous trading network at dusk"
        res = GPTStylePromptExpander.expand_prompt(raw)
        self.assertEqual(res["original_prompt"], raw)
        self.assertIn("Cinematic wide-angle view of autonomous trading network", res["expanded_prompt"])
        self.assertIn("Hasselblad", res["expanded_prompt"])
        self.assertIn("8k resolution", res["expanded_prompt"])
        self.assertIn("blurry", res["negative_prompt"])
        self.assertEqual(res["cost_usd"], 0.0)
        self.assertEqual(res["paid_tokens"], 0)

    def test_zero_token_image_router(self):
        out_png = os.path.join(self.temp_dir, "test_gpt_image.png")
        res = ZeroTokenImageRouter.generate_image(
            prompt="futuristic AI financial research command center",
            output_path=out_png,
            width=640,
            height=360,
            model="flux",
            expand_prompt=True
        )
        self.assertTrue(os.path.exists(out_png))
        self.assertGreater(os.path.getsize(out_png), 5000)
        self.assertEqual(res["cost_usd"], 0.0)
        self.assertEqual(res["paid_tokens"], 0)
        self.assertEqual(res["status"], "SUCCESS")
        self.assertIn("expanded_prompt", res)

    def test_produce_claude_gpt_creative_package(self):
        studio = CreativeStudio(output_root=self.temp_dir)
        pkg = studio.produce_claude_gpt_creative_package(
            prompt="autonomous multi-agent risk assessment citadel",
            title="Janus Flagship Creative Suite",
            subtitle="Claude-Level Animation & GPT-Level Image Generation"
        )
        expected_keys = [
            "pdf_report", "word_document", "infographic_300dpi", "radar_benchmark",
            "concept_image", "video_brief_mp4", "video_preview_gif",
            "claude_interactive_artifact", "sft_dataset_jsonl", "qlora_config_yaml",
            "ollama_modelfile", "cost_audit"
        ]
        for key in expected_keys:
            self.assertIn(key, pkg)
            if key != "cost_audit":
                path = pkg[key]
                self.assertTrue(os.path.exists(path), f"Package file {key} missing at {path}")
                self.assertGreater(os.path.getsize(path), 100)
        self.assertEqual(pkg["cost_audit"]["total_cost_usd"], 0.00)
        self.assertEqual(pkg["cost_audit"]["total_paid_tokens"], 0)

    def test_markdown_section_and_table_extraction(self):
        from desktop_app import extract_sections_from_markdown, extract_table_from_markdown
        sample_md = (
            "# Top Level Title\n\n"
            "## 1. Executive Strategy\n"
            "> Priority initiative for zero-cost multi-agent mesh\n"
            "The multi-agent system routes prompts across local and free cloud models.\n\n"
            "## 2. Telemetry Matrix\n"
            "| Component | Status | Latency |\n"
            "|---|---|---|\n"
            "| Ollama Tier 0 | ACTIVE | 12ms |\n"
            "| Colibri Tier 1 | ACTIVE | 45ms |\n"
        )
        sections = extract_sections_from_markdown(sample_md, default_heading="Test Brief")
        self.assertGreaterEqual(len(sections), 2)
        self.assertIn("1. Executive Strategy", [s["heading"] for s in sections])
        self.assertIn("Priority initiative", sections[0]["callout"])

        table = extract_table_from_markdown(sample_md)
        self.assertIsNotNone(table)
        self.assertEqual(len(table), 3) # Header + 2 data rows
        self.assertEqual(table[0], ["Component", "Status", "Latency"])
        self.assertEqual(table[1][0], "Ollama Tier 0")

    def test_workbench_binary_artifact_integrity(self):
        """Verifies that generated PDF, DOCX, and PNG files retain valid binary signatures and are not corrupted by text write."""
        from desktop_app import ARTIFACTS_DIR
        out_pdf = os.path.join(self.temp_dir, "verified_report.pdf")
        out_docx = os.path.join(self.temp_dir, "verified_doc.docx")
        out_png = os.path.join(self.temp_dir, "verified_img.png")

        AestheticPDFGenerator.generate_report(
            output_path=out_pdf,
            title="Integrity Verification Report",
            subtitle="Testing zero corruption",
            sections=[{"heading": "Section 1", "callout": "Safe callout", "content": "Sample content body"}]
        )
        AestheticDocxGenerator.generate_document(
            output_path=out_docx,
            title="Integrity Verification Document",
            subtitle="Testing zero corruption",
            sections=[{"heading": "Section 1", "callout": "Safe callout", "content": "Sample content body"}]
        )
        ZeroTokenImageRouter.generate_image(
            prompt="Abstract neural network concept",
            output_path=out_png,
            width=320,
            height=180
        )

        # Check binary headers
        with open(out_pdf, "rb") as f:
            pdf_bytes = f.read(5)
            self.assertEqual(pdf_bytes, b"%PDF-", "PDF must begin with %PDF- binary header")

        with open(out_docx, "rb") as f:
            docx_bytes = f.read(4)
            self.assertEqual(docx_bytes, b"PK\x03\x04", "DOCX must begin with PK zip header")

        with open(out_png, "rb") as f:
            png_bytes = f.read(8)
            self.assertEqual(png_bytes, b"\x89PNG\r\n\x1a\n", "PNG must begin with PNG magic header")

    def test_aesthetic_vibe_code_generation(self):
        """Verifies that AestheticVibeCodeGenerator produces a valid single-file HTML component adhering to taste-skill 8.0."""
        out_html = os.path.join(self.temp_dir, "test_vibe_node.html")
        res = AestheticVibeCodeGenerator.generate_vibe_component(
            title="Quantum Harmonics Telemetry Node",
            subtitle="Testing sovereign cybernetic vibe code",
            component_type="telemetry_card",
            accent_color="#06b6d4",
            secondary_accent="#10b981",
            output_path=out_html
        )

        self.assertTrue(os.path.exists(out_html), "Output HTML file must exist")
        self.assertGreater(os.path.getsize(out_html), 1000, "HTML file must contain substantial content")
        self.assertEqual(res["title"], "Quantum Harmonics Telemetry Node")
        self.assertEqual(res["file_path"], out_html)

        content = res["source_code"]
        self.assertIn("<!DOCTYPE html>", content)
        self.assertIn("vibe-artisan-card", content)
        self.assertIn("vibe-wave-canvas", content)
        # Anti-slop check: must contain cybernetic palette and no forbidden purple gradients
        self.assertIn("#060911", content)
        self.assertIn("#06b6d4", content)
        self.assertIn("#10b981", content)
        self.assertNotIn("#8b5cf6", content)
        self.assertNotIn("#a78bfa", content)
        # Verify WCAG AA and taste-skill compliance
        self.assertIn("WCAG AA", content)
        self.assertIn("TASTE-SKILL 8.0", content)

    def test_default_active_creative_skills_registry(self):
        """Verifies that default-active creative skills are properly defined and active by default."""
        from desktop_app import DEFAULT_ACTIVE_CREATIVE_SKILLS
        self.assertEqual(len(DEFAULT_ACTIVE_CREATIVE_SKILLS), 4)

        skill_ids = [s["id"] for s in DEFAULT_ACTIVE_CREATIVE_SKILLS]
        self.assertIn("skill-image-gen", skill_ids)
        self.assertIn("skill-video-gen", skill_ids)
        self.assertIn("skill-doc-forge", skill_ids)
        self.assertIn("skill-vibe-code", skill_ids)

        for skill in DEFAULT_ACTIVE_CREATIVE_SKILLS:
            self.assertTrue(skill["active"], f"Skill {skill['id']} must be active by default")
            self.assertIn("command_types", skill)
            self.assertGreater(len(skill["command_types"]), 0)


