---
name: marlin-domain
description: Compress a prompt using a domain-specific schema for web-api, data-pipeline, or agent-task workflows. Use when the user types /marlin domain or specifies a domain like web-api, data-pipeline, or agent-task.
version: 1.0.0
author: adisingh-cs
project: marlin
phase: v1
category: compression
tags: [domain, specialized, web-api, data-pipeline, agent-task]
input_format: natural-language
output_format: compact-json
token_impact: high
stability: stable
trigger: "/marlin domain --schema web-api"
---

# marlin-domain

Domain mode applies domain-aware compression using specialist schemas and domain-specific key maps. Instead of using the generic base schema, it loads a schema tailored to a specific workflow type — web-api, data-pipeline, or agent-task — and maps prompt fields to domain-native terminology. This produces output that is both compressed and semantically aligned with the target domain.

## When to trigger

- User types `/marlin domain --schema web-api` (or `data-pipeline`, or `agent-task`)
- User says "use domain mode for API prompts" or "compress this as a data pipeline task"
- User is working in a specialized, repeated workflow within a single domain

## Do NOT trigger when

- User does not specify a `--schema` flag (cannot guess the domain)
- User specifies `/marlin structured`, `/marlin compact`, or `/marlin dense`
- The prompt does not fit any supported domain schema

## Supported domains

| Domain flag | Schema file | Key map file |
|-------------|-------------|--------------|
| `web-api` | `schemas/v1/web-api.schema.json` | `schemas/key-maps/web-api-keymap.json` |
| `data-pipeline` | `schemas/v1/data-pipeline.schema.json` | `schemas/key-maps/data-pipeline-keymap.json` |
| `agent-task` | `schemas/v1/agent-task.schema.json` | `schemas/key-maps/agent-task-keymap.json` |

## Pipeline steps

1. **Parse domain flag** — extract `--schema` value from user command; reject if missing or unsupported
2. **Load domain schema** — read the corresponding JSON Schema file
3. **Call intent-parser with domain context** — pass domain hint to improve field extraction accuracy
4. **Apply schema-normalizer with domain schema** — normalize against domain-specific required/optional fields
5. **Apply key-shortener with domain keymap** — use domain-specific abbreviations (extends base keymap)
6. **Strip whitespace and drop nulls** — compact compression pass
7. **Call output-formatter** — format result per user's `--out` flag (default: `report`)

## Token reduction

Typical reduction: **40–65%** from the original natural-language prompt.

Domain mode gains efficiency by mapping directly to pre-defined domain fields rather than the generic base schema, eliminating field-mapping overhead and enabling tighter abbreviations.

## Examples

### Example 1: Web API domain

**Input:**
```
Build a POST endpoint at /api/v2/users that accepts a JSON body with name, email,
and role fields. Authenticate using Bearer JWT tokens. Add rate limiting middleware
at 100 requests per minute. Return the created user object with a 201 status code.
```

**Output (`--schema web-api`):**
```json
{"m":"POST","ep":"/api/v2/users","au":"bearer-jwt","pl":["name","email","role"],"mw":["rate-limit-100rpm"],"rf":"json","v":"v2"}
```

**Report:**
```
Mode: domain (web-api)
Original tokens (est.): 62
Compressed tokens (est.): 24
Reduction: 61%
```

### Example 2: Data pipeline domain

**Input:**
```
Create a data pipeline that reads from a PostgreSQL database table called user_events,
filters events from the last 7 days, aggregates by event type with count and average
duration, writes the results to an S3 bucket in parquet format, runs every 6 hours,
and retries up to 5 times on failure with a batch size of 10000 records.
```

**Output (`--schema data-pipeline`):**
```json
{"src":"postgresql/user_events","tr":["filter-last-7d","agg-by-event-type-count-avg-duration"],"sk":"s3-bucket","f":"parquet","sched":"every-6h","rt":5,"bs":10000}
```

**Report:**
```
Mode: domain (data-pipeline)
Original tokens (est.): 70
Compressed tokens (est.): 25
Reduction: 64%
```

### Example 3: Agent task domain

**Input:**
```
Create an AI agent task that researches competitor pricing for SaaS products in the
developer tools category. The agent should use web search and document analysis tools,
maintain conversation memory across steps, output a structured comparison report,
and hand off the result to the pricing-strategy agent. Priority is high. Limit
context window to 8000 tokens.
```

**Output (`--schema agent-task`):**
```json
{"obj":"research competitor pricing for dev-tools SaaS","tl":["web-search","doc-analysis"],"mem":"conversation","ot":"report","hf":"pricing-strategy-agent","pr":"high","cw":8000}
```

**Report:**
```
Mode: domain (agent-task)
Original tokens (est.): 68
Compressed tokens (est.): 24
Reduction: 65%
```

## Related Skills

- **intent-parser** — extracts intent with domain context awareness
- **schema-normalizer** — normalizes against domain-specific schemas
- **key-shortener** — applies domain-specific key maps
- **output-formatter** — formats the final output per user's `--out` flag
- **token-estimator** — estimates token counts for reports
- **marlin-compact** — compact mode without domain specialization
