# Benchmarks

Marlin's benchmark harness measures real token reduction across all four compression modes
using the Anthropic API.

## Status

> 🚧 **Benchmark results coming soon.**
>
> The harness (`run.py`) is ready. Results will be committed to `results/` after
> the first full benchmark run. Follow the repo to get notified.

## Run it yourself

Requirements: Python 3.11+, `ANTHROPIC_API_KEY` set in your environment.

```bash
cd benchmarks
python run.py
```

Results are written to `benchmarks/results/v1-baseline.json`.

## Methodology

- 10 test prompts covering: REST API design, database query, React component, 
  authentication flow, data pipeline, agent task, code review, bug fix, 
  deployment config, general question
- Each prompt tested against all 4 modes (structured, compact, dense, domain)
- Token counts estimated using `ceil(len(string) / 3.5)` for JSON, `ceil(len(string) / 4)` for natural language
- Results committed as JSON — reproducible by anyone with an API key

## Expected results (based on design targets)

| Mode | Expected reduction |
|---|---|
| structured | 20–35% |
| compact | 35–50% |
| dense | 50–70% |
| domain | 40–65% |

*Actual committed results will replace this table once benchmark run is complete.*
