# Marlin installer for Windows PowerShell
# Usage: irm https://raw.githubusercontent.com/adisingh-cs/Marlin/main/install.ps1 | iex
# Options: pass --minimal, --all, or --list

param(
  [switch]$Minimal,
  [switch]$All,
  [switch]$List
)

$REPO = "adisingh-cs/Marlin"

function Write-Marlin { param($msg) Write-Host "[marlin] $msg" -ForegroundColor Cyan }
function Write-Ok     { param($msg) Write-Host "v $msg" -ForegroundColor Green }
function Write-Warn   { param($msg) Write-Host "! $msg" -ForegroundColor Yellow }

if ($List) {
  Write-Host "Marlin agent slugs for npx skills -a <slug>:"
  Write-Host "  claude-code, cursor, windsurf, cline, github-copilot,"
  Write-Host "  codex, opencode, gemini, antigravity, roo, kiro"
  exit 0
}

Write-Host ""
Write-Host "  Marlin - Swift input. Sharp output. Every token counts." -ForegroundColor Cyan
Write-Host "  https://github.com/$REPO"
Write-Host ""

function Invoke-NpxInstall {
  param($agent)
  if (Get-Command npx -ErrorAction SilentlyContinue) {
    try {
      npx skills add $REPO -g -a $agent -y 2>$null
      Write-Ok $agent
    } catch {
      Write-Warn "$agent skipped"
    }
  }
}

if (Get-Command claude -ErrorAction SilentlyContinue) {
  Write-Marlin "Claude Code detected"
  Invoke-NpxInstall "claude-code"
}

if (Get-Command gemini -ErrorAction SilentlyContinue) {
  Write-Marlin "Gemini CLI detected"
  try {
    gemini extensions install "https://github.com/$REPO" 2>$null
    Write-Ok "Gemini CLI"
  } catch {
    Write-Warn "Gemini extension failed - using npx skills"
    Invoke-NpxInstall "gemini"
  }
}

if ((Test-Path "$env:USERPROFILE\.cursor") -or (Test-Path ".cursor")) {
  Write-Marlin "Cursor detected"; Invoke-NpxInstall "cursor"
}

if ((Test-Path "$env:USERPROFILE\.windsurf") -or (Test-Path ".windsurf")) {
  Write-Marlin "Windsurf detected"; Invoke-NpxInstall "windsurf"
}

if (Get-Command codex -ErrorAction SilentlyContinue) {
  Write-Marlin "Codex detected"; Invoke-NpxInstall "codex"
}

if ((Get-Command antigravity -ErrorAction SilentlyContinue) -or (Test-Path ".antigravity")) {
  Write-Marlin "Antigravity detected"; Invoke-NpxInstall "antigravity"
}

if (Get-Command opencode -ErrorAction SilentlyContinue) {
  Write-Marlin "opencode detected"; Invoke-NpxInstall "opencode"
}

Write-Host ""
Write-Ok "Marlin install complete."
Write-Host "  Use /marlin swift | sharp | strike | sonar in any agent."
Write-Host "  Docs: https://github.com/$REPO"
Write-Host ""
