# aws-knowledge-tool

<p align="center">
  <img src=".github/assets/logo.png" alt="aws-knowledge-tool logo" width="256">
</p>

[![Python Version](https://img.shields.io/badge/python-3.14+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)
[![Type checked: mypy](https://img.shields.io/badge/type%20checked-mypy-blue.svg)](https://github.com/python/mypy)
[![AI Generated](https://img.shields.io/badge/AI-Generated-blueviolet.svg)](https://www.anthropic.com/claude)
[![Built with Claude Code](https://img.shields.io/badge/Built_with-Claude_Code-5A67D8.svg)](https://www.anthropic.com/claude/code)

> CLI tool for querying AWS Knowledge MCP Server - search, read, and discover AWS documentation

## Table of Contents

- [About](#about)
- [Features](#features)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Commands](#commands)
- [Library Usage](#library-usage)
- [Development](#development)
- [Known Issues](#known-issues)
- [Resources](#resources)

## About

`aws-knowledge-tool` is a **CLI-first** tool that provides programmatic access to AWS documentation through the [AWS Knowledge MCP Server](https://knowledge-mcp.global.api.aws). It features an **agent-friendly design** with composable commands, structured output, and pipeline support.

### What is AWS Knowledge MCP Server?

The AWS Knowledge MCP Server is a remote MCP (Model Context Protocol) server that provides access to:
- AWS Documentation
- AWS Blogs  
- AWS Solutions Library
- AWS Architecture Center
- AWS Prescriptive Guidance

**Server**: `https://knowledge-mcp.global.api.aws`  
**Protocol**: MCP (JSON-RPC 2.0 over HTTP)  
**Authentication**: None (public, rate-limited)

### Why CLI-First?

- **Agent-Friendly**: Structured commands and error messages enable AI agents (Claude Code, etc.) to reason and act effectively
- **Composable**: JSON output and stderr separation allow easy piping and integration
- **Reusable**: Commands serve as building blocks for skills, automation, and workflows
- **Reliable**: Type-safe, tested, and predictable behavior

## Features

- 🔍 **Search** - Search AWS documentation with pagination
- 📖 **Read** - Fetch and convert AWS docs to markdown
- 💡 **Recommend** - Discover related documentation
- 📊 **Multi-Level Verbosity** - Progressive logging detail (-v/-vv/-vvv)
- 🐚 **Shell Completion** - Tab completion for bash, zsh, and fish
- 🔒 **Security Scanning** - Automated secret detection, code security, and dependency checks
- 🤖 **Agent-Friendly** - Structured JSON output, clear error messages
- 🔗 **Composable** - Stdin support for pipeline workflows
- 📋 **Multiple Formats** - JSON and markdown output
- 🎯 **Type-Safe** - Strict mypy checks, comprehensive type hints
- ✅ **Well-Tested** - Pytest suite with quality checks

## Installation

### Prerequisites

- Python 3.14+
- [uv](https://github.com/astral-sh/uv) package manager

### Install Globally

```bash
# Clone and install
git clone https://github.com/dnvriend/aws-knowledge-tool.git
cd aws-knowledge-tool
uv tool install .

# Verify installation
aws-knowledge-tool --version

# Optional: Install shell completion
eval "$(aws-knowledge-tool completion bash)"  # For bash
eval "$(aws-knowledge-tool completion zsh)"   # For zsh
```

## Quick Start

```bash
# Search AWS documentation
aws-knowledge-tool search "Lambda function URLs"

# Read a documentation page  
aws-knowledge-tool read "https://docs.aws.amazon.com/lambda/latest/dg/welcome.html"

# Get recommendations
aws-knowledge-tool recommend "https://docs.aws.amazon.com/lambda/latest/dg/welcome.html" --type new

# Pipeline composition
aws-knowledge-tool search "Lambda" --json | jq -r '.[0].url' | aws-knowledge-tool read --stdin
```

## Commands

### search - Search AWS Documentation

```bash
aws-knowledge-tool search QUERY [OPTIONS]

Options:
  -l, --limit INTEGER    Maximum results (default: 10)
  -o, --offset INTEGER   Skip first N results (default: 0)
  --json                 Output JSON format
  --stdin                Read query from stdin
  -v, --verbose          Enable verbose output (use -v for INFO, -vv for DEBUG, -vvv for TRACE)
  -q, --quiet            Suppress non-essential output

Examples:
  # Basic search
  aws-knowledge-tool search "S3 versioning" --limit 5

  # With INFO logging (-v)
  aws-knowledge-tool search "DynamoDB" -v

  # With DEBUG logging and full tracebacks (-vv)
  aws-knowledge-tool search "Lambda" -vv

  # With TRACE logging (includes library internals) (-vvv)
  aws-knowledge-tool search "RDS" -vvv

  # JSON output for pipelines
  aws-knowledge-tool search "Lambda" --json

  # Read from stdin
  echo "Lambda" | aws-knowledge-tool search --stdin
```

### read - Read AWS Documentation

```bash
aws-knowledge-tool read URL [OPTIONS]

Options:
  -s, --start-index INT  Starting character index
  -m, --max-length INT   Maximum characters to fetch
  --json                 Output JSON format
  --stdin                Read URL from stdin
  -v, --verbose          Enable verbose output (use -v for INFO, -vv for DEBUG, -vvv for TRACE)
  -q, --quiet            Suppress non-essential output

Examples:
  # Read full document
  aws-knowledge-tool read "https://docs.aws.amazon.com/lambda/latest/dg/welcome.html"

  # Read with pagination
  aws-knowledge-tool read "https://docs.aws.amazon.com/..." --start-index 5000 --max-length 2000

  # Pipeline from search
  aws-knowledge-tool search "Lambda" --json | jq -r '.[0].url' | aws-knowledge-tool read --stdin

  # With DEBUG logging
  aws-knowledge-tool read "https://docs.aws.amazon.com/..." -vv
```

### recommend - Get Documentation Recommendations

```bash
aws-knowledge-tool recommend URL [OPTIONS]

Options:
  -t, --type TYPE        Filter by type (highly_rated, new, similar, journey)
  -l, --limit INTEGER    Max results per category (default: 5)
  -o, --offset INTEGER   Skip first N per category (default: 0)
  --json                 Output JSON format
  --stdin                Read URL from stdin
  -v, --verbose          Enable verbose output (use -v for INFO, -vv for DEBUG, -vvv for TRACE)
  -q, --quiet            Suppress non-essential output

Examples:
  # Get all recommendations
  aws-knowledge-tool recommend "https://docs.aws.amazon.com/lambda/latest/dg/welcome.html"

  # Filter by type (find new features)
  aws-knowledge-tool recommend "https://docs.aws.amazon.com/..." --type new

  # Limit results and JSON output
  aws-knowledge-tool recommend "https://docs.aws.amazon.com/..." --json --limit 3

  # With INFO logging
  aws-knowledge-tool recommend "https://docs.aws.amazon.com/..." -v
```

## Multi-Level Verbosity Logging

Control logging detail with progressive verbosity flags. All logs output to stderr, keeping stdout clean for data.

### Logging Levels

| Flag | Level | Output | Use Case |
|------|-------|--------|----------|
| (none) | WARNING | Errors and warnings only | Production, quiet mode |
| `-v` | INFO | + High-level operations | Normal debugging |
| `-vv` | DEBUG | + Detailed info, full tracebacks | Development, troubleshooting |
| `-vvv` | TRACE | + Library internals (MCP, httpx) | Deep debugging |

### Examples

```bash
# Quiet mode - only errors and warnings
aws-knowledge-tool search "Lambda"

# INFO - see operations and progress
aws-knowledge-tool search "Lambda" -v
# Output:
# [INFO] Search command started
# [INFO] Searching for: Lambda
# [INFO] Found 10 results

# DEBUG - see detailed information and full tracebacks
aws-knowledge-tool search "Lambda" -vv
# Output:
# [INFO] Search command started
# [INFO] Searching for: Lambda
# [DEBUG] Parameters: limit=10, offset=0
# [DEBUG] Connecting to AWS Knowledge MCP Server...
# [DEBUG] Connected. Searching...
# [DEBUG] Search API call complete
# [INFO] Found 10 results

# TRACE - see library internals (MCP, httpx, httpcore, anyio logs)
aws-knowledge-tool search "Lambda" -vvv
# Output: Same as -vv plus httpx request/response logs
```

### Integration with Pipelines

Logging to stderr allows clean pipeline composition:

```bash
# Data to stdout, logs to stderr - perfect for pipelines
aws-knowledge-tool search "Lambda" --json -v | jq -r '.[0].url' | aws-knowledge-tool read --stdin -v
```

## Shell Completion

The tool provides native shell completion for bash, zsh, and fish shells, following the same pattern as popular tools like kubectl and docker.

### Supported Shells

| Shell | Version Requirement | Status |
|-------|-------------------|--------|
| **Bash** | ≥ 4.4 | ✅ Supported |
| **Zsh** | Any recent version | ✅ Supported |
| **Fish** | ≥ 3.0 | ✅ Supported |
| **PowerShell** | Any version | ❌ Not Supported |

### Installation

#### Quick Setup (Temporary)

```bash
# Bash - active for current session only
eval "$(aws-knowledge-tool completion bash)"

# Zsh - active for current session only
eval "$(aws-knowledge-tool completion zsh)"

# Fish - active for current session only
aws-knowledge-tool completion fish | source
```

#### Permanent Setup (Recommended)

```bash
# Bash - add to ~/.bashrc
echo 'eval "$(aws-knowledge-tool completion bash)"' >> ~/.bashrc
source ~/.bashrc

# Zsh - add to ~/.zshrc
echo 'eval "$(aws-knowledge-tool completion zsh)"' >> ~/.zshrc
source ~/.zshrc

# Fish - save to completions directory
mkdir -p ~/.config/fish/completions
aws-knowledge-tool completion fish > ~/.config/fish/completions/aws-knowledge-tool.fish
```

#### File-based Installation (Better Performance)

For better shell startup performance, generate completion scripts to files:

```bash
# Bash
aws-knowledge-tool completion bash > ~/.aws-knowledge-tool-complete.bash
echo 'source ~/.aws-knowledge-tool-complete.bash' >> ~/.bashrc

# Zsh
aws-knowledge-tool completion zsh > ~/.aws-knowledge-tool-complete.zsh
echo 'source ~/.aws-knowledge-tool-complete.zsh' >> ~/.zshrc

# Fish (automatic loading from completions directory)
mkdir -p ~/.config/fish/completions
aws-knowledge-tool completion fish > ~/.config/fish/completions/aws-knowledge-tool.fish
```

### Usage

Once installed, completion works automatically:

```bash
# Tab completion for commands
aws-knowledge-tool <TAB>
# Shows: search read recommend completion

# Tab completion for options
aws-knowledge-tool search --<TAB>
# Shows: --limit --offset --json --stdin --verbose --quiet --help

# Tab completion for shell types
aws-knowledge-tool completion <TAB>
# Shows: bash zsh fish
```

### Getting Help

```bash
# View completion installation instructions
aws-knowledge-tool completion --help
```

## Library Usage

Use `aws-knowledge-tool` as a Python library:

```python
import asyncio
from aws_knowledge_tool import MCPClient

async def search_docs():
    async with MCPClient() as client:
        results = await client.search_documentation("Lambda functions", limit=5)
        for result in results:
            print(f"{result['title']}: {result['url']}")

asyncio.run(search_docs())
```

## Development

```bash
# Clone repository
git clone https://github.com/dnvriend/aws-knowledge-tool.git
cd aws-knowledge-tool

# Install dependencies
make install

# Run quality checks
make format      # Format with ruff
make lint        # Lint with ruff
make typecheck   # Type check with mypy
make test        # Run pytest
make check       # Run all checks (lint + typecheck + test + security)

# Security scanning
make security-bandit      # Python security linter
make security-pip-audit   # Dependency vulnerability scanner
make security-gitleaks    # Secret and API key detection
make security             # Run all security checks

# Build and install
make pipeline    # format + lint + typecheck + test + security + build + install-global
```

### Security Scanning

The project includes three lightweight security tools that provide 80%+ coverage:

| Tool | Purpose | Speed | Coverage |
|------|---------|-------|----------|
| **bandit** | Python code security linting | ⚡⚡ Fast | SQL injection, hardcoded secrets, unsafe functions |
| **pip-audit** | Dependency vulnerability scanning | ⚡⚡ Fast | Known CVEs in dependencies |
| **gitleaks** | Secret and API key detection | ⚡⚡⚡ Very Fast | Secrets in code and git history |

**Prerequisites for gitleaks:**
```bash
# macOS
brew install gitleaks

# Linux
# See: https://github.com/gitleaks/gitleaks#installation
```

All security checks run automatically in `make check` and `make pipeline`.

## Known Issues

### MCP HTTP Transport

**Issue**: The current MCP Python SDK implementation uses stdio-based transport (read_stream/write_stream) rather than HTTP transport. The tool currently uses a stub implementation with memory streams for type checking.

**Impact**: The tool will not connect to the AWS Knowledge MCP Server until proper HTTP transport is implemented.

**Workaround**: Implementation needs the MCP SDK's HTTP client wrapper or custom HTTP-to-stream adapter.

**TODO**:
- Investigate MCP Python SDK HTTP transport documentation
- Implement proper HTTP client using anyio streams or httpx adapter
- See: https://github.com/modelcontextprotocol/python-sdk

**Code Location**: `aws_knowledge_tool/core/mcp_client.py:39-63`

## Resources

- **AWS Knowledge MCP Server**: `https://knowledge-mcp.global.api.aws`
- **MCP Specification**: https://modelcontextprotocol.io
- **MCP Python SDK**: https://github.com/modelcontextprotocol/python-sdk
- **AWS Documentation**: https://docs.aws.amazon.com

## License

MIT License - see [LICENSE](LICENSE) file

## Author

**Dennis Vriend**  
GitHub: [@dnvriend](https://github.com/dnvriend)

---

🤖 **Built with [Claude Code](https://claude.com/claude-code)**

This project was developed using Claude Code, an AI-powered development tool by Anthropic.
