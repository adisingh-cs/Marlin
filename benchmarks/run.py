#!/usr/bin/env python3
"""
run.py - Marlin benchmark runner.

For each prompt in benchmarks/prompts/test-prompts.txt:
1. Count tokens in the original prompt with Marlin's heuristic estimator.
2. Ask an OpenRouter model to apply the root SKILL.md for each Marlin mode.
3. Count tokens in the compressed output with the same heuristic estimator.
4. Record absolute savings, percent savings, and compression-system overhead.
5. Write results to benchmarks/results/v1-baseline.json by default.

Usage:
    python benchmarks/run.py --model openai/gpt-4o-mini
    python benchmarks/run.py --api-key <key> --model anthropic/claude-3.5-sonnet

Environment:
    OPENROUTER_API_KEY   API key used when --api-key is omitted.
    OPENROUTER_MODEL     Model used when --model is omitted.
"""

from __future__ import annotations

import argparse
import json
import math
import os
import re
import sys
import urllib.error
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


DEFAULT_API_BASE = "https://openrouter.ai/api/v1"
DEFAULT_MODEL = "openai/gpt-4o-mini"
DEFAULT_MODES = [
    "swift",
    "sharp",
    "strike",
    "sonar:web-api",
    "sonar:data-pipeline",
    "sonar:agent-task",
]


@dataclass(frozen=True)
class BenchmarkConfig:
    api_key: str
    model: str
    modes: list[str]
    api_base: str
    max_tokens: int
    site_url: str | None
    app_title: str
    prompts_path: Path
    skill_path: Path
    results_path: Path


def estimate_tokens(text, text_type="natural-language"):
    """Estimate token count using the repository's character heuristic."""
    if not text:
        return 0
    length = len(text)
    if text_type == "json":
        return math.ceil(length / 3.5)
    return math.ceil(length / 4)


def parse_prompts(filepath):
    """Parse test prompts file into list of (id, text) tuples."""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    prompts = []
    blocks = re.split(r"^# (PROMPT-\d+).*$", content, flags=re.MULTILINE)

    for i in range(1, len(blocks), 2):
        prompt_id = blocks[i].strip()
        prompt_text = blocks[i + 1].strip() if i + 1 < len(blocks) else ""
        if prompt_text:
            prompts.append((prompt_id, prompt_text))

    return prompts


def parse_args(argv=None):
    repo_root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(
        description="Run Marlin prompt-compression benchmarks through OpenRouter."
    )
    parser.add_argument(
        "--api-key",
        help="OpenRouter API key. Defaults to OPENROUTER_API_KEY.",
    )
    parser.add_argument(
        "--model",
        help=f"OpenRouter model id. Defaults to OPENROUTER_MODEL or {DEFAULT_MODEL}.",
    )
    parser.add_argument(
        "--modes",
        default=",".join(DEFAULT_MODES),
        help="Comma-separated modes. Use sonar:<schema> for domain schemas.",
    )
    parser.add_argument(
        "--api-base",
        default=DEFAULT_API_BASE,
        help=f"OpenRouter-compatible API base. Defaults to {DEFAULT_API_BASE}.",
    )
    parser.add_argument(
        "--max-tokens",
        type=int,
        default=1024,
        help="Maximum completion tokens per compression request.",
    )
    parser.add_argument(
        "--site-url",
        default=os.environ.get("OPENROUTER_SITE_URL"),
        help="Optional HTTP-Referer value for OpenRouter app attribution.",
    )
    parser.add_argument(
        "--app-title",
        default=os.environ.get("OPENROUTER_APP_TITLE", "Marlin Benchmark"),
        help="Optional X-OpenRouter-Title value for app attribution.",
    )
    parser.add_argument(
        "--prompts",
        type=Path,
        default=repo_root / "benchmarks" / "prompts" / "test-prompts.txt",
        help="Path to benchmark prompts file.",
    )
    parser.add_argument(
        "--skill",
        type=Path,
        default=repo_root / "SKILL.md",
        help="Path to Marlin SKILL.md.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=repo_root / "benchmarks" / "results" / "v1-baseline.json",
        help="Path to write benchmark JSON results.",
    )
    return parser.parse_args(argv)


