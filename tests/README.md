# Tests

Test fixtures for all 11 Marlin skills. Each test file contains an array of test objects that validate skill behavior against expected schemas and reduction targets.

## Structure

All test files are located in `tests/skill-tests/` and follow the naming convention `{skill-name}.test.json`.

## Test object format

```json
{
  "id": "test-001",
  "description": "what this test validates",
  "input": "raw input string or object",
  "mode": "structured|compact|dense|domain|internal",
  "expected_schema": "path to JSON Schema file",
  "expected_fields_present": ["list", "of", "required", "fields"],
  "expected_reduction_min_pct": 20
}
```

## Running tests

### Schema validation (no API key needed)
```bash
python tools/validate-skills.py
```

### Full API-based testing (requires ANTHROPIC_API_KEY)
```bash
export ANTHROPIC_API_KEY=your-key-here
python tools/test-skill.py --skill marlin-compact
python tools/test-skill.py --all
```

## Coverage

| Skill | Test file | Test count |
|-------|-----------|------------|
| marlin-structured | marlin-structured.test.json | 3 |
| marlin-compact | marlin-compact.test.json | 3 |
| marlin-dense | marlin-dense.test.json | 3 |
| marlin-domain | marlin-domain.test.json | 3 |
| intent-parser | intent-parser.test.json | 4 |
| schema-normalizer | schema-normalizer.test.json | 3 |
| key-shortener | key-shortener.test.json | 3 |
| value-encoder | value-encoder.test.json | 3 |
| output-formatter | output-formatter.test.json | 3 |
| token-estimator | token-estimator.test.json | 3 |
| dsl-bridge | dsl-bridge.test.json | 3 |
