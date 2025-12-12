"""Read command for AWS Knowledge Tool.

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""

import click

from aws_knowledge_tool.core import AWSKnowledgeError, MCPClient
from aws_knowledge_tool.logging_config import get_logger, setup_logging
from aws_knowledge_tool.utils import (
    output_json,
    output_markdown,
    read_stdin,
    validate_url,
)

logger = get_logger(__name__)


@click.command(name="read")
@click.argument("url", required=False)
@click.option(
    "--start-index",
    "-s",
    type=int,
    help="Starting character index for pagination",
)
@click.option(
    "--max-length",
    "-m",
    type=int,
    help="Maximum characters to fetch",
)
@click.option(
    "--json",
    "output_json_format",
    is_flag=True,
    help="Output JSON format",
)
@click.option(
    "--markdown",
    "output_markdown_format",
    is_flag=True,
    help="Output markdown format (default)",
)
@click.option(
    "--stdin",
    "use_stdin",
    is_flag=True,
    help="Read URL from stdin for pipeline composition",
)
@click.option(
    "-v",
    "--verbose",
    count=True,
    help="Enable verbose output (use -v for INFO, -vv for DEBUG, -vvv for TRACE)",
)
@click.option(
    "--quiet",
    "-q",
    is_flag=True,
    help="Suppress non-essential output",
)
def read_command(
    url: str | None,
    start_index: int | None,
    max_length: int | None,
    output_json_format: bool,
    output_markdown_format: bool,
    use_stdin: bool,
    verbose: int,
    quiet: bool,
) -> None:
    """Read AWS documentation page and convert to markdown.

    Fetch and convert AWS documentation pages from docs.aws.amazon.com or
    aws.amazon.com domains. Supports pagination for long documents.

    Examples:

    \b
        # Read full document
        aws-knowledge-tool read "https://docs.aws.amazon.com/lambda/latest/dg/welcome.html"

    \b
        # Read with pagination
        aws-knowledge-tool read "https://docs.aws.amazon.com/..." \\
            --start-index 5000 --max-length 2000

    \b
        # JSON output
        aws-knowledge-tool read "https://docs.aws.amazon.com/..." --json

    \b
        # Pipeline from search
        aws-knowledge-tool search "Lambda" --json | jq -r '.[0].url' | \\
            aws-knowledge-tool read --stdin

    \b
        # Read and save to file
        aws-knowledge-tool read "https://docs.aws.amazon.com/..." > lambda-docs.md

    \b
    Output Format:
        Default: Markdown-formatted documentation content
        JSON: String containing markdown content
    """
    # Setup logging based on verbosity count
    setup_logging(verbose)
    logger.info("Read command started")

    try:
        # Get URL from stdin or argument
        if use_stdin:
            url = read_stdin()
            logger.info(f"Read URL from stdin: {url}")
        elif not url:
            raise click.UsageError("URL argument required (or use --stdin)")

        # Validate URL
        validate_url(url)
        logger.info(f"Reading documentation from: {url}")

        if start_index is not None:
            logger.debug(f"Start index: {start_index}")
        if max_length is not None:
            logger.debug(f"Max length: {max_length}")

        # Run synchronous read
        content = _read_sync(url, start_index, max_length)

        logger.info(f"Fetched {len(content)} characters")

        # Output content
        if output_json_format:
            output_json({"url": url, "content": content}, quiet)
        else:
            output_markdown(content, quiet)

    except AWSKnowledgeError as e:
        logger.error(e.message)
        logger.debug("Error details:", exc_info=True)
        raise click.exceptions.Exit(e.exit_code)
    except click.ClickException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        logger.debug("Full traceback:", exc_info=True)
        raise click.exceptions.Exit(1)


def _read_sync(
    url: str,
    start_index: int | None,
    max_length: int | None,
) -> str:
    """Synchronous read implementation.

    Args:
        url: Documentation URL
        start_index: Starting character index
        max_length: Maximum characters

    Returns:
        Markdown content
    """
    logger.debug("Connecting to AWS Knowledge API...")

    with MCPClient() as client:
        logger.debug("Connected. Reading documentation...")
        content = client.read_documentation(url, start_index, max_length)
        logger.debug("Read API call complete")
        return content
