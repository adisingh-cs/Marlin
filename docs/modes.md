# Compression Modes

Marlin exposes four user-facing modes from the single root `SKILL.md`.
Users select a mode explicitly with `/marlin <mode>`; Marlin does not
auto-select modes silently.

## Mode Comparison

| Mode | Trigger | Target Reduction | Best for |
|---|---|---:|---|
| Swift | `/marlin swift` | 20-35% | Readable structured prompts |
| Sharp | `/marlin sharp` | 35-50% | Compact JSON for repeated workflows |
| Strike | `/marlin strike` | 50-70% | Aggressive high-volume compression |
| Sonar | `/marlin sonar --schema <name>` | 40-65% | Domain-shaped prompts |

These percentages are design targets until the OpenRouter benchmark baseline is
run and committed.

## Swift

Swift normalizes a natural-language prompt into the base schema:
`goal`, `action`, `inputs`, `domain`, `constraints`, `format`, and `examples`.
It keeps full key names, fills missing optional fields with `null`, and defaults
`format` to `json` when no format is provided.

Example:

```json
{
  "goal": "build REST API for user management",
  "action": "create",
  "inputs": ["users"],
  "domain": "web-api",
  "constraints": ["CRUD endpoints", "Express.js"],
  "format": "json",
  "examples": null
}
```

## Sharp

Sharp runs the swift normalization first, then applies the base key map and
minifies JSON. Null and empty fields are dropped.

Example:

```json
{"g":"create React user profile component","a":"create","i":["avatar","bio"],"d":"frontend","f":"jsx"}
```

## Strike

Strike runs sharp first, then applies the value abbreviation table from
`SKILL.md`. It also collapses single-item arrays to strings and serializes
multi-item arrays as comma-separated strings when that saves tokens.

Example:

```json
{"g":"impl auth mw for JWT val","a":"create","i":"jwt-token","d":"auth","c":"val-against-db","f":"json"}
```

## Sonar

Sonar applies a domain-specific schema and key map. The current schemas are:

- `web-api`: method, endpoint, auth, payload, headers, response-format, version,
  middleware.
- `data-pipeline`: source, transform, sink, schedule, format, batch-size, retry,
  schema-version.
- `agent-task`: objective, tools, memory, output-type, constraints, handoff,
  priority, context-window.

Example:

```json
{"m":"POST","ep":"/api/users","au":"jwt","mw":["rate-limit"],"rf":"json"}
```

## V3 DSL Bridge

Append `--dsl` to mode commands to output the internal DSL format:

```text
G:build login api|A:create|I:email,password|D:auth|F:json
```

Bridge DSL back to JSON before sending it to a model:

```text
/marlin bridge G:build login api|A:create|I:email,password|D:auth|F:json
```

Raw DSL is intended for storage and agent-to-agent transport, not direct model
consumption.
