---
name: dsl-bridge
description: Convert between Marlin V3 internal DSL format (G:value|A:value) and external model-ready JSON. Use when the user types /marlin dsl or when agent-to-agent prompt passing requires ultra-compact internal format.
version: 1.0.0
author: adisingh-cs
project: marlin
phase: v3
category: bridge
tags: [dsl, bridge, v3, internal, external, conversion]
input_format: dsl
output_format: compact-json
token_impact: high
stability: experimental
trigger: "/marlin dsl"
---

# dsl-bridge

The DSL bridge converts between Marlin's V3 internal DSL format and the V3 external JSON format. The internal format is an ultra-compact pipe-delimited string designed for storage, version control, and agent-to-agent passing. The external format is a short-key JSON object that gets sent to LLMs. The bridge is bidirectional — it can parse DSL into JSON and serialize JSON into DSL.

**Critical rule:** Raw DSL strings are never sent directly to LLMs. The bridge always converts to external JSON before model consumption.

## When to trigger

- User types `/marlin dsl` to convert a prompt to V3 internal DSL format
- User provides a DSL string and asks to convert it to JSON for model use
- Called internally when V3 format is requested by another skill or agent pipeline
- Used for storing compressed prompts in version control or config files

## Do NOT trigger when

- User wants V1 compression (use structured, compact, dense, or domain modes)
- User wants to send raw DSL directly to an LLM (explain that bridge to JSON is required)

## V3 internal DSL syntax

### Format rules
- Fields separated by `|` (pipe)
- Key:value pairs using `:` (colon)
- Keys are uppercase single-letter or 2–3 letter codes: G, A, I, D, C, F, E
- Array values are comma-separated inline, no brackets
- No spaces anywhere in the DSL string
- Maximum length: 500 characters

### Field order (canonical)
`G` → `A` → `I` → `D` → `C` → `F` → `E`

Any extra fields are appended alphabetically after E.

### Escaping
- If a value contains `|`, wrap the entire value in double quotes: `G:"value|with|pipes"`
- If a value contains `:`, wrap the entire value in double quotes: `G:"key:value"`
- Double quotes within quoted values are escaped as `\"`

## Conversion: Internal DSL → External JSON

1. Split string on `|` (respecting quoted values)
2. For each segment, split on first `:` to get key and value
3. Map DSL keys to JSON short keys (G→g, A→a, I→i, D→d, C→c, F→f, E→e)
4. If value contains commas, convert to JSON array
5. If value has no commas, keep as scalar string
6. Build JSON object with proper types
7. Return valid JSON

## Conversion: External JSON → Internal DSL

1. Read JSON object
2. Map JSON keys to DSL codes (g→G, a→A, i→I, d→D, c→C, f→F, e→E)
3. For array values, join elements with commas (no spaces)
4. For null values, omit the field entirely
5. Serialize as `KEY:value|KEY:value` in canonical field order
6. Strip all spaces
7. Return DSL string

## Examples

### Example 1: Login API — bidirectional

**Internal DSL:**
```
G:build login api|A:create|I:email,password,token|D:auth|C:jwt-only|F:json
```

**External JSON:**
```json
{"g":"build login api","a":"create","i":["email","password","token"],"d":"auth","c":["jwt-only"],"f":"json"}
```

### Example 2: Data pipeline — bidirectional

**Internal DSL:**
```
G:process sales data|A:transform|I:sales-csv,revenue-col|D:data-pipeline|C:filter-nulls,sort-desc|F:parquet
```

**External JSON:**
```json
{"g":"process sales data","a":"transform","i":["sales-csv","revenue-col"],"d":"data-pipeline","c":["filter-nulls","sort-desc"],"f":"parquet"}
```

### Example 3: Agent task — bidirectional

**Internal DSL:**
```
G:research competitor pricing|A:analyze|I:web-search,doc-analysis|D:agent-task|C:dev-tools-only|F:report|E:stripe-pricing-page
```

**External JSON:**
```json
{"g":"research competitor pricing","a":"analyze","i":["web-search","doc-analysis"],"d":"agent-task","c":["dev-tools-only"],"f":"report","e":["stripe-pricing-page"]}
```

### Example 4: Escaped values — bidirectional

**Internal DSL:**
```
G:"parse key:value pairs"|A:create|I:config-file|D:data-pipeline|F:json
```

**External JSON:**
```json
{"g":"parse key:value pairs","a":"create","i":["config-file"],"d":"data-pipeline","f":"json"}
```

## When to use V3 DSL

| Use case | Recommended format |
|----------|-------------------|
| Storing prompts in git repos | Internal DSL |
| Agent-to-agent prompt passing | Internal DSL (bridge at consumption point) |
| Ultra-compact logging | Internal DSL |
| Sending to LLMs | External JSON (always bridge first) |
| Human review of compressed prompts | External JSON |
| Config files and environment variables | Internal DSL |

## Related Skills

- **key-shortener** — uses the same key maps for DSL key codes
- **marlin-compact** — compact JSON is structurally similar to V3 external JSON
- **output-formatter** — formats DSL bridge output per user's `--out` flag
- **token-estimator** — estimates token savings for DSL vs JSON representations
- **schema-normalizer** — validates external JSON against V3 schemas
