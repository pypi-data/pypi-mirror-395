# pypith-cli

Wrapper CLI that turns existing tools into agent-friendly experiences.

- Capture help text, analyze it, and emit Pith schemas
- Generate Bash/PowerShell/CMD wrappers
- Optional LLM providers (Anthropic, OpenAI, Ollama) with heuristic fallback

## Installation

```bash
pip install pypith-cli

# With LLM providers
pip install pypith-cli[anthropic]
pip install pypith-cli[openai]
pip install pypith-cli[ollama]
```

## Quick Start

```bash
# Configure LLM provider (optional)
pith init --provider anthropic

# Wrap your tools
pith wrap kubectl terraform docker

# Activate in shell
eval "$(pith activate)"

# Now they're agent-friendly
kubectl                    # Shows progressive discovery tiers
```

## Commands

| Command | Description |
|---------|-------------|
| `pith init` | Configure LLM provider and settings |
| `pith wrap <tool>` | Wrap a CLI with progressive discovery |
| `pith unwrap <tool>` | Remove wrapper |
| `pith list` | List all wrapped tools |
| `pith refresh <tool>` | Re-analyze after tool upgrade |
| `pith activate` | Print PATH activation command |
| `pith find <query>` | Semantic search across tools |
| `pith export <tool>` | Export schema for sharing |
| `pith import <file>` | Import pre-made schema |
