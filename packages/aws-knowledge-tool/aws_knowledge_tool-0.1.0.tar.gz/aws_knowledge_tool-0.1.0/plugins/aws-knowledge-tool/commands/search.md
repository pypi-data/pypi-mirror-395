---
description: Search AWS documentation with full-text search
argument-hint: query
---

Search AWS documentation for QUERY and return results with pagination.

## Usage

```bash
aws-knowledge-tool search "QUERY" [--limit N] [--offset M] [--json]
```

## Arguments

- `QUERY`: Search query (required)
- `--limit N` / `-l N`: Max results (default: 10)
- `--offset M` / `-o M`: Skip first M results (default: 0)
- `--json`: Output JSON format
- `-v/-vv/-vvv`: Verbosity (INFO/DEBUG/TRACE)

## Examples

```bash
# Basic search
aws-knowledge-tool search "Lambda function URLs"

# With limit and JSON output
aws-knowledge-tool search "S3 versioning" --limit 5 --json

# Paginated search
aws-knowledge-tool search "DynamoDB" --limit 10 --offset 20
```

## Output

Returns list of search results with:
- `title`: Page title
- `url`: Documentation URL
- `context`: Summary snippet
- `rank_order`: Relevance ranking
