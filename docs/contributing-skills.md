# Contributing Skill Changes

Marlin currently ships as one root `SKILL.md`, not as multiple internal skill
folders. Contributions should improve that root skill, add schemas/key maps, or
improve benchmark evidence.

## Before You Change The Skill

Check whether the change belongs in:

- `SKILL.md` for user-facing behavior.
- `schemas/v1/*.schema.json` for a new or changed domain contract.
- `schemas/key-maps/*.json` for new key abbreviations.
- `examples/` for golden input/output examples.
- `benchmarks/` for measurement methodology or prompt coverage.

## Mode Changes

User-facing modes are:

- `/marlin swift`
- `/marlin sharp`
- `/marlin strike`
- `/marlin sonar --schema web-api|data-pipeline|agent-task`

Keep these names consistent across README, docs, catalog, agent rule files, and
benchmark defaults.

## Adding A Domain Schema

1. Add `schemas/v1/{domain}.schema.json`.
2. Add `schemas/key-maps/{domain}-keymap.json`.
3. Add the schema to the sonar section of `SKILL.md`.
4. Add example input/output files under `examples/domain/`.
5. Add benchmark prompts or mode coverage if the domain changes expected
   savings.

## Benchmark Evidence

Use the OpenRouter-compatible harness:

```bash
export OPENROUTER_API_KEY="sk-or-..."
python benchmarks/run.py --model "openai/gpt-4o-mini"
```

For published claims, include:

- OpenRouter model id.
- Prompt corpus.
- Mode list.
- Original and compressed token counts.
- Absolute and percent savings.
- Compression-system overhead.
- Any limitations of heuristic token counting.
