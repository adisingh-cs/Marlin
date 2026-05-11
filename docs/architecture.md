# Architecture

Marlin V1 is a single-skill prompt compression system. The root `SKILL.md`
contains the behavior for all user-facing modes: `swift`, `sharp`, `strike`,
and `sonar`. Supporting files in `schemas/`, `schemas/key-maps/`, and
`examples/` document the contracts that the skill asks an agent or model to
apply.

## System Overview

```text
user prompt
  -> mode selection (/marlin swift|sharp|strike|sonar)
  -> root SKILL.md instructions
  -> schema/key-map guided transformation
  -> compressed JSON or DSL output
```

Marlin currently relies on the host agent or benchmark model to perform the
compression described in `SKILL.md`. A deterministic offline compressor is a V2
roadmap item.

## Mode Pipelines

```text
swift  -> extract intent -> normalize to base schema
sharp  -> swift -> apply base key map -> minify JSON -> drop nulls
strike -> sharp -> abbreviate values -> collapse arrays where useful
sonar  -> apply selected domain schema -> apply selected domain key map
```

## Schemas

Schemas define the intended data contracts:

| Schema | Path | Used by |
|---|---|---|
| Base prompt | `schemas/v1/base.schema.json` | swift, sharp, strike |
| Web API | `schemas/v1/web-api.schema.json` | sonar `--schema web-api` |
| Data pipeline | `schemas/v1/data-pipeline.schema.json` | sonar `--schema data-pipeline` |
| Agent task | `schemas/v1/agent-task.schema.json` | sonar `--schema agent-task` |
| V3 external JSON | `schemas/v3/external-json.schema.json` | short-key JSON |
| V3 internal DSL | `schemas/v3/internal-dsl.schema.json` | DSL storage/transport |

## Key Maps

Key maps are JSON contracts for compact field names:

- `schemas/key-maps/base-keymap.json`: shared short keys.
- `schemas/key-maps/web-api-keymap.json`: web API fields.
- `schemas/key-maps/data-pipeline-keymap.json`: data pipeline fields.
- `schemas/key-maps/agent-task-keymap.json`: agent task fields.

The skill should only use abbreviations present in these maps. Unknown fields
should remain readable unless a future key map defines them.

## Benchmark Harness

`benchmarks/run.py` exercises the root `SKILL.md` through OpenRouter's
chat-completions API. It accepts an API key and model from CLI flags or
environment variables, runs the benchmark prompt corpus across Marlin modes,
and writes a JSON result file.

The harness records:

- original heuristic token count
- compressed heuristic token count
- absolute token savings
- percent savings
- mode and prompt source
- estimated compression-system overhead from the injected `SKILL.md`
- provider-reported token usage when OpenRouter returns it

The heuristic counter is useful for quick comparisons, but model-specific
tokenizer support is still needed for claim-grade measurements.
