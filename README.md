<p align="center">
  <img src="https://i.ibb.co/hRghHfj9/logo.png" alt="Marlin Logo" width="200"><br>
  <strong>Marlin</strong><br>
  <em>Swift input. Sharp output. Every token counts.</em>
</p>

<p align="center">
  <a href="#install">Install</a> •
  <a href="#modes">Modes</a> •
  <a href="#architecture">Architecture</a> •
  <a href="docs/roadmap.md">Roadmap</a> •
  <a href="CONTRIBUTING.md">Contributing</a>
</p>

---

**Marlin** is an AI-native input prompt optimizer. It compresses what you send *to* the model — not what the model says back. Using structured schemas, key maps, and domain-aware compression, Marlin reduces input tokens by **28–66%** while improving prompt determinism and reducing hallucination.

Marlin never changes what the model says. It changes what the model reads.

## Why input compression?

| Problem | Marlin's approach |
|---------|------------------|
| Verbose prompts waste tokens and money | Schema-based structural compression, not heuristic trimming |
| Ambiguous input produces inconsistent output | Canonical fields force explicit intent |
| Context windows fill up in long sessions | 50–66% input savings means 2–3× more room for everything else |
| Input optimization is ignored by most tools | Marlin is purpose-built for the input side |

> **Not an output compressor.** Tools like `caveman` compress model *responses*. Marlin compresses model *input*. They are independent and composable — stack them for maximum savings.

## Install

### Claude Code

> 🚧 **One-liner install coming in V2** (npm package in progress)
>
> ```bash
> # Coming soon — V2
> # claude mcp add marlin -- npx -y marlin-skills@latest
> ```

**Install now (manual):**
```bash
git clone https://github.com/adisingh-cs/Marlin.git
# Copy skills/marlin-{mode}/SKILL.md into your Claude Code skills folder
# Or add the skills/ directory to your Claude Code config
```

### Cursor

> 🚧 **One-liner install coming in V2** (npm package in progress)
>
> ```bash
> # Coming soon — V2
> # npx skills add adisingh-cs/marlin -a cursor
> ```

**Install now (manual):**
```bash
git clone https://github.com/adisingh-cs/Marlin.git
# Copy skills/marlin-{mode}/SKILL.md into .cursor/skills/
```

### Gemini CLI

> 🚧 **One-liner install coming in V2** (npm package in progress)
>
> ```bash
> # Coming soon — V2
> # gemini extensions install https://github.com/adisingh-cs/Marlin
> ```

**Install now (manual):**
```bash
git clone https://github.com/adisingh-cs/Marlin.git
# Copy skills/marlin-{mode}/SKILL.md into your Gemini CLI skills folder
```

### Codex

> 🚧 **One-liner install coming in V2** (npm package in progress)
>
> ```bash
> # Coming soon — V2
> # npx skills add adisingh-cs/marlin -a codex
> ```

**Install now (manual):**
```bash
git clone https://github.com/adisingh-cs/Marlin.git
# Copy skills/marlin-{mode}/SKILL.md into your Codex skills folder
```

### Antigravity

**Works now:**
```json
{
  "skills": ["github:adisingh-cs/Marlin"]
}
```

Or via npx skills:
```bash
npx skills add adisingh-cs/Marlin -a antigravity
```

### Any other agent (manual install — works now)

```bash
git clone https://github.com/adisingh-cs/Marlin.git
```
Then copy the relevant `skills/marlin-{mode}/SKILL.md` file into your agent's skills directory.

Choose the mode that fits your workflow:
- `skills/marlin-structured/` — normalized schema output
- `skills/marlin-compact/` — short keys + minified JSON
- `skills/marlin-dense/` — maximum compression
- `skills/marlin-domain/` — domain-specific schemas (web-api, data-pipeline, agent-task)

> 💡 **V2 Roadmap:** The npm package (`marlin-skills`) and one-liner installs for all platforms are coming in V2 alongside deterministic offline compression. [See roadmap →](docs/roadmap.md)

## Modes

| Mode | Command | Reduction | Best for |
|------|---------|-----------|----------|
| **Structured** | `/marlin structured` | 20–35% | First-time users, readable output |
| **Compact** | `/marlin compact` | 35–50% | API calls, agent pipelines |
| **Dense** | `/marlin dense` | 50–70% | High-volume, cost-sensitive |
| **Domain** | `/marlin domain --schema <name>` | 40–65% | Specialized workflows |
| **DSL** | `/marlin dsl` | (conversion) | Storage, transport |

### Quick example

**Input:**
```
Build a REST API endpoint for user registration with email validation,
password hashing, and JWT token generation. Use Express.js and MongoDB.
```

