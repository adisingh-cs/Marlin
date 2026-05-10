# Schemas

Marlin uses JSON Schema (draft-07) to anchor every stage of the compression pipeline. Schemas define the contract between skills — ensuring that output from one skill is valid input for the next.

## Schema inventory

| Schema | Path | Used by |
|--------|------|---------|
| Base prompt | `schemas/v1/base.schema.json` | structured, compact, dense modes |
| Web API | `schemas/v1/web-api.schema.json` | domain mode (--schema web-api) |
| Data pipeline | `schemas/v1/data-pipeline.schema.json` | domain mode (--schema data-pipeline) |
| Agent task | `schemas/v1/agent-task.schema.json` | domain mode (--schema agent-task) |
| V3 internal DSL | `schemas/v3/internal-dsl.schema.json` | dsl-bridge |
| V3 external JSON | `schemas/v3/external-json.schema.json` | dsl-bridge, compact output validation |

## Base schema

The foundational schema used by structured, compact, and dense modes.

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| goal | string (max 100) | Yes | — | Primary objective |
| action | string | Yes | — | Operation verb |
| inputs | array of strings | Yes | — | Parameters or data |
| domain | string or null | No | null | Context area |
| constraints | array of strings or null | No | null | Rules and limits |
| format | string | No | "json" | Desired output format |
| examples | array of strings or null | No | null | Reference samples |

No additional properties allowed.

## Web API schema

Specialized for REST/GraphQL API prompts.

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| method | enum: GET, POST, PUT, DELETE, PATCH | Yes | — | HTTP method |
| endpoint | string | Yes | — | API path or URL |
| auth | string or null | No | null | Auth mechanism |
| payload | array of strings or null | No | null | Request fields |
| headers | array of strings or null | No | null | Required headers |
| response-format | string | No | "json" | Response format |
| version | string or null | No | null | API version |
| middleware | array of strings or null | No | null | Middleware layers |

## Data pipeline schema

Specialized for ETL and data processing prompts.

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| source | string | Yes | — | Data source |
| transform | array of strings | Yes | — | Transformation steps |
| sink | string | Yes | — | Data destination |
| schedule | string or null | No | null | Execution schedule |
| format | string or null | No | null | Data format |
| batch-size | integer or null | No | null | Records per batch |
| retry | integer or null | No | 3 | Retry attempts |
| schema-version | string or null | No | null | Data schema version |

## Agent task schema

Specialized for AI agent task definitions.

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| objective | string | Yes | — | Agent's primary goal |
| tools | array of strings | Yes | — | Available tools |
| output-type | string | Yes | — | Expected output type |
| memory | string or null | No | null | Memory mode |
| constraints | array of strings or null | No | null | Boundaries |
| handoff | string or null | No | null | Handoff target |
| priority | enum: low, medium, high, critical, null | No | null | Task priority |
| context-window | integer or null | No | null | Max context tokens |

## V3 schemas

### Internal DSL schema
- Type: string
- Pattern: `^([A-Z]{1,3}:[^|]+)(\\|[A-Z]{1,3}:[^|]+)*$`
- Max length: 500 characters
- No spaces allowed

### External JSON schema
- Same semantic fields as base schema but with short keys (g, a, i, d, c, f, e)
- Required: g, a, i
- Allows additional properties (for domain-specific fields)

## How schemas flow through the pipeline

```
Natural language input
        │
        ▼
  [No schema — raw text]
        │
   intent-parser
        │
        ▼
  [Partial base schema — nulls allowed]
        │
   schema-normalizer
        │
        ▼
  [Full base schema — types enforced, defaults applied]
        │
   key-shortener
        │
        ▼
  [V3 external JSON schema — short keys]
        │
   value-encoder (dense only)
        │
        ▼
  [V3 external JSON schema — short keys + abbreviated values]
```

## Adding new schemas

1. Create the schema file at `schemas/v1/{domain}.schema.json`
2. Follow JSON Schema draft-07 format
3. Define required and optional fields
4. Set `additionalProperties: false`
5. Create a corresponding key map at `schemas/key-maps/{domain}-keymap.json`
6. Add domain support to the `marlin-domain` skill
