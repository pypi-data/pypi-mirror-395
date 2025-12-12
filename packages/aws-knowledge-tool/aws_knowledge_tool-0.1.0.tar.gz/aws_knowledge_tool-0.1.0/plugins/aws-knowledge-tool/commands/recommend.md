---
description: Get related AWS documentation recommendations
argument-hint: url
---

Discover related documentation through four recommendation types.

## Usage

```bash
aws-knowledge-tool recommend "URL" [--type TYPE] [--limit N] [--offset M] [--json]
```

## Arguments

- `URL`: AWS documentation URL (required)
- `--type TYPE` / `-t TYPE`: Filter by type
  - `highly_rated`: Popular pages within same service
  - `new`: Recently added pages (find new features)
  - `similar`: Pages covering similar topics
  - `journey`: Pages commonly viewed next
- `--limit N` / `-l N`: Max results per category (default: 5)
- `--offset M` / `-o M`: Skip first M per category (default: 0)
- `--json`: Output JSON format
- `-v/-vv/-vvv`: Verbosity (INFO/DEBUG/TRACE)

## Examples

```bash
# Get all recommendations
aws-knowledge-tool recommend "https://docs.aws.amazon.com/lambda/latest/dg/welcome.html"

# Filter by type to find new features
aws-knowledge-tool recommend "https://docs.aws.amazon.com/..." --type new

# JSON output for processing
aws-knowledge-tool recommend "https://docs.aws.amazon.com/..." --json --limit 3
```

## Output

Returns dict with recommendation categories and their pages (title, url, context).
