# Skill Anatomy

Every Marlin skill is defined by a single `SKILL.md` file inside a named folder under `skills/`. This guide explains every section of a SKILL.md and uses `marlin-compact` as a living example throughout.

## File location

```
skills/
└── your-skill-name/
    └── SKILL.md
```

The folder name must be kebab-case and must exactly match the `name` field in the SKILL.md frontmatter.

## Frontmatter

The YAML frontmatter block is enclosed by `---` markers and contains all metadata about the skill.

```yaml
---
name: marlin-compact
version: 1.0.0
author: adisingh-cs
project: marlin
phase: v1
category: compression
tags: [compact, minify, short-keys, api-ready]
input_format: natural-language
output_format: compact-json
token_impact: high
stability: stable
trigger: "/marlin compact"
---
```

### Field reference

| Field | Required | Type | Description |
|-------|----------|------|-------------|
| `name` | Yes | string | Skill identifier. Must match folder name exactly. Kebab-case. |
| `version` | Yes | string | Semantic version (e.g., `1.0.0`). Increment on updates. |
| `author` | Yes | string | GitHub username of the skill author. |
| `project` | Yes | string | Always `marlin` for skills in this repo. |
| `phase` | Yes | enum | `v1` (current) or `v3` (DSL-related features). |
| `category` | Yes | enum | One of: `compression`, `parsing`, `schema`, `encoding`, `formatting`, `estimation`, `bridge`. |
| `tags` | Yes | array | Descriptive tags for search and discovery. |
| `input_format` | Yes | enum | What the skill accepts: `natural-language`, `json`, `compact-json`, `dsl`. |
| `output_format` | Yes | enum | What the skill produces: `structured-json`, `compact-json`, `dense-json`, `dsl`, `report`, `diff`. |
| `token_impact` | Yes | enum | How much this skill affects token count: `high`, `medium`, `low`, `none`. |
| `stability` | Yes | enum | `stable` (production-ready) or `experimental` (may change). |
| `trigger` | Yes | string | User-facing command (e.g., `/marlin compact`) or `internal` for pipeline-only skills. |

## Required body sections

### Title and description

The first heading (`# skill-name`) should match the skill name. Follow with a clear 2–4 sentence description of what the skill does, what transformation it performs, and what output it produces.

### When to trigger

List the exact conditions under which this skill activates. Be specific:
- User commands that invoke it
- Keywords or phrases that match
- Implicit invocation rules (e.g., "default mode when no mode specified")

### Do NOT trigger when

List exclusion conditions. This prevents incorrect activation and helps users understand skill boundaries.

### Pipeline steps

Numbered list of transformation steps the skill performs. Each step should reference which internal skill is called (if any) and what data flows between steps.

### Examples

At least 2 complete input/output pairs. Requirements:
- Use realistic developer prompts (no lorem ipsum)
- Show the full transformation from raw input to compressed output
- For mode skills, include a report block showing token savings
- Cover different types of prompts to demonstrate breadth

### Related Skills

List every skill this one interacts with and explain the relationship:
- Which skills it calls
- Which skills call it
- Which skills handle adjacent use cases

## Optional sections

- **Key map reference** — for encoding skills, show the complete key map table
- **Value abbreviation table** — for value-encoder, list all abbreviations
- **Schema reference** — for mode skills, show the schema fields used
- **Handling edge cases** — document how the skill handles unusual input

## Validation

Run `python tools/validate-skills.py` to check your SKILL.md against all requirements. The validator checks:
- Frontmatter exists and parses correctly
- All required fields are present
- Field values match allowed enums
- `name` matches folder name
- Examples section exists
- Related Skills section exists
- Corresponding test file exists

## Test fixtures

Every skill must have a corresponding test file at `tests/skill-tests/{skill-name}.test.json` with at least 3 test cases. See `tests/README.md` for the test object format.
