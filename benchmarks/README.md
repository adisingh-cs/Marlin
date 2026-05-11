# Benchmarks

Marlin's benchmark harness measures prompt compression through OpenRouter.
It sends the root `SKILL.md` plus each benchmark prompt to an OpenRouter
chat-completions model, then records heuristic token counts, absolute savings,
percent savings, and compression-system overhead.

## Status

Benchmark results are still pending. The harness is OpenRouter-compatible, but
the committed `results/v1-baseline.json` remains a placeholder until a full run
is executed with a real OpenRouter API key and selected model.

## Run it yourself

Requirements: Python 3.11+ and an OpenRouter API key.

Environment-based:

```bash
export OPENROUTER_API_KEY="sk-or-..."
export OPENROUTER_MODEL="openai/gpt-4o-mini"
python benchmarks/run.py
```

Argument-based:

```bash
python benchmarks/run.py --api-key "sk-or-..." --model "openai/gpt-4o-mini"
```

By default, results are written to `benchmarks/results/v1-baseline.json`.
Use `--output path/to/results.json` to write elsewhere.

Run harness unit tests:

```bash
python -m unittest discover -s tests
```

## Options

```bash
python benchmarks/run.py \
  --api-key "sk-or-..." \
  --model "openai/gpt-4o-mini" \
  --modes "swift,sharp,strike,sonar:web-api,sonar:data-pipeline,sonar:agent-task" \
  --max-tokens 1024
```

Supported environment variables:

- `OPENROUTER_API_KEY`: API key used when `--api-key` is omitted.
- `OPENROUTER_MODEL`: model id used when `--model` is omitted.
- `OPENROUTER_SITE_URL`: optional `HTTP-Referer` attribution header.
- `OPENROUTER_APP_TITLE`: optional `X-OpenRouter-Title` attribution header.

## Methodology

- 10 test prompts covering REST API design, database query, React component,
  authentication flow, data pipeline, agent task, code review, bug fix,
  deployment config, and a general architecture question.
- Default modes: `swift`, `sharp`, `strike`, `sonar:web-api`,
  `sonar:data-pipeline`, and `sonar:agent-task`.
- Token counts are estimated with the current repository heuristic:
  `ceil(len(string) / 3.5)` for JSON and `ceil(len(string) / 4)` for natural
  language.
- OpenRouter `usage` fields are recorded when returned by the selected model.
- `compression_system_overhead_tokens` estimates the system prompt containing
  `SKILL.md`. This overhead is real for model-mediated compression and should
  not be confused with downstream prompt savings.

## Reliability Notes

The benchmark is model-mediated, so output can vary by model/provider. Treat
results as empirical measurements for the chosen OpenRouter model, not as
deterministic product guarantees. The character-based token counter is useful
for rough comparisons, but model-specific tokenizer counts are still a future
improvement.
