---
name: value-encoder
version: 1.0.0
author: adisingh-cs
project: marlin
phase: v1
category: encoding
tags: [values, abbreviation, dense, compression]
input_format: compact-json
output_format: dense-json
token_impact: medium
stability: stable
trigger: internal
---

# value-encoder

The value encoder applies abbreviation to string values within a key-shortened JSON object. It replaces common technical terms with standardized short codes, collapses single-item arrays to scalars, and inlines multi-value arrays as comma-separated strings. This is the final compression pass in dense mode and is responsible for the additional 10–20% token savings beyond compact mode.

## When to trigger

- Called internally by dense mode only (marlin-dense)
- Runs after key-shortener, before output-formatter
- Never invoked directly by the user

## Do NOT trigger when

- Running in structured or compact mode (no value abbreviation in those modes)
- Running in domain mode (domain mode handles value encoding differently)

## Hard rules

1. **Only abbreviate string values** — never abbreviate keys (key-shortener handles keys)
2. **Only apply known abbreviations** from the table below — never guess or invent
3. **Never abbreviate values shorter than 5 characters** — too short to save meaningful tokens
4. **Never abbreviate proper nouns** — project names, library names, brand names stay as-is
5. **Never abbreviate identifiers** — variable names, function names, class names stay as-is
6. **Never abbreviate URLs or file paths** — these must remain intact
7. **Abbreviation is case-insensitive matching** but output uses the abbreviated form's casing

## Abbreviation table

| Full value | Abbreviation | Savings |
|-----------|--------------|---------|
| authentication | auth | 10 chars |
| authorization | authz | 8 chars |
| generate | gen | 5 chars |
| endpoint | ep | 6 chars |
| request | req | 4 chars |
| response | res | 5 chars |
| parameter | param | 4 chars |
| function | fn | 6 chars |
| database | db | 6 chars |
| configuration | cfg | 10 chars |
| interface | iface | 4 chars |
| implementation | impl | 10 chars |
| validation | val | 6 chars |
| middleware | mw | 8 chars |
| repository | repo | 6 chars |
| component | comp | 5 chars |
| dependency | dep | 7 chars |
| environment | env | 8 chars |
| infrastructure | infra | 9 chars |
| deployment | deploy | 4 chars |
| application | app | 8 chars |
| notification | notif | 7 chars |
| subscription | sub | 8 chars |
| transaction | txn | 8 chars |
| integration | integ | 6 chars |

## Array collapsing rules

1. **Single-item array → scalar:** `["email"]` becomes `"email"`
2. **Multi-item array → inline string:** `["email","password","token"]` becomes `"email,password,token"`
3. **Empty array → drop field:** `[]` is treated as null and removed in the compact step
4. **Nested arrays:** not supported in Marlin schemas; if encountered, flatten to comma-separated

## Pipeline steps

1. **Receive key-shortened JSON** — input from key-shortener
2. **Scan all string values** — check each against the abbreviation table
3. **Apply abbreviations** — replace matching substrings within values (word-boundary aware)
4. **Collapse single-item arrays** — convert to scalar strings
5. **Inline multi-value arrays** — remove brackets, join with commas, no spaces
6. **Return dense object** — pass to output-formatter

## Examples

### Example 1: Full abbreviation pass

**Input (from key-shortener):**
```json
{"g":"build authentication middleware function","a":"create","i":["jwt-token"],"d":"authentication","c":["validation-against-database","handle-missing-token"]}
```

**Output (after value encoding):**
```json
{"g":"build auth mw fn","a":"create","i":"jwt-token","d":"auth","c":"val-against-db,handle-missing-token"}
```

*Changes: authentication→auth, middleware→mw, function→fn, validation→val, database→db, single-item array collapsed, multi-item array inlined.*

### Example 2: Selective abbreviation (short values preserved)

**Input:**
```json
{"g":"create user API endpoint","a":"create","i":["name","email","role"],"d":"web","c":["rate-limit"]}
```

**Output:**
```json
{"g":"create user API ep","a":"create","i":"name,email,role","d":"web","c":"rate-limit"}
```

*"endpoint" → "ep". "web", "name", "email", "role" are under 5 chars — not abbreviated. "rate-limit" has no match in the table — preserved.*

### Example 3: Proper nouns and identifiers preserved

**Input:**
```json
{"g":"deploy application to Kubernetes","a":"deploy","i":["docker-image","Redis","PostgreSQL"],"d":"infrastructure"}
```

**Output:**
```json
{"g":"deploy app to Kubernetes","a":"deploy","i":"docker-image,Redis,PostgreSQL","d":"infra"}
```

*"application" → "app", "infrastructure" → "infra". "Kubernetes", "Redis", "PostgreSQL" are proper nouns — preserved.*

## Related Skills

- **key-shortener** — produces the key-shortened JSON that value-encoder processes
- **marlin-dense** — the only mode skill that calls value-encoder
- **output-formatter** — receives the dense object for final formatting
- **token-estimator** — measures the token savings achieved by value encoding
