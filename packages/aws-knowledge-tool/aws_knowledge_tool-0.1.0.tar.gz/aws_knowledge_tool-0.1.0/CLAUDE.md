# aws-knowledge-tool - Developer Guide

## Overview

**Purpose**: CLI tool for querying AWS Knowledge MCP Server  
**Tech Stack**: Python 3.14+, uv, mise, click, MCP SDK, httpx  
**Architecture**: Modular CLI-first design with separation of concerns

## Architecture

```
aws-knowledge-tool/
├── aws_knowledge_tool/
│   ├── __init__.py              # Public API exports, version
│   ├── cli.py                   # CLI entry point (Click group)
│   ├── logging_config.py        # Multi-level verbosity logging setup
│   ├── core/                    # Core library functions (importable)
│   │   ├── __init__.py
│   │   ├── mcp_client.py       # MCP client connection & API calls
│   │   └── exceptions.py       # Custom exceptions
│   ├── commands/                # CLI command implementations
│   │   ├── __init__.py
│   │   ├── search.py           # Search command
│   │   ├── read.py             # Read command
│   │   ├── recommend.py        # Recommend command
│   │   └── completion.py       # Shell completion command
│   └── utils.py                 # Shared utilities (formatting, output)
├── tests/
│   ├── __init__.py
│   └── test_utils.py
├── pyproject.toml
├── README.md
├── CLAUDE.md (this file)
├── Makefile
└── .gitignore
```

### Key Design Principles

1. **Separation of Concerns**
   - `core/`: Library functions independent of CLI
   - `commands/`: CLI wrappers with Click decorators
   - `utils.py`: Shared utilities for formatting and output

2. **Exception-Based Errors**
   - Core functions raise exceptions (NOT `sys.exit`)
   - CLI handles formatting and exit codes
   - Exit codes: 0=success, 1=client error, 2=server error, 3=network error

3. **Composable Output**
   - JSON/Markdown → stdout (for piping)
   - Logs/errors → stderr
   - Multi-level verbosity: `-v` (INFO), `-vv` (DEBUG), `-vvv` (TRACE)
   - `--quiet`: Suppress all stderr except errors

4. **Type Safety**
   - Strict mypy checks
   - Comprehensive type hints
   - No Any types in public APIs

## Development Commands

### Quick Start
```bash
uv sync                          # Install dependencies
uv run aws-knowledge-tool --help # Test CLI
```

### Quality Checks
```bash
make format      # Auto-format with ruff
make lint        # Lint with ruff
make typecheck   # Type check with mypy (strict)
make test        # Run pytest suite
make check       # Run all checks (lint + typecheck + test + security)
make pipeline    # Full workflow: format, lint, typecheck, test, security, build, install-global
```

### Security Scanning
```bash
make security-bandit      # Python security linting (SQL injection, hardcoded secrets)
make security-pip-audit   # Dependency vulnerability scanning (CVEs)
make security-gitleaks    # Secret/API key detection in code and git history
make security             # Run all security checks
```

**Security Tools**:
- **bandit** - Fast Python security linter (~2-3 seconds)
- **pip-audit** - Official PyPA dependency vulnerability scanner (~2-3 seconds)
- **gitleaks** - Blazing fast secret detection (~1 second)

**Prerequisites**: Install gitleaks separately (`brew install gitleaks` on macOS)

All security checks are integrated into `make check` and `make pipeline`.

### Build & Install
```bash
make build               # Build wheel package
make install-global      # Install globally with uv tool
make clean               # Remove build artifacts
```

## CLI Commands

### search - Search AWS Documentation

**Format**: `aws-knowledge-tool search QUERY [OPTIONS]`

**Arguments**:
- `QUERY` (positional, optional if `--stdin`): Search query

**Options**:
- `--limit N` / `-l N`: Maximum results (default: 10)
- `--offset M` / `-o M`: Skip first M results (default: 0)
- `--json`: Output JSON format
- `--markdown`: Output markdown format (default)
- `--stdin`: Read query from stdin
- `-v` / `--verbose`: Enable verbose output (use `-v` for INFO, `-vv` for DEBUG, `-vvv` for TRACE)
- `--quiet` / `-q`: Suppress non-essential output

**Implementation**: `aws_knowledge_tool/commands/search.py`

### read - Read AWS Documentation

**Format**: `aws-knowledge-tool read URL [OPTIONS]`

**Arguments**:
- `URL` (positional, optional if `--stdin`): AWS documentation URL

**Options**:
- `--start-index N` / `-s N`: Starting character index
- `--max-length M` / `-m M`: Maximum characters to fetch
- `--json`: Output JSON format
- `--markdown`: Output markdown format (default)
- `--stdin`: Read URL from stdin
- `-v` / `--verbose`: Enable verbose output (use `-v` for INFO, `-vv` for DEBUG, `-vvv` for TRACE)
- `--quiet` / `-q`: Suppress non-essential output

**URL Validation**: Must be from `docs.aws.amazon.com` or `aws.amazon.com`

