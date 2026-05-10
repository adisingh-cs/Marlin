# Security Policy

## Supported Versions

| Version | Supported          |
|---------|--------------------|
| 1.0.x   | :white_check_mark: |

## Reporting a Vulnerability

**Do not open a public issue for security vulnerabilities.**

To report a security vulnerability, please use [GitHub's private security advisory feature](https://github.com/adisingh-cs/marlin/security/advisories/new).

### What to include

- Description of the vulnerability
- Steps to reproduce
- Which skills, schemas, or tools are affected
- Potential impact assessment
- Suggested fix (if you have one)

### Response timeline

- **Acknowledgment:** Within 7 days of report
- **Assessment:** Within 14 days of acknowledgment
- **Fix or mitigation:** Within 30 days for confirmed vulnerabilities

### Scope

Marlin is a skills-based repository. Security concerns may include:

- Prompt injection via crafted input that bypasses intent parsing
- Schema validation bypass allowing malformed output
- Tool scripts (Python) with command injection or path traversal risks
- GitHub Actions workflow vulnerabilities
- Sensitive data leakage through benchmark or test fixtures

### Out of scope

- Vulnerabilities in upstream LLM providers (Anthropic, OpenAI, Google)
- Issues in agent platforms (Claude Code, Cursor, Gemini CLI)
- Token estimation inaccuracy (this is a known approximation, not a security issue)

## Responsible Disclosure

We follow coordinated disclosure. We will credit reporters in the CHANGELOG unless anonymity is requested.
