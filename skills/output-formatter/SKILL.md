---
name: output-formatter
version: 1.0.0
author: adisingh-cs
project: marlin
phase: v1
category: formatting
tags: [output, formatting, report, diff, display]
input_format: json
output_format: report
token_impact: none
stability: stable
trigger: internal
---

# output-formatter

The output formatter is the last step in every Marlin pipeline. It takes the compressed output from the compression pipeline and formats it according to the user's `--out` flag. It supports four output modes: prompt (raw compressed output), report (with token stats), diff (side-by-side comparison), and all (everything combined). If no flag is specified, the default is `report`.

## When to trigger

- Called internally as the final step in every mode skill pipeline
- Receives the compressed object and the original prompt text
- Never invoked directly by the user

## Do NOT trigger when

- No compressed output is available (pipeline must complete first)
- User explicitly requests raw JSON without formatting (edge case — still use `prompt` mode)

## Output modes

### `--out prompt`
Returns the compressed prompt only, with no wrapper or metadata. Ready to paste directly into another tool or pipe to an API.

```
{"g":"build auth API","a":"create","i":["email","password"],"d":"web-api","c":["jwt-only"],"f":"json"}
```

### `--out report`
Returns the compressed prompt plus a statistics block showing token savings. This is the **default** mode.

```
── Marlin Report ──────────────────────────────
Mode:              compact
Original tokens:   58 (estimated)
Compressed tokens: 27 (estimated)
Reduction:         53%
───────────────────────────────────────────────

{"g":"build auth API","a":"create","i":["email","password"],"d":"web-api","c":["jwt-only"],"f":"json"}
```

### `--out diff`
Returns a two-column view showing original fields mapped to compressed equivalents with arrow notation.

```
── Marlin Diff ────────────────────────────────
goal: "build REST API for auth"    →  g: "build auth API"
action: "create"                   →  a: "create"
inputs: ["email", "password"]      →  i: ["email", "password"]
domain: "web-api"                  →  d: "web-api"
constraints: ["jwt-only"]          →  c: ["jwt-only"]
format: "json"                     →  f: "json"
examples: null                     →  (dropped)
───────────────────────────────────────────────
```

### `--out all`
Returns all three blocks (prompt, report, diff) separated by clear dividers.

## Default behavior

If the user does not specify an `--out` flag, the output formatter uses `report` mode.

## Pipeline steps

1. **Receive compressed object and original prompt** — both are needed for report and diff modes
2. **Determine output mode** — parse the `--out` flag from user command; default to `report`
3. **Call token-estimator** — get estimated token counts for both original and compressed text
4. **Format output** — build the appropriate output block(s) based on the selected mode
5. **Return formatted result** — deliver to the user

## Token estimation integration

The output formatter calls token-estimator for the `report` and `all` modes. It passes:
- The original prompt string (natural language → use 4 chars/token ratio)
- The compressed JSON string (structured text → use 3.5 chars/token ratio)

The report always includes the word "estimated" next to token counts to avoid implying exact tokenizer accuracy.

## Examples

### Example 1: Report mode (default)

**Input context:**
- Original prompt: "Build a REST API endpoint that handles user authentication using JWT tokens" (75 chars)
- Compressed: `{"g":"build auth API ep","a":"create","i":["email","password"],"d":"web-api","c":["jwt-only"],"f":"json"}` (102 chars)
- Mode: compact

**Output:**
```
── Marlin Report ──────────────────────────────
Mode:              compact
Original tokens:   19 (estimated)
Compressed tokens: 29 (estimated)
Reduction:         Note: structured representation may increase character count
         but reduces ambiguity and improves model comprehension
───────────────────────────────────────────────

{"g":"build auth API ep","a":"create","i":["email","password"],"d":"web-api","c":["jwt-only"],"f":"json"}
```

### Example 2: Prompt mode (raw output)

**Output:**
```
{"g":"build auth API ep","a":"create","i":"email,password","d":"web-api","c":"jwt-only","f":"json"}
```

*No wrapper, no stats. Just the compressed payload.*

### Example 3: Diff mode

**Output:**
```
── Marlin Diff ────────────────────────────────
goal: "build REST API for user auth"  →  g: "build auth API ep"
action: "create"                      →  a: "create"
inputs: ["email", "password"]         →  i: "email,password"
domain: "web-api"                     →  d: "web-api"
constraints: ["jwt-only", "validate"] →  c: "jwt-only,val"
format: "json"                        →  f: "json"
examples: null                        →  (dropped)
───────────────────────────────────────────────
```

## Related Skills

- **token-estimator** — provides token count estimates for report mode
- **marlin-structured** — calls output-formatter as its final step
- **marlin-compact** — calls output-formatter as its final step
- **marlin-dense** — calls output-formatter as its final step
- **marlin-domain** — calls output-formatter as its final step