**Implementation**: `aws_knowledge_tool/commands/read.py`

### recommend - Get Documentation Recommendations

**Format**: `aws-knowledge-tool recommend URL [OPTIONS]`

**Arguments**:
- `URL` (positional, optional if `--stdin`): AWS documentation URL

**Options**:
- `--type TYPE` / `-t TYPE`: Filter by type (highly_rated, new, similar, journey)
- `--limit N` / `-l N`: Max results per category (default: 5)
- `--offset M` / `-o M`: Skip first M per category (default: 0)
- `--json`: Output JSON format
- `--markdown`: Output markdown format (default)
- `--stdin`: Read URL from stdin
- `-v` / `--verbose`: Enable verbose output (use `-v` for INFO, `-vv` for DEBUG, `-vvv` for TRACE)
- `--quiet` / `-q`: Suppress non-essential output

**Implementation**: `aws_knowledge_tool/commands/recommend.py`

### completion - Generate Shell Completion

**Format**: `aws-knowledge-tool completion SHELL`

**Arguments**:
- `SHELL` (positional): The shell type (bash, zsh, fish)

**Description**: Generates shell completion scripts following the pattern used by popular tools like kubectl, helm, and docker. Provides tab completion for commands, options, and arguments.

**Supported Shells**:
- Bash (≥ 4.4)
- Zsh (any recent version)
- Fish (≥ 3.0)
- PowerShell: ❌ Not supported by Click

**Installation Methods**:

```bash
# Temporary (current session only)
eval "$(aws-knowledge-tool completion bash)"
eval "$(aws-knowledge-tool completion zsh)"
aws-knowledge-tool completion fish | source

# Permanent (add to shell config)
echo 'eval "$(aws-knowledge-tool completion bash)"' >> ~/.bashrc
echo 'eval "$(aws-knowledge-tool completion zsh)"' >> ~/.zshrc

# File-based (better performance)
aws-knowledge-tool completion bash > ~/.aws-knowledge-tool-complete.bash
echo 'source ~/.aws-knowledge-tool-complete.bash' >> ~/.bashrc
```

**Implementation**: `aws_knowledge_tool/commands/completion.py`

**Pattern**: Follows the Click Shell Completion Pattern from Obsidian knowledge base (`click-shell-completion-pattern.md`)

**Key Features**:
- User-friendly `completion <shell>` command instead of environment variables
- Self-documenting help text with installation instructions
- Consistent with industry standard CLI tools
- Built-in help: `aws-knowledge-tool completion --help`

## Multi-Level Verbosity Logging

### Overview

The tool implements progressive logging detail following the Obsidian knowledge base pattern from `implementing-multi-level-verbosity-python-logging.md`.

**Implementation**: `aws_knowledge_tool/logging_config.py`

### Logging Levels

| Verbose Count | Level | Description | Use Case |
|---------------|-------|-------------|----------|
| 0 (no flag) | WARNING | Errors and warnings only | Production, quiet mode |
| 1 (`-v`) | INFO | + Operations and progress | Normal debugging |
| 2 (`-vv`) | DEBUG | + Detailed info, full tracebacks | Development, troubleshooting |
| 3+ (`-vvv`) | TRACE | + Library internals | Deep debugging |

### Key Features

1. **Progressive Detail**: Each level adds information without removing previous levels
2. **Stderr Routing**: All logs to stderr, stdout clean for data
3. **Count-Based Options**: Click `count=True` instead of `is_flag=True`
4. **Exception Tracebacks**: Full tracebacks only with `-vv` or `-vvv`
5. **Library Control**: Dependent library logging (MCP, httpx, httpcore, anyio) only at `-vvv`

### Implementation Pattern

All commands follow this pattern:

```python
@click.option(
    "-v",
    "--verbose",
    count=True,  # KEY: count=True instead of is_flag=True
    help="Enable verbose output (use -v for INFO, -vv for DEBUG, -vvv for TRACE)",
)
def command_name(
    verbose: int,  # Integer, not boolean
    ...
) -> None:
    # Setup logging at command start
    setup_logging(verbose)
    logger = get_logger(__name__)

    # Use structured logging
    logger.info("Operation started")
    logger.debug("Detailed information")
    logger.error("Error occurred")
```

### Logging Configuration

```python
def setup_logging(verbose_count: int = 0) -> None:
    """Configure logging based on verbosity level.

    Args:
        verbose_count: Number of -v flags (0-3+)
            0: WARNING level (quiet mode)
            1: INFO level (normal verbose)
            2: DEBUG level (detailed debugging)
            3+: DEBUG + enable dependent library logging (trace mode)
    """
    if verbose_count == 0:
        level = logging.WARNING
    elif verbose_count == 1:
        level = logging.INFO
    elif verbose_count >= 2:
        level = logging.DEBUG

    logging.basicConfig(
        level=level,
        format="[%(levelname)s] %(message)s",
        stream=sys.stderr,
        force=True,
    )

    # Configure dependent library loggers at TRACE level (-vvv)
    if verbose_count >= 3:
        logging.getLogger("mcp").setLevel(logging.DEBUG)
        logging.getLogger("httpx").setLevel(logging.DEBUG)
        logging.getLogger("httpcore").setLevel(logging.DEBUG)
        logging.getLogger("anyio").setLevel(logging.DEBUG)
```

