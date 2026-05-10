# V3 DSL Format Specification

The V3 internal DSL is an ultra-compact string format designed for storing, transporting, and version-controlling compressed prompts. It is never sent directly to LLMs — the dsl-bridge skill converts it to external JSON before model consumption.

## Syntax

### Basic format
```
KEY:value|KEY:value|KEY:value
```

### Rules
1. Fields are separated by `|` (pipe character)
2. Key-value pairs use `:` (colon) as delimiter
3. Keys are uppercase, 1–3 characters: `G`, `A`, `I`, `D`, `C`, `F`, `E`
4. No spaces anywhere in the string
5. Maximum length: 500 characters

### Canonical field order
Fields must appear in this order:

| Position | Key | Full name | Required |
|----------|-----|-----------|----------|
| 1 | G | Goal | Yes |
| 2 | A | Action | Yes |
| 3 | I | Inputs | Yes |
| 4 | D | Domain | No |
| 5 | C | Constraints | No |
| 6 | F | Format | No |
| 7 | E | Examples | No |

Extra fields (non-standard) are appended alphabetically after E.

### Array handling
- Arrays are comma-separated inline, no brackets
- `I:email,password,token` → JSON: `"i": ["email", "password", "token"]`
- Single-value arrays use no commas: `I:email` → JSON: `"i": ["email"]`

### Escaping
- If a value contains `|`, wrap the entire value in double quotes: `G:"value|with|pipes"`
- If a value contains `:`, wrap the entire value in double quotes: `G:"key:value"`
- Double quotes within quoted values are escaped as `\"`
- Commas within quoted values are treated as literal characters, not array delimiters

## Examples

### Simple prompt
```
G:build login api|A:create|I:email,password|D:auth|C:jwt-only|F:json
```

Bridges to:
```json
{"g":"build login api","a":"create","i":["email","password"],"d":"auth","c":["jwt-only"],"f":"json"}
```

### Data pipeline
```
G:process sales data|A:transform|I:sales-csv,revenue-col|D:data-pipeline|C:filter-nulls,sort-desc|F:parquet
```

Bridges to:
```json
{"g":"process sales data","a":"transform","i":["sales-csv","revenue-col"],"d":"data-pipeline","c":["filter-nulls","sort-desc"],"f":"parquet"}
```

### Escaped values
```
G:"parse key:value config"|A:read|I:config-file|F:json
```

Bridges to:
```json
{"g":"parse key:value config","a":"read","i":["config-file"],"f":"json"}
```

### Optional fields omitted
```
G:sort numbers|A:sort|I:number-array
```

Bridges to:
```json
{"g":"sort numbers","a":"sort","i":["number-array"]}
```

## Conversion rules

### Internal DSL → External JSON
1. Split string on `|` (respecting quoted values)
2. For each segment, split on first `:` to separate key from value
3. Map uppercase DSL keys to lowercase JSON keys (G→g, A→a, etc.)
4. If value contains commas (unquoted), convert to JSON array
5. If value has no commas, keep as scalar string (bridge wraps in array for `i`, `c`, `e` fields)
6. Build JSON object
7. Return valid JSON

### External JSON → Internal DSL
1. Read JSON object
2. Map lowercase keys to uppercase DSL codes (g→G, a→A, etc.)
3. For array values, join elements with commas (no spaces)
4. For null values, omit the field entirely
5. For string values, check if escaping is needed (contains `|` or `:`)
6. Serialize in canonical field order: G|A|I|D|C|F|E
7. Strip all spaces
8. Return DSL string

## When to use V3 DSL

| Use case | Recommended |
|----------|-------------|
| Storing compressed prompts in git | ✓ DSL |
| Agent-to-agent prompt passing | ✓ DSL (bridge at consumption) |
| Ultra-compact logging | ✓ DSL |
| Environment variables | ✓ DSL |
| Config files | ✓ DSL |
| Sending to LLMs | ✗ Always bridge to JSON first |
| Human review | ✗ Use JSON for readability |

## Why raw DSL is never sent to LLMs

LLMs are trained on natural language and common structured formats (JSON, YAML, XML). The pipe-delimited DSL format is not in their training distribution. Sending raw DSL to a model would likely confuse it, produce unpredictable results, or waste tokens on the model trying to parse an unfamiliar format.

The bridge to external JSON ensures the model receives a format it handles natively, while the DSL format optimizes for machine-to-machine transport and human storage.
