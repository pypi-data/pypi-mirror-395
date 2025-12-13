# ContextuAIze

[![PyPI version](https://badge.fury.io/py/contextuaize.svg)](https://pypi.org/project/contextuaize/)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Smart codebase context extraction for LLMs** — Transform your codebase into optimized context for Claude, GPT-4, Gemini, and other large language models.

## What's New in v0.2

- **🧠 Smart Mode** — LLM-powered intelligent file filtering
- **🎯 Query-Driven Context** — Focus on specific features or tasks
- **📝 Auto-Summarization** — Large files get smart summaries
- **🔍 Respects .gitignore** — No more manual exclusion lists
- **🌳 Tech Stack Detection** — Automatically identifies your stack

## Features

| Feature | Basic Mode | Smart Mode (`--smart`) |
|---------|------------|------------------------|
| .gitignore support | ✅ | ✅ |
| Binary file filtering | ✅ | ✅ |
| Directory tree | ✅ | ✅ |
| Stack detection | ✅ | ✅ |
| Intelligent file selection | ❌ | ✅ |
| Query-driven filtering | ❌ | ✅ |
| Large file summarization | ❌ | ✅ |

## Installation

```bash
pip install contextuaize
```

Or install from source:

```bash
git clone https://github.com/ohharsen/contextuaize.git
cd contextuaize
pip install -e .
```

## Quick Start

### Basic Usage

```bash
# Scan current directory
contextuaize

# Scan specific project
contextuaize /path/to/project -o context.txt

# Only Python files
contextuaize --include "*.py"

# Exclude tests
contextuaize --exclude "test*" --exclude "*_test.py"

# Just see the tree structure
contextuaize --tree-only
```

### Smart Mode (LLM-Powered)

Smart mode uses Claude to intelligently select relevant files and summarize large ones.

```bash
# Set your API key
export ANTHROPIC_API_KEY="sk-ant-..."

# Let AI decide what's important
contextuaize --smart

# Focus on specific functionality
contextuaize --smart --query "authentication and user sessions"

# Focus on a bug
contextuaize --smart --query "database connection handling"
```

## How It Works

### Basic Mode
1. Walks the directory tree
2. Respects `.gitignore` rules automatically
3. Skips universal noise (node_modules, .git, lockfiles, binaries)
4. Concatenates all text files with clear markers

### Smart Mode
1. **Two-pass scanning**: First scans structure, then uses LLM to select files
2. **Relevance scoring**: Files ranked as essential → important → optional → skip
3. **Query-driven**: When you specify `--query`, only files relevant to that task are included
4. **Smart summarization**: Files over 100KB get intelligent summaries instead of full content

## CLI Reference

```
contextuaize [directory] [options]

Arguments:
  directory              Directory to scan (default: current directory)

Options:
  -o, --output FILE      Output file path (default: codebase_context.txt)
  
Filtering:
  --include PATTERN      Include only matching files (can repeat)
  --exclude PATTERN      Exclude matching files (can repeat)
  --no-gitignore         Ignore .gitignore rules
  
Smart Mode:
  --smart                Enable LLM-powered intelligent filtering
  --query, -q TEXT       Focus on specific task/feature (enables --smart)
  --api-key KEY          Anthropic API key (or use ANTHROPIC_API_KEY env)
  --model MODEL          Model to use (default: claude-sonnet-4-20250514)
  
Output Destination (mutually exclusive):
  -o, --output FILE      Write to file (default)
  -c, --clipboard        Copy to system clipboard
  --stdout               Print to stdout (for piping)
  
Output Control:
  --quiet                Suppress progress output
  --tree-only            Only show project tree, no file contents
```

## Output Modes

### File (default)
```bash
contextuaize                    # → codebase_context.txt
contextuaize -o context.txt     # → context.txt
```

### Clipboard
```bash
contextuaize -c                 # Copy directly to clipboard
contextuaize --clipboard        # Same thing
```
Works on macOS (pbcopy), Windows (clip), and Linux (xclip/xsel/wl-copy).

### Stdout
```bash
contextuaize --stdout           # Print to stdout
contextuaize --stdout | head    # Pipe to other commands
contextuaize --stdout | pbcopy  # Manual clipboard on macOS
```
Progress messages go to stderr, so piping works cleanly.

## Examples

### Understanding a New Codebase
```bash
contextuaize --smart --query "explain the overall architecture"
```

### Preparing to Add a Feature  
```bash
contextuaize --smart --query "payment processing and Stripe integration"
```

### Debugging an Issue
```bash
contextuaize --smart --query "WebSocket connection handling and reconnection logic"
```

### Code Review Context
```bash
contextuaize --smart --query "user authentication flow"
```

### Just the Backend
```bash
contextuaize --include "*.py" --exclude "test*" --exclude "migrations/*"
```

## Output Format

The generated context file includes:

```
================================================================================
PROJECT CONTEXT SNAPSHOT
================================================================================

Detected Stack: Python, React, Docker
Context Focus: authentication flow
Total Files: 15

PROJECT STRUCTURE
----------------------------------------
my-project/
├── src/
│   ├── auth/
│   │   ├── login.py
│   │   └── session.py
│   └── api/
│       └── routes.py
└── tests/

================================================================================
FILE CONTENTS
================================================================================

--- START FILE: src/auth/login.py ---
[file content or summary]
--- END FILE: src/auth/login.py ---

...
```

## Configuration

### Environment Variables

| Variable | Description |
|----------|-------------|
| `ANTHROPIC_API_KEY` | API key for smart mode |

### Patterns

Both `--include` and `--exclude` support glob patterns:

- `*.py` — All Python files
- `test*` — Files/dirs starting with "test"
- `src/**/*.ts` — TypeScript files in src/
- `!important.py` — Negation (in .gitignore)

## Using with LLMs

After generating context, upload to your LLM with a prompt like:

> "I've attached my project context. Please analyze the architecture and wait for my questions."

Or for focused tasks:

> "Here's context focused on authentication. Help me add OAuth2 support."

## License

MIT License — see [LICENSE](LICENSE) for details.

---

<<<<<<< Updated upstream
**Author:** Arsen Ohanyan • [GitHub](https://github.com/ohharsen)
=======
**Author:** Arsen Ohanyan • [GitHub](https://github.com/ohharsen) • [PyPI](https://pypi.org/project/contextuaize/)
>>>>>>> Stashed changes
