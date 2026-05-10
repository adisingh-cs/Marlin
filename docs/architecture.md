# Architecture

Marlin is a pipeline-based prompt compression system. Every prompt flows through a series of skills, each performing one transformation step. The architecture is designed for composability — skills chain together, schemas anchor the data contract at every stage, and output formatting is decoupled from compression logic.

## System overview

```
┌──────────────────────────────────────────────────────────┐
│                      USER INPUT                          │
│              (natural language prompt)                    │
└────────────────────────┬─────────────────────────────────┘
                         │
                         ▼
┌──────────────────────────────────────────────────────────┐
│                   MODE SELECTOR                          │
│   /marlin structured | compact | dense | domain | dsl    │
└────────────────────────┬─────────────────────────────────┘
                         │
          ┌──────────────┼──────────────┐
          ▼              ▼              ▼
   ┌─────────────┐ ┌─────────┐ ┌─────────────┐
   │ intent-     │ │ domain  │ │ dsl-bridge  │
   │ parser      │ │ schema  │ │ (V3 only)   │
   │             │ │ loader  │ │             │
   └──────┬──────┘ └────┬────┘ └──────┬──────┘
          │              │             │
          ▼              ▼             │
   ┌──────────────────────────┐       │
   │   schema-normalizer      │       │
   │   (base or domain)       │       │
   └──────────┬───────────────┘       │
              │                        │
     ┌────────┼────────┐              │
     ▼        ▼        ▼              │
  ┌──────┐ ┌──────┐ ┌──────┐         │
  │struct│ │key-  │ │value-│         │
  │ured │ │short-│ │encod-│         │
  │ only │ │ener  │ │er    │         │
  └──┬───┘ └──┬───┘ └──┬───┘         │
     │        │        │              │
     └────────┼────────┘              │
              │                        │
              ▼                        ▼
   ┌──────────────────────────────────────┐
   │         output-formatter             │
   │   --out prompt|report|diff|all       │
   │         (uses token-estimator)       │
   └──────────────────┬───────────────────┘
                      │
                      ▼
   ┌──────────────────────────────────────┐
   │           COMPRESSED OUTPUT          │
   │      (ready for LLM consumption)     │
   └──────────────────────────────────────┘
```

## Pipeline per mode

### Structured pipeline
```
input → intent-parser → schema-normalizer(base) → output-formatter
```

### Compact pipeline
```
input → intent-parser → schema-normalizer(base) → key-shortener(base-keymap) → output-formatter
```

### Dense pipeline
```
input → intent-parser → schema-normalizer(base) → key-shortener(base-keymap) → value-encoder → output-formatter
```

### Domain pipeline
```
input → intent-parser(domain-hint) → schema-normalizer(domain-schema) → key-shortener(domain-keymap) → output-formatter
```

### V3 DSL bridge
```
input(DSL) → dsl-bridge(parse) → external-json → output-formatter
input(JSON) → dsl-bridge(serialize) → internal-DSL → output-formatter
```

## Skill dependency graph

```
marlin-structured ──→ intent-parser ──→ schema-normalizer ──→ output-formatter
                                                                    │
marlin-compact ────→ intent-parser ──→ schema-normalizer ──→ key-shortener ──→ output-formatter
                                                                                      │
marlin-dense ──────→ intent-parser ──→ schema-normalizer ──→ key-shortener ──→ value-encoder ──→ output-formatter
                                                                                                        │
marlin-domain ─────→ intent-parser ──→ schema-normalizer ──→ key-shortener ──→ output-formatter
                          │                    │                    │
                     (domain hint)      (domain schema)      (domain keymap)

dsl-bridge ────────→ (standalone, bidirectional conversion)

output-formatter ──→ token-estimator (for report/diff modes)
```

## Schema anchoring

Every stage of the pipeline produces output that conforms to a JSON Schema:

| Pipeline stage | Schema |
|---------------|--------|
| After intent-parser | Partial `base.schema.json` (nulls allowed) |
| After schema-normalizer | Full `base.schema.json` or domain schema |
| After key-shortener | `external-json.schema.json` (short keys) |
| After value-encoder | `external-json.schema.json` (short keys + abbreviated values) |
| V3 DSL string | `internal-dsl.schema.json` (pattern-validated string) |

## Key maps as contracts

Key maps are JSON files that define the mapping between verbose and abbreviated keys:

- `base-keymap.json` — used by compact and dense modes
- `web-api-keymap.json` — extends base for web API domain
- `data-pipeline-keymap.json` — extends base for data pipeline domain
- `agent-task-keymap.json` — extends base for agent task domain

**Rules:**
- Maps are additive — domain maps include all base mappings plus domain-specific ones
- On conflict, domain map wins
- Keys not in any map pass through unchanged
- Skills never invent abbreviations — only map-defined abbreviations are used

## Output formatting

The output-formatter is decoupled from compression logic. It receives:
1. The compressed object (from any mode)
2. The original prompt text
3. The user's `--out` flag

It then calls token-estimator for counts and formats the result. This separation means compression skills never need to know about output presentation.
