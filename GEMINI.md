# Marlin — Input Prompt Optimizer

> Swift input. Sharp output. Every token counts.

Marlin compresses what you send to the model — not what the model
says back. Use /marlin followed by a mode name before any prompt.

## Modes

- `/marlin swift` — normalize and structure (~20-35% token cut)
- `/marlin sharp` — compact JSON + short keys (~35-50% token cut)
- `/marlin strike` — maximum compression (~50-70% token cut)
- `/marlin sonar --schema web-api|data-pipeline|agent-task` — domain schema (~40-65% token cut)

## Output flags (append to any command)

- `--prompt` — compressed prompt only
- `--report` — compressed prompt + token savings (default)
- `--diff` — original vs compressed side by side
- `--all` — everything

## /marlin swift

Normalize intent to fixed schema. Extract: goal, action, inputs,
domain, constraints, format, examples. Set missing to null.
Default format: "json".

Output:
```json
{"goal":"...","action":"...","inputs":[...],"domain":"...","constraints":[...],"format":"json"}
```

## /marlin sharp

Run swift first. Then apply key map and minify:
goal→g, action→a, inputs→i, domain→d, constraints→c, format→f,
examples→e, output→o, context→ctx, type→t, method→m, auth→au,
schema→sc, version→v, endpoint→ep, payload→pl, response→rs,
headers→hd, middleware→mw

Strip all whitespace. Drop null fields.

## /marlin strike

Run sharp first. Then abbreviate values:
authentication→auth, generate→gen, endpoint→ep, request→req,
response→res, parameter→param, function→fn, database→db,
configuration→cfg, interface→iface, implementation→impl,
validation→val, repository→repo, deployment→deploy, environment→env

Collapse single-item arrays to scalar.
Comma-separate multi-value arrays, remove brackets.

## /marlin sonar

Run sharp with domain-specific schema.
--schema web-api: method, endpoint, auth, payload, headers, response-format, version, middleware
--schema data-pipeline: source, transform, sink, schedule, format, batch-size, retry
--schema agent-task: objective, tools, memory, output-type, constraints, handoff, priority

## V3 DSL

Append --dsl to any mode: G:value|A:value|I:val1,val2|D:value|F:value
Bridge DSL to JSON: /marlin bridge <dsl-string>

Built by @adisingh-cs — https://github.com/adisingh-cs/Marlin — MIT License
