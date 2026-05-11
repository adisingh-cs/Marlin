# Contributing to Marlin

Welcome. Marlin is a single-skill input prompt optimizer. Contributions should
make the root skill clearer, add useful schemas/key maps, improve examples, or
strengthen benchmark evidence.

## What Makes A Good Contribution

A strong contribution includes:

1. A focused update to root `SKILL.md` or the supporting schema/docs files.
2. Matching examples when behavior changes.
3. Tests for benchmark harness changes.
4. Benchmark results when changing token-savings claims.
5. Clear notes about methodology and limitations.

## Contribution Types

| Type | Branch prefix | Description |
|---|---|---|
| Skill behavior | `skill/description` | Updates to root `SKILL.md` |
| New schema | `schema/domain-name` | New domain schema and key map |
| Benchmark | `bench/description` | Prompt corpus, runner, or methodology changes |
| Documentation | `docs/topic` | Docs, examples, or install guidance |
| Bug fix | `fix/description` | Corrections to behavior, docs, or tooling |

## Local Validation

Run unit tests:

```bash
python -m unittest discover -s tests
```

Run the OpenRouter benchmark when changing claims:

```bash
export OPENROUTER_API_KEY="sk-or-..."
python benchmarks/run.py --model "openai/gpt-4o-mini"
```

You can also pass the key directly:

```bash
python benchmarks/run.py --api-key "sk-or-..." --model "openai/gpt-4o-mini"
```

Avoid committing API keys, `.env` files, or private benchmark outputs that
contain sensitive data.

## Skill Requirements

Marlin V1 uses one root `SKILL.md`. Keep it aligned with:

- `/marlin swift`
- `/marlin sharp`
- `/marlin strike`
- `/marlin sonar --schema web-api|data-pipeline|agent-task`
- `schemas/v1/*.schema.json`
- `schemas/key-maps/*.json`
- `examples/`
- `benchmarks/README.md`
- agent rule files such as `AGENTS.md`, `GEMINI.md`, and Cursor/Windsurf/Cline
  rules

## Benchmark Claims

Do not present design targets as benchmark-backed results. Published benchmark
claims should include:

- OpenRouter model id.
- Prompt corpus.
- Mode list.
- Original and compressed token counts.
- Absolute and percent savings.
- Compression-system overhead.
- Whether counts are heuristic or tokenizer-accurate.

## What Not To Submit

- API keys or secrets.
- Placeholder examples.
- Token-savings claims without results.
- New abbreviations that are not represented in key maps.
- Unrelated refactors bundled with benchmark or skill changes.

## Credits

Contributors are credited in release notes when their changes are merged.
