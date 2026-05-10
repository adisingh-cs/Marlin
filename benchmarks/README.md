# Benchmarks

Benchmark harness for measuring Marlin compression effectiveness across all modes.

## Methodology

1. Load test prompts from `prompts/test-prompts.txt`
2. Estimate token count in original prompt (character-based heuristic)
3. Apply each Marlin mode via Anthropic API with the corresponding skill loaded
4. Estimate token count in compressed output
5. Calculate reduction percentage
6. Write results to `results/v1-baseline.json`

## Running benchmarks

```bash
export ANTHROPIC_API_KEY=your-key-here
python benchmarks/run.py
```

## Results

Results are stored in `results/v1-baseline.json`. Each result includes:

- Prompt ID
- Mode applied
- Original token count (estimated)
- Compressed token count (estimated)
- Reduction percentage
- Preview of original and compressed text

## Token estimation

Token counts are estimates based on character-length heuristics:
- Natural language: ~4 characters per token
- JSON/structured: ~3.5 characters per token

Actual token counts vary by model tokenizer. These estimates are consistent enough for relative comparison across modes.