def resolve_config(args):
    api_key = args.api_key or os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        print(
            "ERROR: OpenRouter API key not provided. Use --api-key or set OPENROUTER_API_KEY.",
            file=sys.stderr,
        )
        raise SystemExit(1)

    modes = [mode.strip() for mode in args.modes.split(",") if mode.strip()]
    if not modes:
        print("ERROR: at least one mode is required.", file=sys.stderr)
        raise SystemExit(1)

    return BenchmarkConfig(
        api_key=api_key,
        model=args.model or os.environ.get("OPENROUTER_MODEL") or DEFAULT_MODEL,
        modes=modes,
        api_base=args.api_base.rstrip("/"),
        max_tokens=args.max_tokens,
        site_url=args.site_url,
        app_title=args.app_title,
        prompts_path=args.prompts,
        skill_path=args.skill,
        results_path=args.output,
    )


def split_mode(mode):
    if ":" not in mode:
        return mode, None
    name, schema = mode.split(":", 1)
    return name, schema


def build_system_prompt(skill_content, mode):
    mode_name, schema = split_mode(mode)
    schema_line = f"\nSCHEMA: {schema}" if schema else ""
    return f"""You are Marlin, an AI input prompt optimizer. Apply the following skill to compress the user's prompt. Return ONLY the compressed JSON output - no explanations, no markdown, no code fences.

SKILL:
{skill_content}

MODE: {mode_name}{schema_line}
"""


def build_openrouter_request(
    api_key,
    model,
    skill_content,
    prompt_text,
    mode,
    max_tokens,
    api_base=DEFAULT_API_BASE,
    site_url=None,
    app_title="Marlin Benchmark",
):
    system_prompt = build_system_prompt(skill_content, mode)
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "X-OpenRouter-Title": app_title,
    }
    if site_url:
        headers["HTTP-Referer"] = site_url

    return {
        "url": f"{api_base.rstrip('/')}/chat/completions",
        "headers": headers,
        "payload": {
            "model": model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt_text},
            ],
            "temperature": 0,
            "max_tokens": max_tokens,
        },
        "system_prompt": system_prompt,
    }


def post_openrouter(request_data):
    body = json.dumps(request_data["payload"]).encode("utf-8")
    request = urllib.request.Request(
        request_data["url"],
        data=body,
        headers=request_data["headers"],
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=120) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"OpenRouter HTTP {exc.code}: {detail}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"OpenRouter request failed: {exc.reason}") from exc


def extract_completion(response_json):
    try:
        return response_json["choices"][0]["message"]["content"].strip()
    except (KeyError, IndexError, AttributeError) as exc:
        raise RuntimeError(f"Unexpected OpenRouter response: {response_json}") from exc


def extract_usage(response_json):
    usage = response_json.get("usage") or {}
    return {
        "prompt_tokens": usage.get("prompt_tokens"),
        "completion_tokens": usage.get("completion_tokens"),
        "total_tokens": usage.get("total_tokens"),
    }


def build_result(
    prompt_id,
    mode,
    prompt_text,
    compressed,
    prompt_tokens_reported,
    completion_tokens_reported,
    system_prompt_tokens,
):
    original_tokens = estimate_tokens(prompt_text, "natural-language")
    compressed_tokens = estimate_tokens(compressed, "json")
    absolute_savings = original_tokens - compressed_tokens
    reduction_pct = (
        round((1 - compressed_tokens / original_tokens) * 100)
        if original_tokens > 0
        else 0
    )

    return {
        "prompt_id": prompt_id.lower().replace("prompt-", ""),
        "mode": mode,
        "source": "benchmarks/prompts/test-prompts.txt",
        "original_tokens": original_tokens,
        "compressed_tokens": compressed_tokens,
        "absolute_token_savings": absolute_savings,
        "reduction_pct": reduction_pct,
        "compression_system_overhead_tokens": system_prompt_tokens,
        "api_prompt_tokens": prompt_tokens_reported,
        "api_completion_tokens": completion_tokens_reported,
        "original_preview": prompt_text[:80] + "..."
        if len(prompt_text) > 80
        else prompt_text,
        "compressed_preview": compressed[:120] + "..."
        if len(compressed) > 120
        else compressed,
    }


