# Roadmap

Marlin's development is organized into three versions, each building on the previous.

## V1 — Skills-based compression (current)

**Status:** Shipped ✓

V1 is the foundational release. All compression is LLM-assisted — skills guide the model through structured transformation of input prompts.

### Shipped in V1
- Four compression modes: structured, compact, dense, domain
- 11 core skills with full documentation and test coverage
- Base schema + 3 domain schemas (web-api, data-pipeline, agent-task)
- Key maps for all modes and domains
- Output formatting with 4 modes (prompt, report, diff, all)
- Token estimation heuristic
- Benchmark harness with baseline results
- Full tooling: validation, catalog generation, index queries, test runner
- GitHub Actions: PR validation, automatic catalog regeneration
- Install support for Claude Code, Cursor, Gemini CLI, Codex, Antigravity, and 40+ agents

### V1 limitations
- Compression requires an LLM call (skills guide behavior, not execute code)
- Token estimation is heuristic-based (~±10% accuracy)
- No standalone CLI — depends on agent platform
- No programmatic API for non-agent integrations

---

## V2 — Deterministic compression (next)

**Status:** Planned

V2 introduces deterministic compression that does not require an LLM. Compression logic is implemented as executable code (npm package + REST API), enabling one-line installation and zero-cost compression.

### Planned features
- `npm install -g marlin` — CLI tool for local compression
- `npx marlin compress "your prompt" --mode compact` — one-line usage
- REST API endpoint for integration into any pipeline
- Deterministic intent parsing using keyword matching and NLP heuristics
- Exact token counting using tiktoken (GPT) and Anthropic tokenizer libraries
- Offline mode — no API calls needed for compression
- Plugin system for custom schemas and key maps
- VSCode extension for inline prompt compression

### Migration from V1
- All V1 skills remain functional — V2 is additive
- V1 LLM-assisted skills provide higher-quality compression for ambiguous prompts
- V2 deterministic compression is faster and free but may miss nuanced intent
- Users choose: speed+free (V2) or quality (V1) per use case

---

## V3 — Internal DSL format (shipped in V1 build)

**Status:** Shipped ✓ (alongside V1)

V3 introduces the dual-format system — an internal DSL for storage and transport, and an external JSON format for LLM consumption. The dsl-bridge skill handles bidirectional conversion.

### Shipped in V3
- Internal DSL format: `G:build api|A:create|I:email,password|D:auth|F:json`
- External JSON format: `{"g":"build api","a":"create","i":["email","password"],"d":"auth","f":"json"}`
- dsl-bridge skill for bidirectional conversion
- V3 schemas for validation
- Escaping rules for special characters in values

### Future V3 enhancements (post-V2)
- DSL syntax extensions for nested structures
- DSL-native diff format for version control
- Binary-encoded DSL for ultra-compact network transport
- DSL playground web tool for interactive conversion

---

## Long-term vision

Marlin's goal is to become the standard input layer for AI model consumption. Just as gzip compresses HTTP payloads transparently, Marlin should compress prompts transparently — integrated into every agent framework, API client, and developer tool.

The path:
1. **V1:** Prove the concept (skills, schemas, modes) ✓
2. **V2:** Make it accessible (CLI, API, no LLM needed)
3. **V3+:** Make it invisible (auto-compression in agent frameworks)
