#!/usr/bin/env python3
"""
test-skill.py — Run test fixtures against Marlin skills via Anthropic API.

Reads test files from tests/skill-tests/{skill-name}.test.json.
For each test: loads the skill, sends input via Anthropic API,
validates output against the expected schema.

Requires: ANTHROPIC_API_KEY environment variable
Requires: pip install anthropic

Usage:
    python tools/test-skill.py --skill marlin-compact
    python tools/test-skill.py --all
"""

import os
import sys
import json
import argparse
import math

# Check for anthropic package availability
try:
    import anthropic
    HAS_ANTHROPIC = True
except ImportError:
    HAS_ANTHROPIC = False
    anthropic = None


def estimate_tokens(text, input_type="natural-language"):
    """Estimate token count using character-based heuristic."""
    if not text:
        return 0
    length = len(str(text))
    if input_type == "dsl":
        return math.ceil(length / 3)
    elif input_type in ("json", "compact-json", "structured-json", "dense-json"):
        return math.ceil(length / 3.5)
    else:
        return math.ceil(length / 4)


def validate_against_schema(output, schema_path, repo_root):
    """Basic schema validation — checks required fields exist."""
    full_path = os.path.join(repo_root, schema_path)
    if not os.path.isfile(full_path):
        return False, f"Schema file not found: {schema_path}"

    with open(full_path, "r", encoding="utf-8") as f:
        schema = json.load(f)

    required_fields = schema.get("required", [])

    if isinstance(output, dict):
        missing = [f for f in required_fields if f not in output]
        if missing:
            return False, f"Missing required fields: {missing}"
        return True, "Schema validation passed"
    elif isinstance(output, str):
        # For DSL schema, validate pattern
        if schema.get("type") == "string":
            import re
            pattern = schema.get("pattern", "")
            if pattern and not re.match(pattern, output):
                return False, f"DSL string does not match pattern: {pattern}"
            return True, "DSL pattern validation passed"

    return True, "Validation skipped (non-dict output)"


def run_test_with_api(test_case, skill_content, client, repo_root):
    """Run a single test case using the Anthropic API."""
    test_id = test_case.get("id", "unknown")
    description = test_case.get("description", "")
    test_input = test_case.get("input", "")
    expected_schema = test_case.get("expected_schema", "")
    expected_fields = test_case.get("expected_fields_present", [])

    # Build the prompt
    if isinstance(test_input, dict):
        input_str = json.dumps(test_input)
    else:
        input_str = str(test_input)

    prompt = f"""You are using the following Marlin skill. Apply it to the given input and return ONLY the compressed JSON output, nothing else.

SKILL:
{skill_content}

INPUT:
{input_str}

Return only the compressed JSON. No explanations, no markdown formatting, no code fences."""

    try:
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}],
        )

        response_text = message.content[0].text.strip()

        # Try to parse as JSON
        try:
            output = json.loads(response_text)
        except json.JSONDecodeError:
            output = response_text

        # Check expected fields
        if isinstance(output, dict) and expected_fields:
            missing = [f for f in expected_fields if f not in output]
            if missing:
                return "FAIL", f"Missing expected fields: {missing}"

        # Validate against schema
        if expected_schema:
            valid, msg = validate_against_schema(output, expected_schema, repo_root)
            if not valid:
                return "FAIL", msg

        return "PASS", "All checks passed"

    except Exception as e:
        return "FAIL", f"API error: {str(e)}"


def run_test_offline(test_case, repo_root):
    """Run basic offline validation of a test case (no API)."""
    test_id = test_case.get("id", "unknown")
    expected_schema = test_case.get("expected_schema", "")

    # Validate schema file exists
    if expected_schema:
        schema_path = os.path.join(repo_root, expected_schema)
        if not os.path.isfile(schema_path):
            return "FAIL", f"Schema file not found: {expected_schema}"

    # Validate test case structure
    required_test_fields = ["id", "description", "input", "mode"]
    missing = [f for f in required_test_fields if f not in test_case]
    if missing:
        return "FAIL", f"Test case missing fields: {missing}"

    return "PASS", "Offline validation passed (API test skipped)"


def main():
    # Ensure stdout can handle all characters on any platform
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # type: ignore
    parser = argparse.ArgumentParser(description="Run Marlin skill tests")
    parser.add_argument("--skill", help="Specific skill name to test")
    parser.add_argument("--all", action="store_true", help="Test all skills")
    parser.add_argument(
        "--offline",
        action="store_true",
        help="Run offline validation only (no API calls)",
    )

    args = parser.parse_args()

    if not args.skill and not args.all:
        parser.print_help()
        sys.exit(1)

    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    tests_root = os.path.join(repo_root, "tests", "skill-tests")
    skills_root = os.path.join(repo_root, "skills")

    # Set up API client if needed
    client = None
    if not args.offline:
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            print("WARNING: ANTHROPIC_API_KEY not set. Running in offline mode.")
            args.offline = True
        elif not HAS_ANTHROPIC:
            print("WARNING: 'anthropic' package not installed. Running in offline mode.")
            print("  Install with: pip install anthropic")
            args.offline = True
        else:
            client = anthropic.Anthropic(api_key=api_key)  # type: ignore

    # Determine which skills to test
    if args.all:
        test_files = sorted([
            f for f in os.listdir(tests_root)
            if f.endswith(".test.json")
        ])
        skill_names = [f.replace(".test.json", "") for f in test_files]
    else:
        skill_names = [args.skill]

    total_pass = 0
    total_fail = 0

    for skill_name in skill_names:
        test_file = os.path.join(tests_root, f"{skill_name}.test.json")
        skill_file = os.path.join(skills_root, skill_name, "SKILL.md")

        if not os.path.isfile(test_file):
            print(f"  [FAIL] {skill_name}: test file not found")
            total_fail += 1
            continue

        with open(test_file, "r", encoding="utf-8") as f:
            tests = json.load(f)

        skill_content = ""
        if os.path.isfile(skill_file):
            with open(skill_file, "r", encoding="utf-8") as f:
                skill_content = f.read()

        print(f"\n  Testing: {skill_name} ({len(tests)} tests)")
        print(f"  {'-' * 40}")

        for test_case in tests:
            test_id = test_case.get("id", "unknown")
            description = test_case.get("description", "")

            if args.offline:
                status, message = run_test_offline(test_case, repo_root)
            else:
                status, message = run_test_with_api(
                    test_case, skill_content, client, repo_root
                )

            icon = "[PASS]" if status == "PASS" else "[FAIL]"
            print(f"    {icon} {test_id}: {description}")
            if status == "FAIL":
                print(f"      -> {message}")
                total_fail += 1
            else:
                total_pass += 1

    print(f"\n{'═' * 50}")
    print(f"Total: {total_pass + total_fail} | Pass: {total_pass} | Fail: {total_fail}")
    mode = "offline" if args.offline else "API"
    print(f"Mode: {mode}")
    print(f"{'═' * 50}")

    sys.exit(1 if total_fail > 0 else 0)


if __name__ == "__main__":
    main()
