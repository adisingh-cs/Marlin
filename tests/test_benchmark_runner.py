import importlib.util
import io
import json
import os
import sys
import tempfile
import unittest
from contextlib import redirect_stderr
from pathlib import Path
from unittest import mock


REPO_ROOT = Path(__file__).resolve().parents[1]
RUN_PATH = REPO_ROOT / "benchmarks" / "run.py"

spec = importlib.util.spec_from_file_location("marlin_benchmark_run", RUN_PATH)
bench = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = bench
spec.loader.exec_module(bench)


class BenchmarkRunnerTests(unittest.TestCase):
    def test_parse_prompts_keeps_prompt_ids_and_text(self):
        with tempfile.NamedTemporaryFile("w", delete=False, encoding="utf-8") as f:
            f.write("# PROMPT-001 - One\nFirst prompt\n\n# PROMPT-002 - Two\nSecond prompt")
            path = f.name

        try:
            prompts = bench.parse_prompts(path)
        finally:
            os.unlink(path)

        self.assertEqual(
            prompts,
            [("PROMPT-001", "First prompt"), ("PROMPT-002", "Second prompt")],
        )

    def test_config_prefers_cli_values_over_environment(self):
        args = bench.parse_args(
            [
                "--api-key",
                "cli-key",
                "--model",
                "openai/gpt-4o-mini",
                "--modes",
                "swift,sharp",
            ]
        )

        with mock.patch.dict(
            os.environ,
            {
                "OPENROUTER_API_KEY": "env-key",
                "OPENROUTER_MODEL": "anthropic/claude-3.5-sonnet",
            },
        ):
            config = bench.resolve_config(args)

        self.assertEqual(config.api_key, "cli-key")
        self.assertEqual(config.model, "openai/gpt-4o-mini")
        self.assertEqual(config.modes, ["swift", "sharp"])

    def test_config_uses_openrouter_environment_defaults(self):
        args = bench.parse_args([])

        with mock.patch.dict(
            os.environ,
            {
                "OPENROUTER_API_KEY": "env-key",
                "OPENROUTER_MODEL": "google/gemini-2.5-flash",
            },
            clear=True,
        ):
            config = bench.resolve_config(args)

        self.assertEqual(config.api_key, "env-key")
        self.assertEqual(config.model, "google/gemini-2.5-flash")
        self.assertIn("sonar:web-api", config.modes)

    def test_config_requires_api_key(self):
        args = bench.parse_args([])

        with mock.patch.dict(os.environ, {}, clear=True):
            stderr = io.StringIO()
            with redirect_stderr(stderr):
                with self.assertRaises(SystemExit) as raised:
                    bench.resolve_config(args)

        self.assertEqual(raised.exception.code, 1)
        self.assertIn("OpenRouter API key not provided", stderr.getvalue())

    def test_openrouter_request_uses_bearer_auth_and_chat_messages(self):
        request = bench.build_openrouter_request(
            api_key="test-key",
            model="openai/gpt-4o-mini",
            skill_content="SKILL BODY",
            prompt_text="Build a login endpoint",
            mode="sonar:web-api",
            max_tokens=512,
        )

        self.assertEqual(
            request["url"], "https://openrouter.ai/api/v1/chat/completions"
        )
        self.assertEqual(request["headers"]["Authorization"], "Bearer test-key")
        self.assertEqual(request["headers"]["X-OpenRouter-Title"], "Marlin Benchmark")
        self.assertEqual(request["payload"]["model"], "openai/gpt-4o-mini")
        self.assertEqual(request["payload"]["max_tokens"], 512)
        self.assertEqual(request["payload"]["temperature"], 0)
        self.assertEqual(request["payload"]["messages"][0]["role"], "system")
        self.assertIn("MODE: sonar", request["payload"]["messages"][0]["content"])
        self.assertIn(
            "SCHEMA: web-api", request["payload"]["messages"][0]["content"]
        )
        self.assertEqual(request["payload"]["messages"][1]["content"], "Build a login endpoint")

    def test_build_result_records_savings_and_overhead(self):
        result = bench.build_result(
            prompt_id="PROMPT-001",
            mode="sharp",
            prompt_text="A" * 80,
            compressed='{"g":"x"}',
            prompt_tokens_reported=200,
            completion_tokens_reported=10,
            system_prompt_tokens=150,
        )

        self.assertEqual(result["prompt_id"], "001")
        self.assertEqual(result["original_tokens"], 20)
        self.assertEqual(result["compressed_tokens"], 3)
        self.assertEqual(result["absolute_token_savings"], 17)
        self.assertEqual(result["reduction_pct"], 85)
        self.assertEqual(result["api_prompt_tokens"], 200)
        self.assertEqual(result["api_completion_tokens"], 10)
        self.assertEqual(result["compression_system_overhead_tokens"], 150)


if __name__ == "__main__":
    unittest.main()
