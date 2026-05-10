#!/usr/bin/env python3
"""
validate-skills.py — Validates all Marlin SKILL.md files against required structure.

Checks:
1. SKILL.md exists in each skills/ subdirectory
2. Frontmatter is valid YAML
3. All required frontmatter fields are present
4. Field values match allowed enums
5. 'name' field matches folder name exactly
6. Examples section exists in body
7. Related Skills section exists
8. Corresponding test file exists in tests/skill-tests/

Usage:
    python tools/validate-skills.py

Exit code 0 if all skills pass, 1 if any fail.
"""

import os
import sys
import re
import json

# Required frontmatter fields and their allowed values
REQUIRED_FIELDS = {
    "name": None,  # Must match folder name
    "version": None,  # Any semver string
    "author": None,  # Any string
    "project": ["marlin"],
    "phase": ["v1", "v3"],
    "category": [
        "compression", "parsing", "schema", "encoding",
        "formatting", "estimation", "bridge"
    ],
    "tags": None,  # Must be a list
    "input_format": ["natural-language", "json", "compact-json", "dsl"],
    "output_format": [
        "structured-json", "compact-json", "dense-json",
        "dsl", "report", "diff"
    ],
    "token_impact": ["high", "medium", "low", "none"],
    "stability": ["stable", "experimental"],
    "trigger": None,  # Any string
}

REQUIRED_BODY_SECTIONS = ["Examples", "Related Skills"]


def parse_frontmatter(content):
    """Extract YAML frontmatter from a SKILL.md file."""
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n", content, re.DOTALL)
    if not match:
        return None, "No valid YAML frontmatter found (must start with --- and end with ---)"

    frontmatter_text = match.group(1)
    frontmatter = {}

    for line in frontmatter_text.strip().split("\n"):
        line = line.strip()
        if not line or line.startswith("#"):
            continue

        colon_idx = line.find(":")
        if colon_idx == -1:
            continue

        key = line[:colon_idx].strip()
        value = line[colon_idx + 1:].strip()

        # Handle YAML arrays: [item1, item2, item3]
        if value.startswith("[") and value.endswith("]"):
            items = value[1:-1].split(",")
            frontmatter[key] = [item.strip().strip("'\"") for item in items if item.strip()]
        elif value.startswith('"') and value.endswith('"'):
            frontmatter[key] = value[1:-1]
        elif value.startswith("'") and value.endswith("'"):
            frontmatter[key] = value[1:-1]
        else:
            frontmatter[key] = value

    return frontmatter, None


def validate_skill(skill_dir, skill_name, skills_root, tests_root):
    """Validate a single skill. Returns list of error strings."""
    errors = []

    # Check 1: SKILL.md exists
    skill_path = os.path.join(skill_dir, "SKILL.md")
    if not os.path.isfile(skill_path):
        errors.append("SKILL.md file not found")
        return errors

    # Read content
    with open(skill_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Check 2: Frontmatter is valid YAML
    frontmatter, parse_error = parse_frontmatter(content)
    if parse_error:
        errors.append(f"Frontmatter parse error: {parse_error}")
        return errors

    # Check 3: All required frontmatter fields present
    for field in REQUIRED_FIELDS:
        if field not in frontmatter:
            errors.append(f"Missing required field: {field}")

    # Check 4: Field values match allowed enums
    for field, allowed in REQUIRED_FIELDS.items():
        if field not in frontmatter or allowed is None:
            continue
        value = frontmatter[field]
        if isinstance(value, list):
            for item in value:
                if item not in allowed:
                    errors.append(f"Field '{field}': invalid value '{item}' (allowed: {allowed})")
        elif value not in allowed:
            errors.append(f"Field '{field}': invalid value '{value}' (allowed: {allowed})")

    # Check 5: 'name' field matches folder name
    if "name" in frontmatter and frontmatter["name"] != skill_name:
        errors.append(
            f"Field 'name' is '{frontmatter['name']}' but folder is '{skill_name}' — must match"
        )

    # Check 6: 'tags' field must be a list
    if "tags" in frontmatter and not isinstance(frontmatter["tags"], list):
        errors.append("Field 'tags' must be an array")

    # Check 7: Examples section exists in body
    body = content.split("---", 2)[-1] if content.count("---") >= 2 else content
    for section in REQUIRED_BODY_SECTIONS:
        # Match ## Examples or ### Examples etc.
        pattern = rf"^#{{1,4}}\s+{re.escape(section)}"
        if not re.search(pattern, body, re.MULTILINE | re.IGNORECASE):
            errors.append(f"Missing required section: '{section}'")

    # Check 8: Corresponding test file exists
    test_file = os.path.join(tests_root, f"{skill_name}.test.json")
    if not os.path.isfile(test_file):
        errors.append(f"Missing test file: tests/skill-tests/{skill_name}.test.json")
    else:
        # Validate test file is valid JSON with at least 3 tests
        try:
            with open(test_file, "r", encoding="utf-8") as tf:
                tests = json.load(tf)
            if not isinstance(tests, list):
                errors.append(f"Test file must be a JSON array")
            elif len(tests) < 3:
                errors.append(f"Test file has {len(tests)} tests, minimum is 3")
        except json.JSONDecodeError as e:
            errors.append(f"Test file is not valid JSON: {e}")

    return errors


def main():
    # Determine paths relative to script location
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    skills_root = os.path.join(repo_root, "skills")
    tests_root = os.path.join(repo_root, "tests", "skill-tests")

    if not os.path.isdir(skills_root):
        print("ERROR: skills/ directory not found")
        sys.exit(1)

    # Find all skill directories
    skill_dirs = sorted([
        d for d in os.listdir(skills_root)
        if os.path.isdir(os.path.join(skills_root, d)) and not d.startswith(".")
    ])

    if not skill_dirs:
        print("ERROR: No skill directories found in skills/")
        sys.exit(1)

    print(f"Validating {len(skill_dirs)} skills...\n")

    total_pass = 0
    total_fail = 0
    all_results = []

    for skill_name in skill_dirs:
        skill_dir = os.path.join(skills_root, skill_name)
        errors = validate_skill(skill_dir, skill_name, skills_root, tests_root)

        if errors:
            status = "FAIL"
            total_fail += 1
        else:
            status = "PASS"
            total_pass += 1

        all_results.append((skill_name, status, errors))

    # Print results
    max_name_len = max(len(name) for name, _, _ in all_results)

    for skill_name, status, errors in all_results:
        icon = "✓" if status == "PASS" else "✗"
        print(f"  {icon} {skill_name:<{max_name_len}}  {status}")
        if errors:
            for error in errors:
                print(f"    └─ {error}")

    print(f"\n{'─' * 50}")
    print(f"Total: {len(skill_dirs)} | Pass: {total_pass} | Fail: {total_fail}")
    print(f"{'─' * 50}")

    sys.exit(1 if total_fail > 0 else 0)


if __name__ == "__main__":
    main()
