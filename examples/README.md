# Examples

This directory contains complete input/output pairs for every Marlin compression mode. Each example uses realistic developer prompts — no placeholder text.

## Structure

```
examples/
├── structured/         # Structured mode (full key names, schema-normalized)
│   ├── input.txt
│   └── output.json
├── compact/            # Compact mode (short keys, minified, nulls dropped)
│   ├── input.txt
│   └── output.json
├── dense/              # Dense mode (short keys + value abbreviation + array collapse)
│   ├── input.txt
│   └── output.json
├── domain/             # Domain mode (domain-specific schemas and keymaps)
│   ├── web-api-input.txt
│   ├── web-api-output.json
│   ├── data-pipeline-input.txt
│   ├── data-pipeline-output.json
│   ├── agent-task-input.txt
│   └── agent-task-output.json
└── v3-dsl/             # V3 DSL format (internal DSL + external JSON)
    ├── internal.txt
    └── external.json
```

## How to read these examples

1. Open `input.txt` — this is what the user types (natural language prompt)
2. Open `output.json` — this is what Marlin produces after compression
3. Compare token counts mentally or use `tools/test-skill.py` to validate

## Using examples for testing

These examples serve as golden fixtures. Run `python tools/test-skill.py` against them to validate skill behavior.
