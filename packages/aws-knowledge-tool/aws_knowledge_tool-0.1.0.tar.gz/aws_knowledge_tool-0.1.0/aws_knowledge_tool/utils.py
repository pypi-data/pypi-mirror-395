"""Utility functions for aws-knowledge-tool.

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""

import json
import sys
from typing import Any

import click


def output_json(data: Any, quiet: bool = False) -> None:
    """Output data as JSON to stdout.

    Args:
        data: Data to output
        quiet: If True, suppress output
    """
    if not quiet:
        click.echo(json.dumps(data, indent=2, ensure_ascii=False))


def output_markdown(content: str, quiet: bool = False) -> None:
    """Output content as markdown to stdout.

    Args:
        content: Markdown content to output
        quiet: If True, suppress output
    """
    if not quiet:
        click.echo(content)


def output_search_results_markdown(results: list[dict[str, Any]], quiet: bool = False) -> None:
    """Output search results in markdown format.

    Args:
        results: List of search results
        quiet: If True, suppress output
    """
    if quiet:
        return

    if not results:
        click.echo("No results found.")
        return

    click.echo(f"Found {len(results)} results:\n")

    for result in results:
        rank = result.get("rank_order", "N/A")
        title = result.get("title", "Untitled")
        url = result.get("url", "")
        context = result.get("context", "")

        click.echo(f"[{rank}] {title}")
        click.echo(f"    URL: {url}")
        if context:
            # Truncate context if too long
            display_context = context[:200] + "..." if len(context) > 200 else context
            click.echo(f"    {display_context}")
        click.echo()


def output_recommendations_markdown(
    recommendations: dict[str, list[dict[str, Any]]], quiet: bool = False
) -> None:
    """Output recommendations in markdown format.

    Args:
        recommendations: Dict of recommendation categories
        quiet: If True, suppress output
    """
    if quiet:
        return

    if not recommendations:
        click.echo("No recommendations found.")
        return

    for category, pages in recommendations.items():
        if not pages:
            continue

        category_display = category.upper().replace("_", " ")
        click.echo(f"\n{category_display}:")

        for page in pages:
            title = page.get("title", "Untitled")
            url = page.get("url", "")
            context = page.get("context", "")

            click.echo(f"  - {title}")
            click.echo(f"    {url}")
            if context:
                click.echo(f"    {context[:150]}...")
        click.echo()


def log_verbose(message: str, verbose: bool = False) -> None:
    """Log verbose message to stderr.

    Args:
        message: Message to log
        verbose: If True, output message
    """
    if verbose:
        click.echo(f"[VERBOSE] {message}", err=True)


def log_error(message: str) -> None:
    """Log error message to stderr.

    Args:
        message: Error message
    """
    click.echo(f"[ERROR] {message}", err=True)


def read_stdin() -> str:
    """Read input from stdin.

    Returns:
        Content from stdin, stripped

    Raises:
        click.ClickException: If stdin is empty
    """
    if sys.stdin.isatty():
        raise click.ClickException("No input provided via stdin. Use --stdin with piped input.")

    content = sys.stdin.read().strip()
    if not content:
        raise click.ClickException("Empty input received from stdin.")

    return content


def validate_url(url: str) -> None:
    """Validate AWS documentation URL.

    Args:
        url: URL to validate

    Raises:
        click.BadParameter: If URL is invalid
    """
    valid_domains = ["docs.aws.amazon.com", "aws.amazon.com"]

    if not url.startswith(("http://", "https://")):
        raise click.BadParameter(f"URL must start with http:// or https://: {url}")

    # Extract domain
    domain_start = url.find("://") + 3
    domain_end = url.find("/", domain_start)
    domain = url[domain_start:domain_end] if domain_end != -1 else url[domain_start:]

    if not any(domain == valid or domain.endswith(f".{valid}") for valid in valid_domains):
        raise click.BadParameter(
            f"URL must be from {' or '.join(valid_domains)} domain. Got: {domain}"
        )
