---
name: marlin
description: Compress and restructure input prompts into lean schema-anchored representations for any AI model. Use when the user runs /marlin swift, /marlin sharp, /marlin strike, or /marlin sonar to reduce input token cost and improve model output quality.
license: MIT
metadata:
  author: adisingh-cs
  github: https://github.com/adisingh-cs/Marlin
  version: "1.0.0"
---

# Marlin

> *Swift input. Sharp output. Every token counts.*

Marlin compresses what you send **to** the model — not what the model
says back. It restructures verbose natural language prompts into lean,
schema-anchored representations. The model receives a cleaner, denser
signal and returns sharper, more deterministic output.

**Four modes. One command prefix. You pick the intensity.**

---

## Modes

| Command | Mode | Token Reduction | Best For |
|---|---|---|---|
| `/marlin swift` | Structured | ~20–35% | General prompts, first use |
| `/marlin sharp` | Compact | ~35–50% | API calls, repeated workflows |
| `/marlin strike` | Dense | ~50–70% | High-volume, cost-sensitive |
| `/marlin sonar` | Domain | ~40–65% | Web-API, data pipelines, agents |

---

## Output Flags (optional, append to any command)

| Flag | Returns |
|---|---|
| `--prompt` | Compressed prompt only — ready to paste |
| `--report` | Compressed prompt + token savings count + reduction % |
| `--diff` | Original vs compressed side by side |
| `--all` | Everything above |

Default if no flag: `--report`

Example: `/marlin sharp --diff`

---

## /marlin swift

**What it does:** Normalizes your prompt into a fixed, unambiguous
schema. Removes filler, resolves intent, enforces canonical field
names. Lightest compression — best when clarity matters more than
maximum savings.

**Pipeline:**
1. Read the raw prompt
2. Extract: goal, action, inputs, domain, constraints, format, examples
3. Map to canonical field names using these aliases:
   - goal ← objective, purpose, task, want, need, build, create, make
   - action ← verb, operation, do, perform, run, execute, generate, write
   - inputs ← params, args, fields, data, variables, values, given
   - domain ← context, area, topic, category, subject, about, for
   - constraints ← limits, rules, must, cannot, only, never, requirements
   - format ← output, return, response, give me, show me, as
   - examples ← like, e.g., for example, such as, sample
4. Set missing fields to null — never omit, never invent
5. Default format to "json" if null
6. Output structured JSON matching this schema:
   ```
   {
     "goal": string (required, max 100 chars),
     "action": string (required),
     "inputs": [string] (required, coerce scalar to array),
     "domain": string | null,
     "constraints": [string] | null,
     "format": string (default: "json"),
     "examples": [string] | null
   }
   ```
7. Apply output flag (default: --report)

**Example:**

Input:
```
I want to build a login endpoint that takes email and password,
checks against the database, and returns a JWT token if valid.
Only use PostgreSQL. Output as JSON.
```

Output (--report):
```json
{
  "goal": "build login endpoint",
  "action": "create",
  "inputs": ["email", "password"],
  "domain": "authentication",
  "constraints": ["PostgreSQL only"],
  "format": "json",
  "examples": null
}
```
Original: ~38 tokens | Compressed: ~28 tokens | Saved: ~26%

---

## /marlin sharp

**What it does:** Runs swift normalization first, then applies key
shortening and JSON minification. Keys become single letters. All
whitespace stripped. Null fields dropped. Best balance of compression
and readability.

**Key map (apply exactly — never invent abbreviations):**
```
goal → g          action → a        inputs → i
domain → d        constraints → c   format → f
examples → e      output → o        context → ctx
type → t          method → m        auth → au
schema → sc       version → v       endpoint → ep
payload → pl      response → rs     headers → hd
middleware → mw   priority → pr     objective → obj
tools → tl        memory → mem      handoff → hf
source → src      transform → tr    sink → sk
schedule → sched  batch-size → bs   retry → rt
```

**Pipeline:**
1. Run full swift normalization
2. Apply key map — replace every verbose key with its short form
3. Drop all null/empty fields (do not include them)
4. Strip all whitespace between tokens
5. Apply output flag

**Example:**

Input (same as above)

Output (--report):
```json
{"g":"build login endpoint","a":"create","i":["email","password"],"d":"authentication","c":["PostgreSQL only"],"f":"json"}
```
Original: ~38 tokens | Compressed: ~22 tokens | Saved: ~42%

---

## /marlin strike

**What it does:** Runs sharp compression first, then applies value
abbreviation. Most aggressive V1 mode. Collapses arrays where possible.
Best for high-volume pipelines where every token counts.

**Value abbreviation table (apply only these — never abbreviate
values shorter than 5 chars, never abbreviate proper nouns,
identifiers, URLs, or file paths):**
```
authentication → auth     authorization → authz
generate → gen            endpoint → ep
request → req             response → res
parameter → param         function → fn
database → db             configuration → cfg
interface → iface         implementation → impl
validation → val          middleware → mw
repository → repo         component → comp
dependency → dep          environment → env
infrastructure → infra    deployment → deploy
documentation → docs      integration → integ
application → app         development → dev
production → prod         management → mgmt
```

