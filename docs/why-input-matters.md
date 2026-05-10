# Why input compression matters

Most developers focus on what the model says back to them. Marlin focuses on what the model reads in the first place. This is the less obvious — and arguably more impactful — half of the token optimization problem.

## The cost of verbose input

Every token you send to an LLM costs money. At scale, input tokens are the dominant cost driver — not output tokens. A prompt that rambles for 200 tokens when 60 would convey the same intent is not just wasteful; it is actively degrading model performance by diluting the signal in your context window.

Consider the math: if your average prompt is 150 tokens and you could compress it to 60 tokens without losing intent, you save 60% per call. At 100,000 API calls per day at $3/million input tokens, that is $27 per day, $810 per month — from input alone.

## Structured input produces deterministic output

LLMs are probabilistic systems. The more ambiguity in the input, the wider the distribution of possible outputs. Verbose, conversational prompts introduce noise — filler words, implicit assumptions, contradictory phrasing — that forces the model to make guesses about what you actually want.

Structured input eliminates this guessing. When you send `{"goal":"build auth API","action":"create","inputs":["email","password"],"constraints":["jwt-only"]}` instead of a three-sentence paragraph saying roughly the same thing, the model receives:

1. **Unambiguous intent** — one goal, one action, explicitly named
2. **Complete field coverage** — every relevant dimension is either specified or explicitly null
3. **No filler to parse** — the model spends zero capacity on "I need to" and "it should be able to"
4. **Deterministic field order** — the same prompt always looks the same structurally

The result: sharper, more consistent, more reproducible output.

## Schema-anchored prompts reduce hallucination

When a model receives a schema-normalized prompt, it has less room to hallucinate. The schema constrains what fields exist, what types they are, and what values are valid. The model is not inventing structure — it is responding to structure that was provided.

This is especially powerful in agent pipelines where prompts are passed between models. A human might tolerate a vaguely-worded prompt. An agent receiving that same prompt as the 14th step in a pipeline will amplify every ambiguity into compounding errors.

## Input vs. output compression

There is a common confusion between what Marlin does and what output-style compressors do. Here is the distinction:

| Dimension | Input compression (Marlin) | Output compression (e.g., caveman) |
|-----------|---------------------------|-------------------------------------|
| What it compresses | The prompt sent TO the model | The response style FROM the model |
| How it works | Schema-based structural normalization | Style instructions (terse, no fluff) |
| What changes | The shape and density of input tokens | The verbosity and formatting of output |
| Token savings | Input tokens (dominant cost at scale) | Output tokens |
| Model behavior effect | More deterministic, less hallucination | More concise responses |
| Composability | Independent — stack with any output compressor | Independent — stack with any input compressor |

These solve different halves of the same problem. They compose cleanly. Run Marlin to compress the input, run an output compressor to tighten the response, and stack the savings. There is no conflict.

## The context window is finite

Modern LLMs have large context windows — 100K, 200K tokens. But large does not mean infinite, and every token matters more than developers realize.

In long sessions, agent workflows, and multi-turn conversations, the context window fills up. Verbose prompts eat into the space available for:
- Conversation history
- System instructions
- Tool outputs
- Retrieved context (RAG)

Compressing input prompts by 50% effectively doubles the useful capacity of your context window for everything else.

## The bottom line

Input token cost matters more than most developers realize. Structured input produces more deterministic output. Schema-anchored prompts reduce hallucination. Input compression and output compression are independent, composable optimizations. And the context window you save on input is context window you gain for everything else.

Marlin never changes what the model says. It changes what the model reads.
