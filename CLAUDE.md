# Marlin — Input Prompt Optimizer

Marlin compresses input prompts before sending to any model.
Four modes available via slash commands. Read SKILL.md for full instructions.

Quick reference:
- /marlin swift — normalize + structure (target: ~20-35%)
- /marlin sharp — compact JSON + short keys (target: ~35-50%)
- /marlin strike — maximum compression (target: ~50-70%)
- /marlin sonar --schema web-api|data-pipeline|agent-task (target: ~40-65%)

Append --report (default), --prompt, --diff, or --all to any command.

Built by @adisingh-cs — https://github.com/adisingh-cs/Marlin — MIT License
