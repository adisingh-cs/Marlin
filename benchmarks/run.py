#!/usr/bin/env python3
"""
run.py — Marlin benchmark runner.

For each prompt in benchmarks/prompts/test-prompts.txt:
1. Count tokens in original (estimate using character heuristic)
2. Apply each of the 4 Marlin modes via Anthropic API
3. Count tokens in compressed output
4. Calculate reduction %
5. Write results to benchmarks/results/v1-baseline.json

Requires: ANTHROPIC_API_KEY environment variable
Requires: pip install anthropic

Usage:
    python benchmarks/run.py
"""

import os
import sys
import json
import math
import re
from datetime import datetime, timezone

try:
    import anthropic
except ImportError:
    print("ERROR: 'anthropic' package not installed.")
    print("Install with: pip install anthropic")
    sys.exit(1)


def estimate_tokens(text, text_type="natural-language"):
    """Estimate token count using character-based heuristic."""
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
    blocks = re.split(r"^# (PROMPT-\d+)", content, flags=re.MULTILINE)

    # blocks[0] is empty, then alternating id/text pairs
    for i in range(1, len(blocks), 2):
        prompt_id = blocks[i].strip()
        # Extract just the ID part (e.g., "PROMPT-001")
        prompt_id = prompt_id.split(" ")[0] if " " in prompt_id else prompt_id
        prompt_text = blocks[i + 1].strip() if i + 1 < len(blocks) else ""
        if prompt_text:
            prompts.append((prompt_id, prompt_text))

    return prompts


def load_skill(skill_name, skills_root):
    """Load a SKILL.md file content."""
    skill_path = os.path.join(skills_root, skill_name, "SKILL.md")
    if not os.path.isfile(skill_path):
        return None
    with open(skill_path, "r", encoding="utf-8") as f:
        return f.read()


def compress_prompt(client, prompt_text, skill_content, mode):
    """Send a prompt through Marlin compression via API."""
    system_prompt = f"""You are Marlin, an AI input prompt optimizer. Apply the following skill to compress the user's prompt. Return ONLY the compressed JSON output — no explanations, no markdown, no code fences.

SKILL:
{skill_content}

MODE: {mode}
"""

    try:
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1024,
            system=system_prompt,
            messages=[{"role": "user", "content": prompt_text}],
        )
        return message.content[0].text.strip()
    except Exception as e:
        return f"ERROR: {str(e)}"


def main():
    # Check API key
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("ERROR: ANTHROPIC_API_KEY environment variable not set.")
        sys.exit(1)

    client = anthropic.Anthropic(api_key=api_key)

    # Determine paths
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    prompts_path = os.path.join(repo_root, "benchmarks", "prompts", "test-prompts.txt")
    results_path = os.path.join(repo_root, "benchmarks", "results", "v1-baseline.json")
    skills_root = os.path.join(repo_root, "skills")

    # Parse prompts
    prompts = parse_prompts(prompts_path)
    print(f"Loaded {len(prompts)} test prompts\n")

    # Define modes and their corresponding skills
    modes = {
        "structured": "marlin-structured",
        "compact": "marlin-compact",
        "dense": "marlin-dense",
        "domain": "marlin-domain",
    }

    # Load all skills
    skill_contents = {}
    for mode, skill_name in modes.items():
        content = load_skill(skill_name, skills_root)
        if content:
            skill_contents[mode] = content
        else:
            print(f"WARNING: Could not load skill {skill_name}")

    results = []
    mode_totals = {mode: {"total_reduction": 0, "count": 0} for mode in modes}

    for prompt_id, prompt_text in prompts:
        original_tokens = estimate_tokens(prompt_text, "natural-language")
        print(f"Processing {prompt_id} ({original_tokens} tokens est.)...")

        for mode, skill_name in modes.items():
            if mode not in skill_contents:
                continue

            compressed = compress_prompt(
                client, prompt_text, skill_contents[mode], mode
            )

            if compressed.startswith("ERROR:"):
                print(f"  {mode}: {compressed}")
                continue

            compressed_tokens = estimate_tokens(compressed, "json")
            reduction_pct = round(
                (1 - compressed_tokens / original_tokens) * 100
            ) if original_tokens > 0 else 0

            result = {
                "prompt_id": prompt_id.lower().replace("prompt-", ""),
                "mode": mode,
                "original_tokens": original_tokens,
                "compressed_tokens": compressed_tokens,
                "reduction_pct": max(0, reduction_pct),
                "original_preview": prompt_text[:50] + "..." if len(prompt_text) > 50 else prompt_text,
                "compressed_preview": compressed[:50] + "..." if len(compressed) > 50 else compressed,
            }
            results.append(result)

            mode_totals[mode]["total_reduction"] += max(0, reduction_pct)
            mode_totals[mode]["count"] += 1

            print(f"  {mode}: {original_tokens} → {compressed_tokens} tokens ({reduction_pct}%)")

    # Calculate summary
    summary = {}
    for mode, totals in mode_totals.items():
        avg = round(totals["total_reduction"] / totals["count"]) if totals["count"] > 0 else 0
        summary[mode] = {"avg_reduction_pct": avg}

    # Build output
    output = {
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "model": "claude-sonnet-4-20250514",
        "prompts_tested": len(prompts),
        "results": results,
        "summary": summary,
    }

    # Write results
    os.makedirs(os.path.dirname(results_path), exist_ok=True)
    with open(results_path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"\nResults written to {results_path}")
    print(f"\nSummary:")
    for mode, stats in summary.items():
        print(f"  {mode}: avg {stats['avg_reduction_pct']}% reduction")


if __name__ == "__main__":
    main()
