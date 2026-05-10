# Contributing to Marlin

Welcome! Marlin thrives on community contributions. Whether you're building a new compression skill, fixing a schema bug, improving documentation, or adding benchmark data — every contribution makes Marlin sharper. You don't need to be an expert in prompt engineering or LLMs to help. If you use AI tools and have ideas about how prompts can be structured better, you belong here.

## What makes a good skill contribution

A strong skill contribution includes:

1. **A complete `SKILL.md`** with all required frontmatter fields filled (see below)
2. **A corresponding test file** at `tests/skill-tests/{skill-name}.test.json` with at least 3 test cases
3. **At least 2 realistic examples** showing input → output transformation (no lorem ipsum)
4. **Passing validation** — run `python tools/validate-skills.py` before submitting
5. **Clear documentation** — the skill body must explain what the skill does, when to use it, when not to use it, and how it chains with other skills

## Contribution types

| Type | Branch prefix | Description |
|------|--------------|-------------|
| New skill | `skill/skill-name` | A new compression, parsing, encoding, or utility skill |
| New schema | `schema/schema-name` | A new domain schema (JSON Schema draft-07) |
| New domain keymap | `keymap/domain-name` | A new key abbreviation map for a specific domain |
| Bug fix | `fix/description` | Fix to an existing skill, schema, tool, or workflow |
| Benchmark | `bench/description` | New benchmark data, improved test prompts, or methodology improvements |
| Documentation | `docs/topic` | Documentation improvements, guides, or corrections |

## How to submit

1. **Fork** the repository
2. **Create a branch** using the naming convention above
3. **Make your changes** — follow all conventions described in this guide
4. **Run validation locally:** `python tools/validate-skills.py`
5. **Regenerate the catalog:** `python tools/generate-catalog.py`
6. **Open a Pull Request** against `main`
7. **Fill out the PR template** completely — CI must pass before review

## SKILL.md requirements

Every SKILL.md must include this frontmatter with valid values:

| Field | Required | Allowed values |
|-------|----------|----------------|
| `name` | Yes | Must match folder name exactly (kebab-case) |
| `version` | Yes | Semantic version (e.g., `1.0.0`) |
| `author` | Yes | GitHub username |
| `project` | Yes | `marlin` |
| `phase` | Yes | `v1`, `v3` |
| `category` | Yes | `compression`, `parsing`, `schema`, `encoding`, `formatting`, `estimation`, `bridge` |
| `tags` | Yes | Array of strings |
| `input_format` | Yes | `natural-language`, `json`, `compact-json`, `dsl` |
| `output_format` | Yes | `structured-json`, `compact-json`, `dense-json`, `dsl`, `report`, `diff` |
| `token_impact` | Yes | `high`, `medium`, `low`, `none` |
| `stability` | Yes | `stable`, `experimental` |
| `trigger` | Yes | Command string or `internal` |

### Required body sections

- **Description** — what the skill does
- **When to trigger** — exact conditions for activation
- **Do NOT trigger when** — exclusion conditions
- **Steps** — numbered pipeline steps
- **Examples** — at least 2 complete input/output pairs
- **Related Skills** — which skills this chains with

## What not to submit

- **Binary files** — no images, compiled binaries, or archives (except in `assets/` with `.gitkeep`)
- **API keys or secrets** — never commit credentials of any kind
- **Skills without test fixtures** — every skill needs a test file
- **Duplicate skills** — if your skill overlaps with an existing one, explain the measurable improvement
- **Placeholder content** — no TODOs, no "fill in later", no lorem ipsum
- **camelCase filenames** — use kebab-case for everything

## Code of conduct

Marlin is an inclusive, respectful project. Treat every contributor — regardless of experience level, background, or perspective — with dignity and professionalism. Constructive feedback is welcome; personal attacks, harassment, and dismissive behavior are not. We build tools that help everyone work better, and that starts with how we work together.

## Credits

All contributors are credited in [CHANGELOG.md](CHANGELOG.md). If your contribution is merged, your GitHub username will be listed alongside the change. If you prefer anonymity, let us know in your PR.
