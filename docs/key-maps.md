# Key Maps

Key maps define the mapping between verbose JSON key names and their
abbreviated equivalents. They are the core data contract for sharp, strike, and
sonar modes.

## How key maps work

1. The root `SKILL.md` mode instructions select the relevant key map
2. It walks every key in the input JSON object
3. If a key exists in the map, it is replaced with the short version
4. If a key is NOT in the map, it passes through unchanged
5. The skill never invents abbreviations — only map-defined ones are used

## Base key map

Used by sharp and strike modes. Located at `schemas/key-maps/base-keymap.json`.

| Full key | Short key | Used by |
|----------|-----------|---------|
| goal | g | All modes |
| action | a | All modes |
| inputs | i | All modes |
| domain | d | All modes |
| constraints | c | All modes |
| format | f | All modes |
| examples | e | All modes |
| output | o | General |
| context | ctx | General |
| type | t | General |
| method | m | Web API |
| auth | au | Web API |
| schema | sc | General |
| version | v | General |
| endpoint | ep | Web API |
| payload | pl | Web API |
| response | rs | General |
| headers | hd | Web API |
| middleware | mw | Web API |
| priority | pr | Agent task |
| objective | obj | Agent task |
| tools | tl | Agent task |
| memory | mem | Agent task |
| handoff | hf | Agent task |
| source | src | Data pipeline |
| transform | tr | Data pipeline |
| sink | sk | Data pipeline |
| schedule | sched | Data pipeline |
| batch-size | bs | Data pipeline |
| retry | rt | Data pipeline |

## Domain key maps

Domain key maps extend the base map with domain-specific abbreviations. They include all base mappings plus additions.

### Web API key map (`web-api-keymap.json`)

Adds to base:

| Full key | Short key |
|----------|-----------|
| response-format | rf |
| content-type | ct |
| status-code | st |
| query-params | qp |
| path-params | pp |
| rate-limit | rl |
| pagination | pg |
| cors | co |
| cache | ca |

### Data pipeline key map (`data-pipeline-keymap.json`)

Adds to base:

| Full key | Short key |
|----------|-----------|
| schema-version | sv |
| partition-key | pk |
| watermark | wm |
| checkpoint | cp |
| parallelism | par |
| window-size | ws |
| dead-letter | dl |
| backfill | bf |
| compression | cmp |
| serialization | ser |

### Agent task key map (`agent-task-keymap.json`)

Adds to base:

| Full key | Short key |
|----------|-----------|
| output-type | ot |
| context-window | cw |
| max-steps | ms |
| temperature | tmp |
| stop-condition | sc |
| fallback | fb |
| escalation | esc |
| retry-policy | rp |
| timeout | to |
| agent-role | ar |
| delegation | del |

## Rules

1. **Maps are additive** — domain maps include all base mappings plus domain-specific ones
2. **Domain maps override base on conflict** — if both define a key, domain wins
3. **Keys not in map pass through unchanged** — unknown keys are preserved as-is
4. **Abbreviations are deterministic** — the same key always maps to the same abbreviation
5. **Maps are bidirectional** — the dsl-bridge uses maps in reverse (short → long) when converting external JSON to readable format

## Contributing new key maps

To add a new domain:
1. Create `schemas/key-maps/{domain}-keymap.json`
2. Include all base map entries plus your domain-specific additions
3. Create a corresponding domain schema at `schemas/v1/{domain}.schema.json`
4. Add support in the sonar section of root `SKILL.md`
5. Add test fixtures covering the new domain
