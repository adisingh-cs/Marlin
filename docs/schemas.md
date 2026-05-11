# Schemas

Marlin uses JSON Schema draft-07 files to document the structured outputs
described in the root `SKILL.md`. The current V1 implementation is a single
skill, so schemas are contracts for agent/model behavior rather than runtime
validators.

## Schema Inventory

| Schema | Path | Used by |
|---|---|---|
| Base prompt | `schemas/v1/base.schema.json` | swift, sharp, strike |
| Web API | `schemas/v1/web-api.schema.json` | sonar `--schema web-api` |
| Data pipeline | `schemas/v1/data-pipeline.schema.json` | sonar `--schema data-pipeline` |
| Agent task | `schemas/v1/agent-task.schema.json` | sonar `--schema agent-task` |
| V3 internal DSL | `schemas/v3/internal-dsl.schema.json` | DSL storage/transport |
| V3 external JSON | `schemas/v3/external-json.schema.json` | short-key JSON sent to models |

## Base Schema

The base schema is used by swift directly and by sharp/strike before key
shortening.

| Field | Type | Required | Default | Description |
|---|---|---:|---|---|
| goal | string, max 100 | Yes | - | Primary objective |
| action | string | Yes | - | Operation verb |
| inputs | array of strings | Yes | - | Parameters or data |
| domain | string or null | No | null | Context area |
| constraints | array of strings or null | No | null | Rules and limits |
| format | string | No | json | Desired output format |
| examples | array of strings or null | No | null | Reference samples |

## Domain Schemas

### Web API

Fields: `method`, `endpoint`, `auth`, `payload`, `headers`,
`response-format`, `version`, `middleware`.

Required: `method`, `endpoint`.

### Data Pipeline

Fields: `source`, `transform`, `sink`, `schedule`, `format`, `batch-size`,
`retry`, `schema-version`.

Required: `source`, `transform`, `sink`.

### Agent Task

Fields: `objective`, `tools`, `output-type`, `memory`, `constraints`,
`handoff`, `priority`, `context-window`.

Required: `objective`, `tools`, `output-type`.

## V3 Schemas

The internal DSL schema validates compact strings such as:

```text
G:build login api|A:create|I:email,password|D:auth|F:json
```

The external JSON schema validates short-key JSON objects such as:

```json
{"g":"build login api","a":"create","i":["email","password"],"d":"auth","f":"json"}
```

## Adding New Schemas

1. Create `schemas/v1/{domain}.schema.json`.
2. Follow JSON Schema draft-07.
3. Define required and optional fields.
4. Set `additionalProperties: false` unless the domain needs extension fields.
5. Create `schemas/key-maps/{domain}-keymap.json`.
6. Add the domain to the sonar section of root `SKILL.md`.
7. Add examples and benchmark prompts that exercise the new schema.
