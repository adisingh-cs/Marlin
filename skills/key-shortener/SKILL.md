---
name: key-shortener
description: Replace verbose JSON keys with short single-letter abbreviations using the Marlin key map. Use internally in compact and dense compression modes.
version: 1.0.0
author: adisingh-cs
project: marlin
phase: v1
category: encoding
tags: [keys, abbreviation, minify, keymap]
input_format: json
output_format: compact-json
token_impact: medium
stability: stable
trigger: internal
---

# key-shortener

The key shortener replaces verbose JSON key names with single-letter or two-letter abbreviations using a predefined key map. It is the core differentiator between structured and compact modes. The skill loads the appropriate key map (base or domain-specific), walks every key in the input object, and replaces it if a mapping exists. Keys not found in the map pass through unchanged — the skill never invents abbreviations.

## When to trigger

- Called internally by compact, dense, and domain mode skills
- Never invoked directly by the user
- Always runs after schema-normalizer, before output-formatter

## Do NOT trigger when

- Running in structured mode (structured mode retains full key names)
- Input is already using short keys (prevent double-shortening)

## Hard rules

1. **Only use keys defined in the loaded keymap** — never invent or guess abbreviations
2. **Keys not in the map pass through unchanged** — unknown keys are preserved as-is
3. **Key maps are loaded from `schemas/key-maps/`** — base-keymap.json is the default
4. **Domain key maps extend the base** — they include all base mappings plus domain-specific ones
5. **On conflict between base and domain map, domain wins** — domain maps are authoritative
6. **Nested objects are walked recursively** — key shortening applies at all depth levels

## Key map reference (base)

| Full key | Short key | Notes |
|----------|-----------|-------|
| goal | g | Primary objective |
| action | a | Operation verb |
| inputs | i | Parameters/data |
| domain | d | Context area |
| constraints | c | Rules/limits |
| format | f | Output format |
| examples | e | Reference samples |
| output | o | Output specification |
| context | ctx | Context information |
| type | t | Type identifier |
| method | m | HTTP method or operation type |
| auth | au | Authentication mechanism |
| schema | sc | Schema reference |
| version | v | Version identifier |
| endpoint | ep | API endpoint |
| payload | pl | Request payload |
| response | rs | Response specification |
| headers | hd | HTTP headers |
| middleware | mw | Middleware layers |
| priority | pr | Priority level |
| objective | obj | Agent objective |
| tools | tl | Available tools |
| memory | mem | Memory/state mode |
| handoff | hf | Handoff target |
| source | src | Data source |
| transform | tr | Transformation steps |
| sink | sk | Data destination |
| schedule | sched | Execution schedule |
| batch-size | bs | Batch size |
| retry | rt | Retry count |

## Pipeline steps

1. **Determine which keymap to load** — base-keymap.json for compact/dense; domain keymap for domain mode
2. **Load keymap from file** — parse the JSON mapping object
3. **Walk input object** — iterate over every key at every depth level
4. **Check each key against map** — if the key exists in the map, replace with the short version
5. **Preserve unknown keys** — if a key is not in the map, keep it exactly as-is
6. **Return shortened object** — pass to the next pipeline step (value-encoder or output-formatter)

## Examples

### Example 1: Base keymap application

**Input:**
```json
{
  "goal": "build auth API",
  "action": "create",
  "inputs": ["email", "password"],
  "domain": "web-api",
  "constraints": ["jwt-only"],
  "format": "json",
  "examples": null
}
```

**Output:**
```json
{
  "g": "build auth API",
  "a": "create",
  "i": ["email", "password"],
  "d": "web-api",
  "c": ["jwt-only"],
  "f": "json",
  "e": null
}
```

### Example 2: Domain keymap with extra fields

**Input (from web-api domain normalization):**
```json
{
  "method": "POST",
  "endpoint": "/api/users",
  "auth": "bearer-jwt",
  "payload": ["name", "email"],
  "headers": ["content-type"],
  "response-format": "json",
  "middleware": ["rate-limit"]
}
```

**Output (using web-api keymap):**
```json
{
  "m": "POST",
  "ep": "/api/users",
  "au": "bearer-jwt",
  "pl": ["name", "email"],
  "hd": ["content-type"],
  "rf": "json",
  "mw": ["rate-limit"]
}
```

### Example 3: Unknown keys pass through

**Input:**
```json
{
  "goal": "analyze logs",
  "action": "read",
  "inputs": ["server-logs"],
  "custom-field": "this-is-not-in-keymap"
}
```

**Output:**
```json
{
  "g": "analyze logs",
  "a": "read",
  "i": ["server-logs"],
  "custom-field": "this-is-not-in-keymap"
}
```

*`custom-field` is not in any keymap, so it passes through unchanged.*

## Related Skills

- **marlin-compact** — calls key-shortener as step 2 of its pipeline
- **marlin-dense** — calls key-shortener via compact pipeline
- **marlin-domain** — calls key-shortener with domain-specific keymap
- **schema-normalizer** — produces the normalized object that key-shortener processes
- **value-encoder** — next step after key-shortener in dense mode
