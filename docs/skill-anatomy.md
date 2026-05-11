# Skill Anatomy

Marlin V1 is distributed as a single root `SKILL.md`. That file contains the
metadata, mode descriptions, transformation rules, examples, V3 DSL rules, and
quick reference used by supported agents.

## Frontmatter

The root skill starts with YAML frontmatter:

```yaml
---
name: marlin
description: Compress and restructure input prompts into lean schema-anchored representations for any AI model.
license: MIT
metadata:
  author: adisingh-cs
  github: https://github.com/adisingh-cs/Marlin
  version: "1.0.0"
---
```

Keep this metadata aligned with `skills_index.json`, `CATALOG.md`, and release
notes.

## Required Body Sections

`SKILL.md` should cover:

- Mode table for `/marlin swift`, `/marlin sharp`, `/marlin strike`, and
  `/marlin sonar`.
- Output flags: `--prompt`, `--report`, `--diff`, `--all`, and `--dsl`.
- Per-mode pipeline rules.
- Base key map and domain key maps.
- Strike value abbreviation table.
- Sonar schemas for `web-api`, `data-pipeline`, and `agent-task`.
- V3 DSL format and bridge instructions.
- Complete examples with token-savings estimates.

## Contribution Checklist

When editing the skill:

1. Keep command names consistent across `SKILL.md`, `README.md`, agent rule
   files, and `CATALOG.md`.
2. Use abbreviations that exist in `schemas/key-maps/*.json`.
3. Add or update examples when behavior changes.
4. Run the benchmark/unit tests before publishing.
5. Do not claim benchmark-backed savings until `benchmarks/results/` contains a
   real run for the stated model and methodology.
