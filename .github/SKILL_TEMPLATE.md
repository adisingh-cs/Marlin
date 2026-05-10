<!-- Copy this file to skills/{your-skill-name}/SKILL.md and fill in every section. Do not leave placeholders. -->
<!-- Your skill folder name must match the 'name' field below exactly (kebab-case). -->
<!-- See docs/skill-anatomy.md for detailed guidance on each section. -->

---
name: your-skill-name
version: 1.0.0
author: your-github-username
project: marlin
phase: v1
category: compression
tags: [tag1, tag2, tag3]
input_format: natural-language
output_format: structured-json
token_impact: medium
stability: experimental
trigger: "/marlin your-command"
---

# your-skill-name

A clear, concise description of what this skill does. One paragraph, 2-4 sentences. Explain the transformation it performs, what input it expects, and what output it produces.

## When to trigger

- List the exact conditions under which this skill should activate
- Include trigger commands, keywords, and implicit invocation rules
- Be specific — ambiguity leads to incorrect triggering

## Do NOT trigger when

- List exclusion conditions
- When should this skill NOT run, even if the input looks related?
- What other skills should handle those cases instead?

## Pipeline steps

1. **Step name** — describe what this step does
2. **Step name** — describe what this step does
3. **Step name** — describe what this step does

## Examples

### Example 1: Descriptive title

**Input:**
```
Your raw input here — use realistic developer prompts
```

**Output:**
```json
{
  "your": "compressed output here"
}
```

### Example 2: Descriptive title

**Input:**
```
Another realistic input prompt
```

**Output:**
```json
{
  "another": "compressed output"
}
```

## Related Skills

- **skill-name** — how this skill relates to it
- **skill-name** — how this skill relates to it
