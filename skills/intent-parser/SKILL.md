---
name: intent-parser
version: 1.0.0
author: adisingh-cs
project: marlin
phase: v1
category: parsing
tags: [parsing, nlp, intent, extraction, alias-resolution]
input_format: natural-language
output_format: structured-json
token_impact: medium
stability: stable
trigger: internal
---

# intent-parser

The intent parser is the first step in every Marlin compression pipeline. It takes a raw natural-language prompt and extracts structured intent by scanning for alias keywords mapped to canonical schema fields. The output is a partial intent object — fields that cannot be identified are set to null, never omitted. Unrecognized or ambiguous content is dropped silently; the parser never errors on valid text input.

## When to trigger

- Called internally by all four mode skills (structured, compact, dense, domain)
- Never invoked directly by the user
- Always the first skill in the pipeline

## Do NOT trigger when

- Input is already structured JSON (pass directly to schema-normalizer)
- Input is V3 DSL format (use dsl-bridge instead)

## Alias resolution table

The parser scans for these keywords and phrases to identify canonical fields:

| Canonical field | Alias keywords |
|----------------|----------------|
| **goal** | objective, purpose, task, want, need, build, create, make, design, implement, develop, set up, configure |
| **action** | verb, operation, do, perform, run, execute, generate, write, read, update, delete, deploy, test, analyze |
| **inputs** | params, args, fields, data, variables, values, given, accepts, takes, receives, with, using, from |
| **domain** | context, area, topic, category, subject, about, for, in, related to, concerning |
| **constraints** | limits, rules, must, cannot, only, never, always, requirements, should, ensure, enforce, restrict, no more than, at least |
| **format** | output, return, response, give me, show me, as, in the form of, formatted as, render as |
| **examples** | like, e.g., for example, such as, sample, similar to, based on, reference, model after |

## Extraction rules

1. **Goal extraction** — identify the primary objective. Look for the main clause following "build", "create", "design", etc. Truncate to 100 characters.
2. **Action extraction** — identify the primary verb. If multiple verbs exist, choose the most specific one (e.g., "validate" over "do").
3. **Input extraction** — collect all named parameters, fields, variables, or data items mentioned. Return as array even if single item.
4. **Domain detection** — infer from context clues. "API", "endpoint", "REST" → "web-api". "pipeline", "ETL", "transform" → "data-pipeline". "agent", "task", "tool-use" → "agent-task". Generic or unclear → null.
5. **Constraint extraction** — collect all rules, requirements, and limitations. Each constraint becomes one array element.
6. **Format detection** — look for explicit format mentions (JSON, YAML, SQL, CSV, etc.). Default to "json" if not specified.
7. **Example extraction** — collect any referenced examples, samples, or "like X" references.

## Pipeline steps

1. **Receive raw prompt** — accept the natural-language string
2. **Tokenize and scan** — break into clauses; scan each clause against alias table
3. **Map aliases to canonical fields** — when an alias is found, extract the associated value
4. **Build partial intent object** — populate all 7 fields; use null for any field not identified
5. **Return intent object** — pass to schema-normalizer for type enforcement

## Handling edge cases

- **Multiple goals detected:** use the first one; append others to constraints
- **No action verb found:** set action to "create" as default
- **Empty prompt:** return all-null object (schema-normalizer will catch required field violations)
- **Unrecognized content:** drop silently — never add to unknown fields, never error
- **Domain hint provided:** if domain mode passes a domain hint, use it directly instead of inferring

## Examples

### Example 1: Imperative prompt

**Input:**
```
Build a login page with email and password fields that validates input on the client side
and sends credentials to the /api/auth endpoint.
```

**Output (partial intent):**
```json
{
  "goal": "build a login page",
  "action": "build",
  "inputs": ["email", "password"],
  "domain": "web-api",
  "constraints": ["validate-input-client-side", "send-to-/api/auth"],
  "format": "json",
  "examples": null
}
```

### Example 2: Question-style prompt

**Input:**
```
How do I set up a CI/CD pipeline using GitHub Actions that runs tests on every pull request
and deploys to AWS on merge to main?
```

**Output (partial intent):**
```json
{
  "goal": "set up CI/CD pipeline with GitHub Actions",
  "action": "create",
  "inputs": ["github-actions", "aws"],
  "domain": "infrastructure",
  "constraints": ["run-tests-on-pr", "deploy-on-merge-to-main"],
  "format": "json",
  "examples": null
}
```

### Example 3: Casual prompt

**Input:**
```
I want something like Stripe's checkout flow but for digital downloads, need to handle
payments, generate license keys, and send confirmation emails.
```

**Output (partial intent):**
```json
{
  "goal": "build checkout flow for digital downloads",
  "action": "create",
  "inputs": ["payments", "license-keys", "confirmation-emails"],
  "domain": "web-api",
  "constraints": null,
  "format": "json",
  "examples": ["Stripe checkout flow"]
}
```

### Example 4: Technical prompt

**Input:**
```
Implement a Redis-backed rate limiter using the sliding window algorithm with a limit of
100 requests per 60-second window per API key, returning 429 with Retry-After header
when exceeded.
```

**Output (partial intent):**
```json
{
  "goal": "implement Redis-backed rate limiter",
  "action": "implement",
  "inputs": ["api-key"],
  "domain": "web-api",
  "constraints": ["sliding-window-algorithm", "100-req-per-60s-per-key", "return-429-with-retry-after"],
  "format": "json",
  "examples": null
}
```

## Related Skills

- **schema-normalizer** — receives the partial intent object and enforces schema types
- **marlin-structured** — calls intent-parser as its first pipeline step
- **marlin-compact** — calls intent-parser via the structured pipeline
- **marlin-dense** — calls intent-parser via the structured pipeline
- **marlin-domain** — calls intent-parser with domain context hint
