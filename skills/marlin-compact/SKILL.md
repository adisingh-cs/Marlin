---
name: marlin-compact
description: Compress a prompt into minified JSON with shortened single-letter keys for maximum token efficiency. Use when the user types /marlin compact or wants to reduce input token cost on API calls or agent pipelines.
version: 1.0.0
author: adisingh-cs
project: marlin
phase: v1
category: compression
tags: [compact, minify, short-keys, api-ready]
input_format: natural-language
output_format: compact-json
token_impact: high
stability: stable
trigger: "/marlin compact"
---

# marlin-compact

Compact mode builds on structured mode by applying key shortening and JSON minification. All verbose key names are replaced with single-letter or two-letter abbreviations using the base keymap, whitespace is stripped, and null/empty fields are dropped. The result is a dense, machine-friendly JSON payload that retains full semantic meaning at roughly half the original token count.

## When to trigger

- User types `/marlin compact` before or after their prompt
- User says "compact this", "minify my prompt", or "make it shorter"
- User wants API-ready compressed prompts
- User is building agent pipelines and needs minimal token overhead

## Do NOT trigger when

- User specifies `/marlin structured` (they want readable keys)
- User specifies `/marlin dense` (they want value abbreviation too)
- User specifies `/marlin domain` (they want domain-specific compression)

## Key map applied

Source: `schemas/key-maps/base-keymap.json`

| Full key | Short key |
|----------|-----------|
| goal | g |
| action | a |
| inputs | i |
| domain | d |
| constraints | c |
| format | f |
| examples | e |
| output | o |
| context | ctx |
| type | t |
| method | m |
| auth | au |
| schema | sc |
| version | v |
| endpoint | ep |
| payload | pl |
| response | rs |
| headers | hd |
| middleware | mw |

## Pipeline steps

1. **Run full structured pipeline** — intent-parser → schema-normalizer (produces structured JSON)
2. **Apply key-shortener** — load `schemas/key-maps/base-keymap.json`, replace all matching keys
3. **Strip whitespace** — remove all non-essential whitespace from the JSON output
4. **Drop null/empty fields** — remove any field whose value is null, empty string, or empty array
5. **Call output-formatter** — format result per user's `--out` flag (default: `report`)

## Token reduction

Typical reduction: **35–50%** from the original natural-language prompt.

Key shortening typically saves 15–20% on top of structured mode's gains. Null dropping and minification add another 5–10%.

## Examples

### Example 1: Authentication API

**Input:**
```
I need to build a REST API endpoint that handles user authentication using JWT tokens.
The endpoint should accept email and password as inputs, validate them against the database,
and return an access token and refresh token if successful.
```

**Output (compact JSON):**
```json
{"g":"build auth api endpoint","a":"create","i":["email","password"],"d":"web-api","c":["jwt-only","validate-against-db"],"f":"json"}
```

**Report:**
```
Mode: compact
Original tokens (est.): 58
Compressed tokens (est.): 27
Reduction: 53%
```

### Example 2: React component

**Input:**
```
Create a React component called UserProfile that displays a user's avatar, name, email,
and bio. It should accept a user object as a prop, handle loading and error states,
and use Tailwind CSS for styling. Include a button to edit the profile that opens a modal.
```

**Output (compact JSON):**
```json
{"g":"create UserProfile React component","a":"create","i":["user-object"],"d":"frontend","c":["handle-loading-state","handle-error-state","tailwind-css","edit-button-opens-modal"],"f":"jsx"}
```

### Example 3: Database migration

**Input:**
```
Write a database migration that adds a new table called notifications with columns:
id (UUID primary key), user_id (foreign key to users), message (text not null),
read (boolean default false), created_at (timestamp), and an index on user_id.
```

**Output (compact JSON):**
```json
{"g":"add notifications table","a":"create","i":["id-uuid-pk","user_id-fk-users","message-text-not-null","read-bool-default-false","created_at-timestamp"],"d":"database","c":["index-on-user_id"],"f":"sql"}
```

## Related Skills

- **marlin-structured** — provides the structured JSON that compact mode builds on
- **intent-parser** — extracts intent from natural language (called via structured pipeline)
- **schema-normalizer** — enforces base schema (called via structured pipeline)
- **key-shortener** — applies the key abbreviation map (called in step 2)
- **output-formatter** — formats the final output per user's `--out` flag
- **token-estimator** — estimates token counts for reports
- **marlin-dense** — next level; adds value abbreviation on top of compact
