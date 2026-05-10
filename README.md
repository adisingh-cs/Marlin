<!-- assets/logo.png -->
<p align="center">
  <img src="https://i.ibb.co/hRghHfj9/logo.png" alt="Marlin" width="200"/>
</p>

<h1 align="center">Marlin</h1>
<p align="center"><em>Swift input. Sharp output. Every token counts.</em></p>

<p align="center">
  <a href="#install">Install</a> •
  <a href="#modes">Modes</a> •
  <a href="#usage">Usage</a> •
  <a href="#v3-dsl">V3 DSL</a> •
  <a href="docs/roadmap.md">Roadmap</a> •
  <a href="CONTRIBUTING.md">Contributing</a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/version-1.0.0-blue" alt="version"/>
  <img src="https://img.shields.io/badge/license-MIT-green" alt="license"/>
  <img src="https://img.shields.io/badge/skills-claude--code%20%7C%20cursor%20%7C%20antigravity%20%7C%2040%2B%20agents-purple" alt="platforms"/>
</p>

---

**Marlin** compresses what you send *to* the model — not what the model says back.
It restructures verbose prompts into lean, schema-anchored representations.
The model receives a cleaner, denser signal and returns sharper, more deterministic output.

Input tokens cost money. Verbose prompts waste context window. Marlin fixes the input side.

---

## Install

**One command. Works globally across all your projects.**

```bash
npx skills add adisingh-cs/Marlin -g -a antigravity
```

Replace `-a antigravity` with your agent:

| Agent | Command |
|---|---|
| Antigravity | `npx skills add adisingh-cs/Marlin -g -a antigravity` |
| Claude Code | `npx skills add adisingh-cs/Marlin -g -a claude-code` |
| Cursor | `npx skills add adisingh-cs/Marlin -g -a cursor` |
| All agents | `npx skills add adisingh-cs/Marlin -g` |

**Manual install (any agent that supports SKILL.md):**
```bash
git clone https://github.com/adisingh-cs/Marlin.git
# Copy SKILL.md into your agent's skills folder
```

> 💡 One-liner installs for Gemini CLI, Codex, and OpenCode coming in V2.

---

## Modes

Four modes. One command prefix. You pick the intensity.

| Command | Intensity | Token Reduction | Best For |
|---|---|---|---|
| `/marlin swift` | Light | ~20–35% | General prompts, first use |
| `/marlin sharp` | Mid | ~35–50% | API calls, repeated workflows |
| `/marlin strike` | Max | ~50–70% | High-volume, cost-sensitive |
| `/marlin sonar` | Domain | ~40–65% | Web-API, data, agent tasks |

---

## Usage

### /marlin swift — normalize and structure

```
/marlin swift

I want to build a login endpoint that takes email and password,
checks against the database, and returns a JWT token if valid.
Only use PostgreSQL. Output as JSON.
```

Output:
```json
{
  "goal": "build login endpoint",
  "action": "create",
  "inputs": ["email", "password"],
  "domain": "authentication",
  "constraints": ["PostgreSQL only"],
  "format": "json"
}
```
> Original: ~38 tokens → Compressed: ~28 tokens → Saved: ~26%

---

### /marlin sharp — compact JSON, short keys

```
/marlin sharp

I want to build a login endpoint that takes email and password,
checks against the database, and returns a JWT token if valid.
Only use PostgreSQL. Output as JSON.
```

Output:
```json
{"g":"build login endpoint","a":"create","i":["email","password"],"d":"authentication","c":["PostgreSQL only"],"f":"json"}
```
> Original: ~38 tokens → Compressed: ~22 tokens → Saved: ~42%

---

### /marlin strike — maximum compression

```
/marlin strike

I want to build a login endpoint that takes email and password,
checks against the database, and returns a JWT token if valid.
Only use PostgreSQL. Output as JSON.
```

Output:
```json
{"g":"build login ep","a":"create","i":"email,password","d":"auth","c":"PostgreSQL only","f":"json"}
```
> Original: ~38 tokens → Compressed: ~18 tokens → Saved: ~53%

---

### /marlin sonar — domain-aware compression

```
/marlin sonar --schema web-api

Create a POST endpoint at /api/users/login that accepts email and
password in the request body, validates with JWT, returns tokens.
Requires Authorization header. Version 2.
```

Output:
```json
{"mth":"POST","ep":"/api/users/login","au":"jwt","pl":["email","password"],"hd":["Authorization"],"rf":"json","v":"2"}
```
> Original: ~42 tokens → Compressed: ~21 tokens → Saved: ~50%

Available schemas: `--schema web-api` · `--schema data-pipeline` · `--schema agent-task`

---

## Output Flags

Append to any command:

| Flag | Returns |
|---|---|
| `--prompt` | Compressed prompt only — ready to paste |
| `--report` | Compressed + token savings report *(default)* |
| `--diff` | Original vs compressed side by side |
| `--all` | Everything |

Example: `/marlin sharp --diff`

---

## V3 DSL

For agent-to-agent passing and ultra-compact storage:

```
# Internal DSL (store/pass between agents)
G:build login ep|A:create|I:email,password|D:auth|F:json

# Bridge to JSON before sending to any LLM
/marlin bridge G:build login ep|A:create|I:email,password|D:auth|F:json
```

Append `--dsl` to any mode command for DSL output.

---

## Quick Reference

```
/marlin swift          Normalize + structure  (~20–35%)
/marlin sharp          Compact + short keys   (~35–50%)
/marlin strike         Maximum compression    (~50–70%)
/marlin sonar          Domain schema          (~40–65%)

--prompt   Compressed prompt only
--report   Prompt + savings report (default)
--diff     Side-by-side comparison
--all      Everything
--dsl      V3 internal DSL format
```

---

## Works great with caveman

Marlin compresses **input**. [caveman](https://github.com/JuliusBrussee/caveman)
compresses **output**. Run both — save on both ends.

---

## Benchmarks

> 🚧 Benchmark results coming in V1.1 — harness is ready.
> Run it yourself: `cd benchmarks && python run.py` (requires `ANTHROPIC_API_KEY`)

---

## Roadmap

- **V1 (now):** Single SKILL.md, four modes, npx install, V3 DSL
- **V2:** npm package + REST API — deterministic compression, no LLM needed
- **V3:** Multi-agent pipeline support, domain schema expansion

[Full roadmap →](docs/roadmap.md)

---

## Contributing

Contributions welcome — new domain schemas, key maps, examples,
benchmark results. Read [CONTRIBUTING.md](CONTRIBUTING.md) first.

---

## Attribution

MIT License. Free to use, fork, and build on.
If Marlin saves you tokens, a ⭐ or a mention helps others find it.
[ATTRIBUTION.md](ATTRIBUTION.md)

---

<p align="center">
  Built by <a href="https://github.com/adisingh-cs">@adisingh-cs</a> — Aditya Singh
</p>