**Pipeline:**
1. Run full sharp compression
2. Apply value abbreviation table to all string values
3. Collapse single-item arrays to scalar string
4. Comma-separate multi-value arrays inline, remove brackets
5. Apply output flag

**Example:**

Input (same as above)

Output (--report):
```json
{"g":"build login ep","a":"create","i":"email,password","d":"auth","c":"PostgreSQL only","f":"json"}
```
Original: ~38 tokens | Compressed: ~18 tokens | Saved: ~53%

---

## /marlin sonar

**What it does:** Domain-aware compression. User specifies a domain
and Marlin applies a specialist schema with domain-specific field
maps and value abbreviations. Combines sharp compression with
domain-optimised structure.

**Usage:** `/marlin sonar --schema web-api`
Available schemas: `web-api`, `data-pipeline`, `agent-task`

**Schema: web-api**
Fields: method, endpoint, auth, payload, headers, response-format,
version, middleware
Key map extension: method→mth, endpoint→ep, auth→au, payload→pl,
headers→hd, response-format→rf, version→v, middleware→mw

Example input:
```
Create a POST endpoint at /api/users/login that accepts email and
password in the request body, validates with JWT, returns access
token and refresh token. Requires Authorization header. Version 2.
```

Example output (--report):
```json
{"mth":"POST","ep":"/api/users/login","au":"jwt","pl":["email","password"],"hd":["Authorization"],"rf":"json","v":"2"}
```
Original: ~42 tokens | Compressed: ~21 tokens | Saved: ~50%

---

**Schema: data-pipeline**
Fields: source, transform, sink, schedule, format, batch-size,
retry, schema-version
Key map extension: source→src, transform→tr, sink→sk,
schedule→sched, format→f, batch-size→bs, retry→rt,
schema-version→sv

Example input:
```
Read customer records from PostgreSQL every hour, transform by
removing nulls and normalizing email to lowercase, write to
BigQuery. Batch size 500. Retry 3 times on failure. JSON format.
```

Example output (--report):
```json
{"src":"PostgreSQL","tr":["remove nulls","normalize email lowercase"],"sk":"BigQuery","sched":"hourly","f":"json","bs":500,"rt":3}
```
Original: ~44 tokens | Compressed: ~24 tokens | Saved: ~45%

---

**Schema: agent-task**
Fields: objective, tools, memory, output-type, constraints,
handoff, priority, context-window
Key map extension: objective→obj, tools→tl, memory→mem,
output-type→ot, constraints→c, handoff→hf, priority→pr,
context-window→cw

Example input:
```
Search the web for recent AI papers published in the last 7 days,
summarize each one in 3 bullet points, save results to a markdown
file. Use web search and file write tools. High priority.
Pass results to the report-writer agent when done.
```

Example output (--report):
```json
{"obj":"find and summarize recent AI papers","tl":["web-search","file-write"],"ot":"markdown","c":["last 7 days","3 bullets each"],"hf":"report-writer","pr":"high"}
```
Original: ~52 tokens | Compressed: ~26 tokens | Saved: ~50%

---

## V3 DSL Format

For agent-to-agent passing and ultra-compact storage, Marlin supports
an internal DSL format. Never send raw DSL to an LLM — always bridge
to JSON first.

**Internal DSL (store and pass between agents):**
```
G:build login ep|A:create|I:email,password|D:auth|C:PostgreSQL only|F:json
```

**External JSON (send to model):**
```json
{"g":"build login ep","a":"create","i":["email","password"],"d":"auth","c":["PostgreSQL only"],"f":"json"}
```

**DSL rules:**
- Fields separated by `|`
- Key:value pairs using `:`
- Array values comma-separated, no brackets
- No spaces anywhere
- Field order: G → A → I → D → C → F → E

To convert: append `--dsl` to any command for DSL output.
To bridge DSL → JSON for a model call: `/marlin bridge <dsl-string>`

---

## Composing with other tools

Marlin compresses **input**. Tools like caveman compress **output**.
Run both to save on both ends:

1. `/marlin sharp` → compressed prompt sent to model
2. Model generates response with caveman active → compressed output

Stack the savings. They solve different halves of the same problem.

---

## Quick Reference

```
/marlin swift          Normalize + structure (~20-35% savings)
/marlin sharp          Compact JSON + short keys (~35-50% savings)
/marlin strike         Maximum compression (~50-70% savings)
/marlin sonar          Domain schema compression (~40-65% savings)

Flags (append to any):
  --prompt             Compressed prompt only
  --report             Prompt + token savings (default)
  --diff               Side-by-side comparison
  --all                Everything
  --dsl                Output as V3 internal DSL
  --schema web-api     Domain schema (sonar mode only)
  --schema data-pipeline
  --schema agent-task
```

---

*Built by [@adisingh-cs](https://github.com/adisingh-cs) —
[github.com/adisingh-cs/Marlin](https://github.com/adisingh-cs/Marlin)*

*MIT License — free to use, fork, and build on.*
*If Marlin saves you tokens, a ⭐ or mention is appreciated.*