## Library Usage

### Programmatic API

```python
import asyncio
from aws_knowledge_tool import MCPClient

async def example():
    async with MCPClient() as client:
        # Search
        results = await client.search_documentation("Lambda", limit=5)
        
        # Read
        content = await client.read_documentation("https://docs.aws.amazon.com/...")
        
        # Recommend
        recommendations = await client.get_recommendations("https://docs.aws.amazon.com/...")

asyncio.run(example())
```

### Public API Exports

From `aws_knowledge_tool`:
- `MCPClient`: MCP client for AWS Knowledge Server
- `AWSKnowledgeError`: Base exception
- `ClientError`: Client-side errors (exit code 1)
- `ServerError`: Server-side errors (exit code 2)
- `NetworkError`: Network errors (exit code 3)
- `__version__`: Package version

## Code Standards

- **Python Version**: 3.14+
- **Type Hints**: Required for all functions
- **Docstrings**: Required for all public functions (Google style)
- **Line Length**: 100 characters
- **Formatting**: ruff
- **Linting**: ruff with E, F, I, N, W, UP rules
- **Type Checking**: mypy strict mode

### Module Docstring Template

```python
"""
[Module description].

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""
```

## Testing

```bash
# Run all tests
make test

# Run with verbose output
uv run pytest tests/ -v

# Run specific test file
uv run pytest tests/test_utils.py

# Run with coverage
uv run pytest tests/ --cov=aws_knowledge_tool
```

## Important Notes

### Core Dependencies

- **click** (≥8.1.7): CLI framework
- **mcp** (≥1.0.0): Model Context Protocol SDK
- **httpx** (≥0.25.0): HTTP client for async requests

### MCP Client Implementation

**Current Status**: Stub implementation using memory streams

**Issue**: MCP Python SDK uses stdio-based transport (read_stream/write_stream) for ClientSession, not HTTP transport. The research examples showing HTTP usage are simplified or outdated.

**Location**: `aws_knowledge_tool/core/mcp_client.py:39-63`

**What Works**:
- Type checking passes
- Architecture is correct
- API surface is complete

**What Needs Implementation**:
- Proper HTTP transport using anyio streams
- HTTP client wrapper for MCP protocol
- See: https://github.com/modelcontextprotocol/python-sdk

### Version Synchronization

**CRITICAL**: Keep version synced across:
1. `pyproject.toml` → `[project] version = "X.Y.Z"`
2. `cli.py` → `@click.version_option(version="X.Y.Z")`  
3. `__init__.py` → `__version__ = "X.Y.Z"`

### Installation from Wheel

When using `make install-global`, install from the wheel file to avoid caching:

```makefile
install-global:
    uv tool install dist/aws_knowledge_tool-0.1.0-py3-none-any.whl
```

## Known Issues & Future Fixes

### 1. MCP HTTP Transport (High Priority)

**Problem**: ClientSession requires read_stream/write_stream, not HTTP client

**Current Workaround**: Stub implementation with memory streams

**Steps to Fix**:
1. Research MCP Python SDK HTTP examples
2. Implement HTTP-to-stream adapter using anyio
3. Update `mcp_client.py` connect() method
4. Add integration tests

**References**:
- https://github.com/modelcontextprotocol/python-sdk
- Research document: `/Users/dennisvriend/projects/aws-knowledge-tool/references/research.md`

## Project Structure Details

### Entry Points

- **CLI**: `aws_knowledge_tool.cli:main` (registered in pyproject.toml)
- **Library**: Import from `aws_knowledge_tool` package

### File Responsibilities

- `cli.py`: Click group, command registration, version display
- `logging_config.py`: Multi-level verbosity logging setup and configuration
- `core/mcp_client.py`: MCP connection, API calls, response parsing
- `core/exceptions.py`: Custom exception hierarchy with exit codes
- `commands/search.py`: Search command implementation
- `commands/read.py`: Read command implementation
- `commands/recommend.py`: Recommend command implementation
- `commands/completion.py`: Shell completion command (bash, zsh, fish)
- `utils.py`: Output formatting, validation, stdin helpers

## Resources

- **AWS Knowledge MCP Server**: https://knowledge-mcp.global.api.aws
- **MCP Specification**: https://modelcontextprotocol.io
- **MCP Python SDK**: https://github.com/modelcontextprotocol/python-sdk
- **Click Shell Completion**: https://click.palletsprojects.com/en/8.1.x/shell-completion/
- **Research Document**: `references/research.md`
- **Obsidian Pattern References**:
  - Multi-level verbosity: `implementing-multi-level-verbosity-python-logging.md`
  - Shell completion: `click-shell-completion-pattern.md`
