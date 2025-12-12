---
description: Read AWS documentation page as markdown
argument-hint: url
---

Read AWS documentation from URL and convert to markdown format.

## Usage

```bash
aws-knowledge-tool read "URL" [--start-index N] [--max-length M] [--json]
```

## Arguments

- `URL`: AWS documentation URL (required)
- `--start-index N` / `-s N`: Starting character index
- `--max-length M` / `-m M`: Maximum characters to fetch
- `--json`: Output JSON format
- `-v/-vv/-vvv`: Verbosity (INFO/DEBUG/TRACE)

## Examples

```bash
# Read full document
aws-knowledge-tool read "https://docs.aws.amazon.com/lambda/latest/dg/welcome.html"

# Read with pagination
aws-knowledge-tool read "https://docs.aws.amazon.com/..." --start-index 5000 --max-length 2000

# Pipeline from search
aws-knowledge-tool search "Lambda" --json | jq -r '.[0].url' | aws-knowledge-tool read --stdin
```

## Output

Returns markdown-formatted documentation content from docs.aws.amazon.com or aws.amazon.com domains.
