#!/usr/bin/env bash
# Marlin installer — detects installed agents and wires Marlin to each
# Usage: curl -fsSL https://raw.githubusercontent.com/adisingh-cs/Marlin/main/install.sh | bash
# Options: --minimal (skill only), --all (also drop rule files), --list (show agent slugs)
set -euo pipefail

REPO="adisingh-cs/Marlin"
CYAN='\033[0;36m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log()  { echo -e "${CYAN}[marlin]${NC} $*"; }
ok()   { echo -e "${GREEN}✓${NC} $*"; }
warn() { echo -e "${YELLOW}⚠${NC} $*"; }

MINIMAL=false
WITH_ALL=false
LIST=false

for arg in "$@"; do
  case $arg in
    --minimal) MINIMAL=true ;;
    --all)     WITH_ALL=true ;;
    --list)    LIST=true ;;
  esac
done

if $LIST; then
  echo "Marlin agent slugs for npx skills -a <slug>:"
  echo "  claude-code, cursor, windsurf, cline, github-copilot,"
  echo "  codex, opencode, gemini, antigravity, roo, kiro, amp,"
  echo "  continue, aider, goose, tabnine, trae, warp, replit"
  exit 0
fi

echo ""
echo "  🐟 Marlin — Swift input. Sharp output. Every token counts."
echo "  https://github.com/${REPO}"
echo ""

npx_install() {
  local agent="$1"
  if command -v npx &>/dev/null; then
    npx skills add "${REPO}" -g -a "${agent}" -y 2>/dev/null \
      && ok "${agent}" || warn "${agent} skipped (not found)"
  fi
}

# Claude Code
if command -v claude &>/dev/null; then
  log "Claude Code detected"; npx_install "claude-code"
fi

# Gemini CLI
if command -v gemini &>/dev/null; then
  log "Gemini CLI detected"
  gemini extensions install "https://github.com/${REPO}" 2>/dev/null \
    && ok "Gemini CLI" \
    || { warn "Gemini extension failed — using npx skills"; npx_install "gemini"; }
fi

# Cursor
if [ -d "$HOME/.cursor" ] || [ -d ".cursor" ]; then
  log "Cursor detected"; npx_install "cursor"
fi

# Windsurf
if [ -d "$HOME/.windsurf" ] || [ -d ".windsurf" ]; then
  log "Windsurf detected"; npx_install "windsurf"
fi

# Cline
if [ -d ".clinerules" ]; then
  log "Cline detected"; npx_install "cline"
fi

# Copilot
if [ -f ".github/copilot-instructions.md" ]; then
  log "GitHub Copilot detected"; npx_install "github-copilot"
fi

# Codex
if command -v codex &>/dev/null; then
  log "Codex detected"; npx_install "codex"
fi

# Antigravity
if command -v antigravity &>/dev/null || [ -d ".antigravity" ]; then
  log "Antigravity detected"; npx_install "antigravity"
fi

# opencode
if command -v opencode &>/dev/null; then
  log "opencode detected"; npx_install "opencode"
fi

# Roo
if [ -d ".roo" ]; then
  log "Roo detected"; npx_install "roo"
fi

# Kiro
if command -v kiro &>/dev/null || [ -d ".kiro" ]; then
  log "Kiro detected"; npx_install "kiro"
fi

# Fallback: install globally for everything else
if ! command -v claude &>/dev/null && ! command -v gemini &>/dev/null && \
   ! [ -d "$HOME/.cursor" ] && ! command -v codex &>/dev/null; then
  log "No specific agent detected — installing globally via npx skills"
  npx skills add "${REPO}" -g -y 2>/dev/null && ok "Global install done" || warn "npx skills not found — manual install required"
fi

# Drop rule files into current repo if --all
if $WITH_ALL; then
  log "Writing rule files into current directory..."
  RULE="When user types /marlin swift|sharp|strike|sonar — apply Marlin compression. https://github.com/${REPO}"
  mkdir -p .cursor/rules
  printf -- "---\ndescription: Marlin input optimizer\nglobs: []\nalwaysApply: false\n---\n\n%s" "$RULE" > .cursor/rules/marlin.mdc
  ok ".cursor/rules/marlin.mdc"
  mkdir -p .windsurf/rules && echo "$RULE" > .windsurf/rules/marlin.md && ok ".windsurf/rules/marlin.md"
  mkdir -p .clinerules && echo "$RULE" > .clinerules/marlin.md && ok ".clinerules/marlin.md"
  mkdir -p .github && echo "$RULE" > .github/copilot-instructions.md && ok ".github/copilot-instructions.md"
fi

echo ""
ok "Marlin install complete."
echo "  Use /marlin swift | sharp | strike | sonar in any agent."
echo "  Docs: https://github.com/${REPO}"
echo ""
