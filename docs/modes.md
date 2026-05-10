# Compression Modes

Marlin offers four compression modes plus a V3 DSL bridge. Each mode is a user-facing entry point that orchestrates internal skills to achieve a specific level of compression. Users select their mode explicitly — Marlin never auto-selects silently.

## Mode comparison

| Mode | Trigger | Token reduction | Best for |
|------|---------|----------------|----------|
| Structured | `/marlin structured` | 20–35% | First-time users, general prompts |
| Compact | `/marlin compact` | 35–50% | API calls, agent pipelines |
| Dense | `/marlin dense` | 50–70% | High-volume, cost-sensitive workflows |
| Domain | `/marlin domain --schema <name>` | 40–65% | Specialized repeated workflows |
| DSL Bridge | `/marlin dsl` | (conversion, not compression) | Agent-to-agent, storage |

---

## Structured mode

**Trigger:** `/marlin structured`

**Pipeline:** input → intent-parser → schema-normalizer(base) → output-formatter

**What it does:**
- Parses natural language into structured fields (goal, action, inputs, domain, constraints, format, examples)
- Normalizes against the base schema with type enforcement and defaults
- Retains full-length key names for readability
- Fills missing fields with null

**When to use:**
- You want readable, structured output
- You are new to Marlin and want to see how compression works
- Your prompts are general-purpose (not domain-specific)

**When NOT to use:**
- You need maximum compression (use dense)
- You are working in a specific domain (use domain mode)

**Example:**

Input:
```
Build a REST API with Express.js for user management with CRUD endpoints
```

Output:
```json
{
  "goal": "build REST API for user management",
  "action": "create",
  "inputs": ["users"],
  "domain": "web-api",
  "constraints": ["CRUD-endpoints", "Express.js"],
  "format": "json",
  "examples": null
}
```

---

## Compact mode

**Trigger:** `/marlin compact`

**Pipeline:** input → intent-parser → schema-normalizer(base) → key-shortener(base-keymap) → output-formatter

**What it does:**
- Runs the full structured pipeline first
- Applies key shortening using `base-keymap.json` (goal→g, action→a, etc.)
- Strips all whitespace
- Drops null and empty fields

**When to use:**
- You want a balance of compression and speed
- You are building API integrations or agent pipelines
- You need machine-friendly JSON output

**When NOT to use:**
- You want human-readable output (use structured)
- You want maximum compression (use dense)

**Example:**

Input:
```
Create a React component for displaying user profiles with avatar and bio
```

Output:
```json
{"g":"create React user profile component","a":"create","i":["avatar","bio"],"d":"frontend","f":"jsx"}
```

---

## Dense mode

**Trigger:** `/marlin dense`

**Pipeline:** input → intent-parser → schema-normalizer(base) → key-shortener(base-keymap) → value-encoder → output-formatter

**What it does:**
- Runs the full compact pipeline first
- Applies value abbreviation (authentication→auth, database→db, etc.)
- Collapses single-item arrays to scalars
- Inlines multi-item arrays as comma-separated strings

**When to use:**
- You are optimizing for cost in high-volume workflows
- You are comfortable reading abbreviated output
- Every token saved matters (batch processing, expensive models)

**When NOT to use:**
- You need human-readable output
- Abbreviated values might cause confusion in your workflow
- You are new to Marlin (start with structured or compact)

**Example:**

Input:
```
Implement authentication middleware that validates JWT tokens against the database
```

Output:
```json
{"g":"impl auth mw for JWT val","a":"create","i":"jwt-token","d":"auth","c":"val-against-db","f":"json"}
```

---

## Domain mode

**Trigger:** `/marlin domain --schema web-api` (or `data-pipeline`, `agent-task`)

**Pipeline:** input → intent-parser(domain-hint) → schema-normalizer(domain-schema) → key-shortener(domain-keymap) → output-formatter

**What it does:**
- Loads a domain-specific schema (e.g., web-api has method, endpoint, auth fields)
- Uses domain-specific key maps for tighter abbreviations
- Maps prompt fields to domain-native terminology
- Combines structural compression with domain knowledge

**Supported domains:**
- `web-api` — REST/GraphQL API endpoints, HTTP methods, middleware
- `data-pipeline` — ETL, source/transform/sink, scheduling, batching
- `agent-task` — AI agent objectives, tools, handoffs, priority

**When to use:**
- You work repeatedly in one domain
- Your prompts consistently describe the same type of task
- You want domain-native field names in the output

**When NOT to use:**
- Your prompt does not fit a supported domain
- You forgot to specify `--schema` (domain mode requires it)

**Example (web-api):**

Input:
```
Build a POST endpoint at /api/users with JWT auth and rate limiting
```

Output:
```json
{"m":"POST","ep":"/api/users","au":"jwt","mw":["rate-limit"],"rf":"json"}
```

---

## V3 DSL bridge

**Trigger:** `/marlin dsl`

**Pipeline:** input → dsl-bridge → output-formatter

**What it does:**
- Converts between V3 internal DSL format and external JSON format
- Internal DSL: `G:build api|A:create|I:email,password|D:auth|F:json`
- External JSON: `{"g":"build api","a":"create","i":["email","password"],"d":"auth","f":"json"}`
- Bidirectional — parse DSL to JSON or serialize JSON to DSL

**When to use:**
- Storing prompts in version control or config files
- Passing prompts between agents (ultra-compact transport format)
- Logging compressed prompts

**When NOT to use:**
- Sending prompts directly to LLMs (always bridge to JSON first)
- You want compression from natural language (use structured/compact/dense first)

See [V3 DSL Format](v3-dsl-format.md) for full specification.
