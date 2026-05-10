---
name: marlin-structured
version: 1.0.0
author: adisingh-cs
project: marlin
phase: v1
category: compression
tags: [structured, normalize, schema, entry-point]
input_format: natural-language
output_format: structured-json
token_impact: high
stability: stable
trigger: "/marlin structured"
---

# marlin-structured

Structured mode is Marlin's foundational compression level. It takes a raw natural-language prompt, parses its intent, normalizes it against the base schema, and returns a clean, unambiguous JSON representation. This is the entry point for users who want deterministic prompt structure without aggressive key or value compression.

## When to trigger

- User types `/marlin structured` before or after their prompt
- User says "use structured mode", "normalize this prompt", or "structure this"
- User asks for "basic compression" or "schema-based formatting"
- Default mode when user invokes Marlin without specifying a mode

## Do NOT trigger when

- User specifies `/marlin compact`, `/marlin dense`, or `/marlin domain`
- User requests DSL format (use dsl-bridge instead)
- Input is already valid JSON matching the base schema

## Pipeline steps

1. **Detect input type** — confirm the input is natural language (not already JSON or DSL)
2. **Call intent-parser** — extract goal, action, inputs, domain, constraints, format, examples from the raw prompt using alias resolution
3. **Call schema-normalizer** — map the parsed intent object to `schemas/v1/base.schema.json`, enforce types, apply defaults, fill missing fields with null
4. **Call output-formatter** — format the result according to the user's `--out` flag (default: `report`)
5. **Return result** — deliver the structured JSON representation to the user

## Schema reference

Uses `schemas/v1/base.schema.json` with fields:

| Field | Type | Required | Default |
|-------|------|----------|---------|
| goal | string (max 100) | yes | — |
| action | string | yes | — |
| inputs | array of strings | yes | — |
| domain | string or null | no | null |
| constraints | array of strings or null | no | null |
| format | string | no | "json" |
| examples | array of strings or null | no | null |

## Token reduction

Typical reduction: **20–35%** from the original natural-language prompt.

Structured mode removes conversational filler, normalizes intent into fixed fields, and eliminates ambiguity — but retains full-length key names and does not abbreviate values.

## Examples

### Example 1: Coding task

**Input:**
```
I need to build a REST API endpoint that handles user authentication using JWT tokens.
The endpoint should accept email and password as inputs, validate them against the database,
and return an access token and refresh token if successful. Use Express.js.
```

**Output (structured JSON):**
```json
{
  "goal": "build REST API endpoint for user authentication",
  "action": "create",
  "inputs": ["email", "password"],
  "domain": "web-api",
  "constraints": ["jwt-only", "validate-against-database", "return-access-and-refresh-tokens"],
  "format": "json",
  "examples": ["Express.js"]
}
```

**Report:**
```
Mode: structured
Original tokens (est.): 62
Compressed tokens (est.): 38
Reduction: 39%
```

### Example 2: API design task

**Input:**
```
Design a GraphQL schema for a blog platform. It should support posts, comments, and users.
Each post has a title, body, author, and list of comments. Comments have text and author.
Users have username, email, and bio. Include queries for listing posts and getting a single post by ID.
```

**Output (structured JSON):**
```json
{
  "goal": "design GraphQL schema for blog platform",
  "action": "design",
  "inputs": ["posts", "comments", "users"],
  "domain": "web-api",
  "constraints": ["post-has-title-body-author-comments", "comment-has-text-author", "user-has-username-email-bio", "query-list-posts", "query-get-post-by-id"],
  "format": "graphql",
  "examples": null
}
```

### Example 3: Data task

**Input:**
```
Write a Python script that reads a CSV file containing sales data, filters rows where revenue
is greater than 10000, groups by region, calculates the average revenue per region,
and writes the result to a new CSV file sorted by average revenue descending.
```

**Output (structured JSON):**
```json
{
  "goal": "process sales CSV with filtering and aggregation",
  "action": "write",
  "inputs": ["sales-csv-file"],
  "domain": "data-pipeline",
  "constraints": ["filter-revenue-gt-10000", "group-by-region", "calc-avg-revenue-per-region", "sort-avg-revenue-desc"],
  "format": "csv",
  "examples": ["Python"]
}
```

## Related Skills

- **intent-parser** — called in step 2 to extract structured intent from natural language
- **schema-normalizer** — called in step 3 to enforce base schema types and defaults
- **output-formatter** — called in step 4 to format output per user's `--out` flag
- **token-estimator** — used by output-formatter for token count estimates in report mode
- **marlin-compact** — next compression level up; applies key shortening on top of structured output
