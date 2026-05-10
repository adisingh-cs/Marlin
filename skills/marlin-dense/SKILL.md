---
name: marlin-dense
description: Apply maximum compression to a prompt by shortening keys, abbreviating values, and collapsing arrays. Use when the user types /marlin dense or needs aggressive token reduction for high-volume or cost-sensitive workflows.
version: 1.0.0
author: adisingh-cs
project: marlin
phase: v1
category: compression
tags: [dense, aggressive, value-encoding, cost-optimization]
input_format: natural-language
output_format: dense-json
token_impact: high
stability: stable
trigger: "/marlin dense"
---

# marlin-dense

Dense mode is Marlin's most aggressive V1 compression level. It runs the full compact pipeline (structured + key shortening + minification) and then applies value abbreviation — replacing common technical terms with short codes. Single-item arrays are collapsed to scalars, and multi-value arrays are inlined as comma-separated strings. This mode targets 50–70% token reduction and is designed for high-volume, cost-sensitive workflows.

## When to trigger

- User types `/marlin dense` before or after their prompt
- User says "maximum compression", "densify this", or "make this as small as possible"
- User is optimizing for cost in high-volume API pipelines
- User is an experienced Marlin user comfortable with abbreviated output

## Do NOT trigger when

- User specifies `/marlin structured` or `/marlin compact`
- User needs human-readable output (dense output is machine-optimized)
- User specifies `/marlin domain` (domain mode has its own value handling)

## Value abbreviation table

Applied to string values only. Never applied to keys (key-shortener handles keys), proper nouns, identifiers, URLs, or file paths. Only values of 5+ characters are eligible.

| Full value | Abbreviation |
|-----------|--------------|
| authentication | auth |
| authorization | authz |
| generate | gen |
| endpoint | ep |
| request | req |
| response | res |
| parameter | param |
| function | fn |
| database | db |
| configuration | cfg |
| interface | iface |
| implementation | impl |
| validation | val |
| middleware | mw |
| repository | repo |
| component | comp |
| dependency | dep |
| environment | env |
| infrastructure | infra |
| deployment | deploy |
| application | app |
| notification | notif |
| subscription | sub |
| transaction | txn |
| integration | integ |

## Pipeline steps

1. **Run full compact pipeline** — structured → key-shortened → minified → null-dropped
2. **Apply value-encoder** — scan all string values against abbreviation table, replace matches
3. **Collapse single-item arrays** — if an array has exactly 1 element, convert to scalar string
4. **Inline multi-value arrays** — convert `["a","b","c"]` to `"a,b,c"` (remove brackets, comma-separate)
5. **Call output-formatter** — format result per user's `--out` flag (default: `report`)

## Token reduction

Typical reduction: **50–70%** from the original natural-language prompt.

Value encoding saves 10–20% on top of compact mode. Array collapsing saves another 5–10% by eliminating bracket and quote overhead.

## Examples

### Example 1: Authentication flow

**Input (67 tokens est.):**
```
Build an authentication middleware function that validates JWT tokens from the
request headers, checks the token against the database, and returns an unauthorized
response if the token is invalid or expired. Include error handling for missing tokens.
```

**Output (dense JSON, 19 tokens est.):**
```json
{"g":"build auth mw fn","a":"create","i":"jwt-token","d":"auth","c":"val-against-db,handle-missing-token,handle-expired-token","f":"json"}
```

**Report:**
```
Mode: dense
Original tokens (est.): 67
Compressed tokens (est.): 19
Reduction: 72%
```

### Example 2: Deployment configuration

**Input (54 tokens est.):**
```
Create a deployment configuration for a Node.js application that uses Docker containers,
sets up environment variables for database connection and API keys, configures auto-scaling
with minimum 2 and maximum 10 instances, and includes health check endpoints.
```

**Output (dense JSON, 18 tokens est.):**
```json
{"g":"create deploy cfg for Node.js app","a":"create","i":"docker-container","d":"infra","c":"env-vars-db-api-keys,auto-scale-min2-max10,health-check-ep","f":"yaml"}
```

**Report:**
```
Mode: dense
Original tokens (est.): 54
Compressed tokens (est.): 18
Reduction: 67%
```

### Example 3: API integration

**Input (72 tokens est.):**
```
Write an integration test for the payment processing endpoint that sends a POST request
with valid credit card parameters, validates the response contains a transaction ID
and confirmation status, handles timeout errors with retry logic, and mocks the
external payment gateway dependency.
```

**Output (dense JSON, 21 tokens est.):**
```json
{"g":"write integ test for payment ep","a":"create","i":"credit-card-params","d":"web-api","c":"val-res-has-txn-id,val-confirmation-status,handle-timeout-retry,mock-payment-gateway-dep","f":"json"}
```

**Report:**
```
Mode: dense
Original tokens (est.): 72
Compressed tokens (est.): 21
Reduction: 71%
```

## Related Skills

- **marlin-compact** — provides the compact JSON that dense mode builds on
- **marlin-structured** — foundational structured pipeline (called via compact)
- **intent-parser** — extracts intent from natural language (called via structured pipeline)
- **schema-normalizer** — enforces base schema (called via structured pipeline)
- **key-shortener** — applies key abbreviation (called via compact pipeline)
- **value-encoder** — applies value abbreviation table (called in step 2)
- **output-formatter** — formats the final output per user's `--out` flag
- **token-estimator** — estimates token counts for reports