def summarize_results(results, modes):
    summary = {}
    for mode in modes:
        rows = [row for row in results if row["mode"] == mode]
        if not rows:
            summary[mode] = {
                "runs": 0,
                "avg_reduction_pct": 0,
                "avg_absolute_token_savings": 0,
            }
            continue

        summary[mode] = {
            "runs": len(rows),
            "avg_original_tokens": round(
                sum(row["original_tokens"] for row in rows) / len(rows), 1
            ),
            "avg_compressed_tokens": round(
                sum(row["compressed_tokens"] for row in rows) / len(rows), 1
            ),
            "avg_absolute_token_savings": round(
                sum(row["absolute_token_savings"] for row in rows) / len(rows), 1
            ),
            "avg_reduction_pct": round(
                sum(row["reduction_pct"] for row in rows) / len(rows), 1
            ),
            "avg_compression_system_overhead_tokens": round(
                sum(row["compression_system_overhead_tokens"] for row in rows)
                / len(rows),
                1,
            ),
        }
    return summary


def compress_prompt(config, skill_content, prompt_text, mode):
    request_data = build_openrouter_request(
        api_key=config.api_key,
        model=config.model,
        skill_content=skill_content,
        prompt_text=prompt_text,
        mode=mode,
        max_tokens=config.max_tokens,
        api_base=config.api_base,
        site_url=config.site_url,
        app_title=config.app_title,
    )
    response_json = post_openrouter(request_data)
    compressed = extract_completion(response_json)
    usage = extract_usage(response_json)
    return compressed, usage, estimate_tokens(
        request_data["system_prompt"], "natural-language"
    )


def run_benchmark(config):
    skill_content = config.skill_path.read_text(encoding="utf-8")
    prompts = parse_prompts(config.prompts_path)
    results = []

    print(f"Loaded {len(prompts)} test prompts")
    print(f"Provider: OpenRouter")
    print(f"Model: {config.model}")
    print(f"Modes: {', '.join(config.modes)}\n")

    for prompt_id, prompt_text in prompts:
        original_tokens = estimate_tokens(prompt_text, "natural-language")
        print(f"Processing {prompt_id} ({original_tokens} tokens est.)...")

        for mode in config.modes:
            try:
                compressed, usage, system_prompt_tokens = compress_prompt(
                    config, skill_content, prompt_text, mode
                )
                result = build_result(
                    prompt_id=prompt_id,
                    mode=mode,
                    prompt_text=prompt_text,
                    compressed=compressed,
                    prompt_tokens_reported=usage["prompt_tokens"],
                    completion_tokens_reported=usage["completion_tokens"],
                    system_prompt_tokens=system_prompt_tokens,
                )
                results.append(result)
                print(
                    "  {mode}: {original} -> {compressed} tokens "
                    "({pct}%, saved {saved})".format(
                        mode=mode,
                        original=result["original_tokens"],
                        compressed=result["compressed_tokens"],
                        pct=result["reduction_pct"],
                        saved=result["absolute_token_savings"],
                    )
                )
            except Exception as exc:
                print(f"  {mode}: ERROR: {exc}", file=sys.stderr)

    summary = summarize_results(results, config.modes)
    output = {
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "provider": "openrouter",
        "api_base": config.api_base,
        "model": config.model,
        "prompts_tested": len(prompts),
        "modes_requested": config.modes,
        "token_counter": "heuristic: ceil(len(natural_language)/4), ceil(len(json)/3.5)",
        "methodology_notes": [
            "Compression is model-mediated and therefore nondeterministic unless the selected model/provider honors deterministic settings.",
            "Token counts are approximate unless api_prompt_tokens/api_completion_tokens are returned by OpenRouter.",
            "compression_system_overhead_tokens estimates the system prompt containing SKILL.md and should not be counted as downstream prompt savings.",
        ],
        "results": results,
        "summary": summary,
    }

    config.results_path.parent.mkdir(parents=True, exist_ok=True)
    config.results_path.write_text(
        json.dumps(output, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    print(f"\nResults written to {config.results_path}")
    print("\nSummary:")
    for mode, stats in summary.items():
        print(
            f"  {mode}: n={stats['runs']}, "
            f"avg {stats['avg_reduction_pct']}% reduction, "
            f"avg saved {stats['avg_absolute_token_savings']} tokens"
        )

    return output


def main(argv=None):
    args = parse_args(argv)
    config = resolve_config(args)
    run_benchmark(config)


if __name__ == "__main__":
    main()
