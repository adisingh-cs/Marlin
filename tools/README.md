# Tools

Utility scripts for maintaining the Marlin repository. All tools are Python 3.11+ and use stdlib only (no pip dependencies) unless noted.

## Available tools

| Tool | Purpose | Dependencies |
|------|---------|-------------|
| `validate-skills.py` | Validate all SKILL.md files against required structure | stdlib only |
| `generate-catalog.py` | Generate CATALOG.md and skills_index.json from SKILL.md frontmatter | stdlib only |
| `build-index.py` | Query and filter skills_index.json via CLI | stdlib only |
| `test-skill.py` | Run test fixtures against skills via Anthropic API | `anthropic` pip package |

## Usage

```bash
# Validate all skills (run before every PR)
python tools/validate-skills.py

# Regenerate catalog and index
python tools/generate-catalog.py

# Query index by phase, category, or stability
python tools/build-index.py --phase v1
python tools/build-index.py --category compression
python tools/build-index.py --stability stable

# Run tests for a specific skill (requires ANTHROPIC_API_KEY)
python tools/test-skill.py --skill marlin-compact

# Run all tests
python tools/test-skill.py --all
```
