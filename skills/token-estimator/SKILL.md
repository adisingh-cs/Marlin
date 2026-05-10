---
name: token-estimator
version: 1.0.0
author: adisingh-cs
project: marlin
phase: v1
category: estimation
tags: [tokens, estimation, counting, cost]
input_format: natural-language
output_format: structured-json
token_impact: none
stability: stable
trigger: internal
---

# token-estimator

The token estimator provides approximate token counts for strings using a character-based heuristic. It differentiates between natural-language text and structured text (JSON, DSL) and applies the appropriate ratio. This skill is used by the output-formatter to generate token savings reports. It always clearly states that counts are estimates — actual token counts depend on the specific tokenizer used by the target LLM.

## When to trigger

- Called internally by output-formatter when generating report or diff output
- Can be called by any skill that needs a token count estimate
- Never invoked directly by the user

## Do NOT trigger when

- Exact token counts are needed (use the target model's tokenizer instead)
- The string is empty or null (return 0)

## Estimation formula

| Input type | Formula | Rationale |
|-----------|---------|-----------|
| Natural language (English) | `ceil(len(string) / 4)` | English text averages ~4 characters per token across GPT/Claude tokenizers |
| JSON / structured text | `ceil(len(string) / 3.5)` | JSON has more punctuation and short tokens, increasing the token-to-character ratio |
| DSL (V3 internal format) | `ceil(len(string) / 3)` | DSL is dense with delimiters, further increasing the ratio |

## Hard rules

1. **Always state this is an estimate** — never claim exact count
2. **Actual count depends on tokenizer** — different models use different tokenizers (BPE, SentencePiece, etc.)
3. **Return integer values only** — always round up using ceiling
4. **Empty or null input returns 0** — do not error
5. **Count characters after any encoding** — if the string contains Unicode, count the full character representation

## Input type detection

The estimator auto-detects input type:

1. **JSON:** string starts with `{` or `[` and is valid JSON structure
2. **DSL:** string matches the V3 DSL pattern (`KEY:value|KEY:value`)
3. **Natural language:** everything else

## Pipeline steps

1. **Receive input string** — the text to estimate tokens for
2. **Detect input type** — JSON, DSL, or natural language
3. **Apply formula** — divide character count by the appropriate ratio and ceil
4. **Return estimate** — integer token count with type annotation

## Examples

### Example 1: Natural language prompt

**Input:**
```
Build a REST API endpoint that handles user authentication using JWT tokens and returns access and refresh tokens.
```

**Calculation:**
- Character count: 113
- Type: natural language
- Formula: ceil(113 / 4) = 29

**Output:**
```json
{
  "input_type": "natural-language",
  "character_count": 113,
  "estimated_tokens": 29,
  "note": "Estimate based on ~4 chars/token for English text. Actual count depends on model tokenizer."
}
```

### Example 2: Compact JSON

**Input:**
```
{"g":"build auth API ep","a":"create","i":["email","password"],"d":"web-api","c":["jwt-only"],"f":"json"}
```

**Calculation:**
- Character count: 102
- Type: JSON
- Formula: ceil(102 / 3.5) = 30

**Output:**
```json
{
  "input_type": "json",
  "character_count": 102,
  "estimated_tokens": 30,
  "note": "Estimate based on ~3.5 chars/token for JSON. Actual count depends on model tokenizer."
}
```

### Example 3: V3 DSL format

**Input:**
```
G:build auth API|A:create|I:email,password|D:web-api|C:jwt-only|F:json
```

**Calculation:**
- Character count: 70
- Type: DSL
- Formula: ceil(70 / 3) = 24

**Output:**
```json
{
  "input_type": "dsl",
  "character_count": 70,
  "estimated_tokens": 24,
  "note": "Estimate based on ~3 chars/token for DSL. Actual count depends on model tokenizer."
}
```

### Example 4: Comparison for report

**Input (pair):**
- Original (natural language, 245 chars): est. 62 tokens
- Compressed (JSON, 98 chars): est. 28 tokens
- Reduction: 55%

**Output:**
```json
{
  "original_tokens": 62,
  "compressed_tokens": 28,
  "reduction_pct": 55,
  "note": "All counts are estimates. Actual savings may vary by ±5-10% depending on tokenizer."
}
```

## Related Skills

- **output-formatter** — calls token-estimator for report and diff modes
- **marlin-structured** — benefits from token estimates in pipeline output
- **marlin-compact** — benefits from token estimates in pipeline output
- **marlin-dense** — benefits from token estimates in pipeline output
- **marlin-domain** — benefits from token estimates in pipeline output
