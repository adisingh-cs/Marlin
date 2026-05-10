# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-05-10

### Added
- Four compression modes: structured, compact, dense, domain
- 11 core skills: marlin-structured, marlin-compact, marlin-dense, marlin-domain, intent-parser, schema-normalizer, key-shortener, value-encoder, output-formatter, token-estimator, dsl-bridge
- V3 DSL internal/external bridge format
- Three domain schemas: web-api, data-pipeline, agent-task
- Base key maps for all modes and domains
- Benchmark harness (`benchmarks/run.py`) and baseline results
- Full test suite for all 11 skills (33+ test cases)
- `validate-skills.py` — skill validation tool
- `generate-catalog.py` — catalog and index generator
- `build-index.py` — filtered index query tool
- `test-skill.py` — API-based skill test runner
- GitHub Actions: validate workflow (PR checks) and catalog workflow (auto-regenerate)
- Issue templates: bug report, skill request, feature request
- Pull request template with contribution checklist
- Skill template for contributors
- Complete documentation suite: architecture, modes, DSL format, key maps, schemas, roadmap, contributing
- Install support: Claude Code, Cursor, Gemini CLI, Codex, Antigravity, npx skills, manual

### Author
Adi Singh — [@adisingh-cs](https://github.com/adisingh-cs) — https://github.com/adisingh-cs
