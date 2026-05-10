---
name: schema-normalizer
description: Map a parsed intent object to the canonical Marlin base schema, enforcing field types and defaults. Use internally after intent-parser and before any compression skill.
version: 1.0.0
author: adisingh-cs
project: marlin
phase: v1
category: schema
tags: [schema, normalize, validate, types, defaults]
input_format: json
output_format: structured-json
token_impact: low
stability: stable
trigger: internal
---

# schema-normalizer

The schema normalizer takes the partial intent object produced by the intent-parser and maps it to a canonical schema. It enforces field types, applies default values, coerces mistyped values where safe, and validates the result against the target JSON Schema. This skill ensures that every Marlin output is schema-compliant regardless of how messy the original input was.

## When to trigger

- Called internally by all four mode skills, immediately after intent-parser
- Receives the partial intent object and the target schema reference
- Never invoked directly by the user

## Do NOT trigger when

- Input is already schema-valid (skip normalization, pass through)
- No intent object is available (intent-parser must run first)

## Schema field rules (base schema)

| Field | Type | Required | Default | Coercion rules |
|-------|------|----------|---------|----------------|
| goal | string | yes | — | Truncate to 100 chars if longer |
| action | string | yes | — | Lowercase, trim whitespace |
| inputs | array of strings | yes | — | If scalar string, wrap in single-item array |
| domain | string or null | no | null | Lowercase, trim whitespace |
| constraints | array of strings or null | no | null | If scalar string, wrap in single-item array |
| format | string | no | "json" | Lowercase, trim whitespace |
| examples | array of strings or null | no | null | If scalar string, wrap in single-item array |

## Pipeline steps

1. **Receive intent object and schema reference** — determine which schema to validate against (base, web-api, data-pipeline, or agent-task)
2. **Enforce required fields** — check that all required fields are present and non-null; if missing, flag but do not error (let downstream handle)
3. **Apply type coercion** — convert scalar strings to single-item arrays where schema expects arrays; trim whitespace from all string values; lowercase action, domain, and format fields
4. **Apply defaults** — set format to "json" if missing; set optional nullable fields to null if absent
5. **Validate against schema** — run JSON Schema draft-07 validation; collect any violations
6. **Return clean object** — output the normalized, schema-compliant intent object

## Handling domain schemas

When called from domain mode, the normalizer loads the domain-specific schema instead of the base schema. Domain schemas have different required fields:

- **web-api:** required = method, endpoint
- **data-pipeline:** required = source, transform, sink
- **agent-task:** required = objective, tools, output-type

The normalizer maps intent-parser output fields to domain fields using this bridge:

| Intent field | web-api field | data-pipeline field | agent-task field |
|-------------|--------------|-------------------|-----------------|
| goal | (endpoint context) | (source context) | objective |
| action | method | (transform context) | (inferred) |
| inputs | payload | (source/transform) | tools |
| constraints | middleware, auth | retry, schedule | constraints |

## Examples

### Example 1: Clean input — minimal coercion

**Input (from intent-parser):**
```json
{
  "goal": "build REST API for user management",
  "action": "create",
  "inputs": ["users", "roles", "permissions"],
  "domain": "web-api",
  "constraints": ["jwt-auth", "rate-limiting"],
  "format": "json",
  "examples": null
}
```

**Output (normalized):**
```json
{
  "goal": "build REST API for user management",
  "action": "create",
  "inputs": ["users", "roles", "permissions"],
  "domain": "web-api",
  "constraints": ["jwt-auth", "rate-limiting"],
  "format": "json",
  "examples": null
}
```

*No changes needed — input was already schema-compliant.*

### Example 2: Type coercion needed

**Input (from intent-parser):**
```json
{
  "goal": "  Write a Python script to process CSV data  ",
  "action": "  Write  ",
  "inputs": "csv-file",
  "domain": "Data Pipeline",
  "constraints": "filter-nulls",
  "format": null,
  "examples": "pandas example"
}
```

**Output (normalized):**
```json
{
  "goal": "Write a Python script to process CSV data",
  "action": "write",
  "inputs": ["csv-file"],
  "domain": "data pipeline",
  "constraints": ["filter-nulls"],
  "format": "json",
  "examples": ["pandas example"]
}
```

*Coercions applied: whitespace trimmed, scalars wrapped in arrays, defaults set, casing normalized.*

### Example 3: Missing optional fields

**Input (from intent-parser):**
```json
{
  "goal": "deploy Docker container",
  "action": "deploy",
  "inputs": ["docker-image", "config"],
  "domain": null,
  "constraints": null,
  "format": null,
  "examples": null
}
```

**Output (normalized):**
```json
{
  "goal": "deploy Docker container",
  "action": "deploy",
  "inputs": ["docker-image", "config"],
  "domain": null,
  "constraints": null,
  "format": "json",
  "examples": null
}
```

*Default "json" applied to format. Nulls preserved for optional fields.*

## Related Skills

- **intent-parser** — produces the partial intent object that this skill normalizes
- **key-shortener** — next step after normalization in compact/dense pipelines
- **marlin-structured** — calls schema-normalizer as step 3
- **marlin-domain** — calls schema-normalizer with domain-specific schema
- **output-formatter** — receives the normalized object for final formatting