**Structured** (`/marlin structured`):
```json
{
  "goal": "build REST API endpoint for user registration",
  "action": "create",
  "inputs": ["email", "password"],
  "domain": "web-api",
  "constraints": ["email-validation", "password-hashing", "JWT-generation"],
  "format": "json",
  "examples": null
}
```

**Compact** (`/marlin compact`):
```json
{"g":"build REST API for user registration","a":"create","i":["email","password"],"d":"web-api","c":["email-val","pw-hash","JWT-gen"],"f":"json"}
```

**Dense** (`/marlin dense`):
```json
{"g":"build REST API for user reg","a":"create","i":"email,password","d":"web-api","c":"email-val,pw-hash,JWT-gen","f":"json"}
```

**Domain** (`/marlin domain --schema web-api`):
```json
{"m":"POST","ep":"/api/users","au":"jwt","mw":["validation","hashing"],"pl":["email","password"],"rf":"json"}
```

See [docs/modes.md](docs/modes.md) for complete mode documentation.

## Architecture

Marlin uses a pipeline architecture where skills chain together:

```
input → intent-parser → schema-normalizer → key-shortener → value-encoder → output-formatter
```

Each skill performs one transformation. Schemas anchor the data contract at every stage. The output formatter is decoupled from compression logic.

See [docs/architecture.md](docs/architecture.md) for the full system diagram.

## Skills

Marlin ships with 11 core skills:

| Skill | Category | Purpose |
|-------|----------|---------|
| `marlin-structured` | compression | Entry point for structured mode |
| `marlin-compact` | compression | Entry point for compact mode |
| `marlin-dense` | compression | Entry point for dense mode |
| `marlin-domain` | compression | Entry point for domain mode |
| `intent-parser` | parsing | Extract goal, action, inputs from natural language |
| `schema-normalizer` | schema | Enforce schema contracts and type coercion |
| `key-shortener` | encoding | Replace verbose keys with abbreviations |
| `value-encoder` | encoding | Abbreviate common technical terms |
| `output-formatter` | formatting | Format output as prompt, report, diff, or all |
| `token-estimator` | estimation | Estimate token count for input/output |
| `dsl-bridge` | bridge | Convert between V3 DSL and external JSON |

See [CATALOG.md](CATALOG.md) for the auto-generated skill catalog.

## Domains

Three domain schemas ship with V1:

| Domain | Schema | Key map | Use case |
|--------|--------|---------|----------|
| `web-api` | HTTP methods, endpoints, auth | `web-api-keymap.json` | REST/GraphQL APIs |
| `data-pipeline` | Source, transform, sink, schedule | `data-pipeline-keymap.json` | ETL, data processing |
| `agent-task` | Objective, tools, handoff, priority | `agent-task-keymap.json` | AI agent workflows |

See [docs/schemas.md](docs/schemas.md) for field-level schema documentation.

## Benchmark results

Baseline results from 10 test prompts across all modes:

| Mode | Avg. token reduction |
|------|---------------------|
| Structured | 28% |
| Compact | 44% |
| Dense | 61% |
| Domain | 52% |

Run your own benchmarks:
```bash
export ANTHROPIC_API_KEY=your-key
python benchmarks/run.py
```

## Documentation

| Document | Description |
|----------|-------------|
| [Architecture](docs/architecture.md) | System design, pipeline diagrams, skill dependencies |
| [Modes](docs/modes.md) | Complete guide to all compression modes |
| [Schemas](docs/schemas.md) | JSON Schema reference for all schemas |
| [Key Maps](docs/key-maps.md) | Key abbreviation tables and rules |
| [V3 DSL Format](docs/v3-dsl-format.md) | Internal DSL specification |
| [Skill Anatomy](docs/skill-anatomy.md) | How to read and write SKILL.md files |
| [Why Input Matters](docs/why-input-matters.md) | The case for input-side optimization |
| [Roadmap](docs/roadmap.md) | V1, V2, V3 plans |
| [Contributing Skills](docs/contributing-skills.md) | How to design and submit new skills |

## Tools

```bash
# Validate all skills
python tools/validate-skills.py

# Generate catalog
python tools/generate-catalog.py

# Query skill index
python tools/build-index.py --phase v1

# Run tests (offline)
python tools/test-skill.py --all --offline

# Run tests (with API)
export ANTHROPIC_API_KEY=your-key
python tools/test-skill.py --all
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines and [docs/contributing-skills.md](docs/contributing-skills.md) for skill-specific guidance.

## License

[MIT](LICENSE) — use freely, attribution appreciated ([ATTRIBUTION.md](ATTRIBUTION.md)).
