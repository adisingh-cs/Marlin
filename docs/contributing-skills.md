# Contributing Skills

This guide covers how to design, write, test, and submit a new Marlin skill. If you have not read [CONTRIBUTING.md](../CONTRIBUTING.md), start there for general contribution guidelines. This document goes deeper into skill-specific best practices.

## Before you build

### 1. Check for existing coverage

Before writing a new skill, check:
- Does an existing mode or skill already handle this use case?
- Would your use case be better served by a new domain schema rather than a new skill?
- Can the existing intent-parser alias table be extended to cover your case?

### 2. Identify the skill's role in the pipeline

Every skill must fit into Marlin's pipeline architecture. Ask:
- Is this a user-facing mode skill (like marlin-compact) or an internal pipeline skill (like key-shortener)?
- Where does it sit in the pipeline? After which skill? Before which skill?
- What does it receive as input? What does it produce as output?
- Which schema validates its output?

### 3. Choose the right category

| Category | When to use |
|----------|-------------|
| compression | User-facing mode skills that orchestrate a compression pipeline |
| parsing | Skills that extract structure from unstructured input |
| schema | Skills that enforce schema contracts and normalize data |
| encoding | Skills that transform keys or values for compactness |
| formatting | Skills that control how output is presented to the user |
| estimation | Skills that measure or estimate properties (like token count) |
| bridge | Skills that convert between formats (like DSL ↔ JSON) |

## Writing the SKILL.md

### Start with the frontmatter

Use the template at `.github/SKILL_TEMPLATE.md`. Fill every field. Common mistakes:
- Setting `name` to something different from the folder name
- Using a `category` value that does not match the enum list
- Forgetting to set `trigger` to `internal` for non-user-facing skills

### Write the description

One paragraph, 2–4 sentences. Answer:
1. What does this skill do? (transformation it performs)
2. What does it take as input? (format and content)
3. What does it produce as output? (format and content)

Bad: "This skill helps with compression."
Good: "The value encoder applies abbreviation to string values within a key-shortened JSON object. It replaces common technical terms with standardized short codes, collapses single-item arrays to scalars, and inlines multi-value arrays as comma-separated strings."

### Define trigger conditions precisely

For user-facing skills:
- List exact commands (e.g., `/marlin compact`)
- List keyword triggers (e.g., "minify my prompt")
- List implicit triggers (e.g., "default when no mode specified")

For internal skills:
- Set trigger to `internal`
- Document which skills call this one and when

### Write meaningful examples

Requirements:
- At least 2 complete input/output pairs (3 is better)
- Use realistic developer prompts
- Cover different prompt types (API, data, frontend, infrastructure)
- For mode skills, include token count comparisons
- Show edge cases if relevant

Bad example input: "Do something with data"
Good example input: "Build a REST API endpoint that handles user authentication using JWT tokens. The endpoint should accept email and password as inputs."

### Document related skills

For every skill this one interacts with, explain the relationship. This creates a navigable skill graph and helps users understand the full pipeline.

## Writing test fixtures

### Test file location
`tests/skill-tests/{skill-name}.test.json`

### Test object format
```json
{
  "id": "test-001",
  "description": "what this test validates",
  "input": "raw input string or object",
  "mode": "structured|compact|dense|domain|internal",
  "expected_schema": "schemas/v1/base.schema.json",
  "expected_fields_present": ["goal", "action", "inputs"],
  "expected_reduction_min_pct": 20
}
```

### Test design guidelines
- Test the happy path first (clear, well-formed input)
- Test edge cases (vague input, missing fields, unusual formatting)
- Test boundary conditions (very short prompts, very long prompts)
- Set realistic `expected_reduction_min_pct` — do not over-promise
- Each test should validate a specific behavior, not everything at once

### Minimum: 3 tests per skill

## Choosing a trigger phrase

Good triggers:
- Are short and memorable
- Follow the `/marlin <mode>` convention for user-facing skills
- Do not conflict with existing triggers
- Are descriptive of what happens

Bad triggers: `/compress`, `/do-thing`, `/marlin magic`

## Submitting your skill

1. Fork the repository
2. Create a branch: `skill/{your-skill-name}`
3. Add your SKILL.md in `skills/{your-skill-name}/`
4. Add your test file in `tests/skill-tests/{your-skill-name}.test.json`
5. Run `python tools/validate-skills.py` — all must pass
6. Run `python tools/generate-catalog.py` — commit the updated catalog
7. Open a PR using the template
8. Address review feedback

## Review criteria

Maintainers evaluate skill contributions on:
1. **Necessity** — does this fill a real gap?
2. **Quality** — is the SKILL.md complete and well-written?
3. **Fit** — does it integrate cleanly into the existing pipeline?
4. **Testing** — are the test fixtures meaningful and comprehensive?
5. **Documentation** — are examples realistic and edge cases documented?
