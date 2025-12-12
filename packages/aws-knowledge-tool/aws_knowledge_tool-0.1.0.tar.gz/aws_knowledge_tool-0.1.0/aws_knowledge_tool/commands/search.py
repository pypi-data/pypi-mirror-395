"""Search command for AWS Knowledge Tool.

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""

from typing import Any

import click

from aws_knowledge_tool.core import AWSKnowledgeError, MCPClient
from aws_knowledge_tool.logging_config import get_logger, setup_logging
from aws_knowledge_tool.utils import (
    output_json,
    output_search_results_markdown,
    read_stdin,
)

logger = get_logger(__name__)


@click.command(name="search")
@click.argument("query", required=False)
@click.option(
    "--limit",
    "-l",
    type=int,
    default=10,
    help="Maximum number of results (default: 10)",
    show_default=True,
)
@click.option(
    "--offset",
    "-o",
    type=int,
    default=0,
    help="Skip first N results (default: 0)",
    show_default=True,
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
    help="Read query from stdin for pipeline composition",
)
@click.option(
    "-v",
    "--verbose",
    count=True,  # KEY: count=True instead of is_flag=True
    help="Enable verbose output (use -v for INFO, -vv for DEBUG, -vvv for TRACE)",
)
@click.option(
    "--quiet",
    "-q",
    is_flag=True,
    help="Suppress non-essential output",
)
def search_command(
    query: str | None,
    limit: int,
    offset: int,
    output_json_format: bool,
    output_markdown_format: bool,
    use_stdin: bool,
    verbose: int,  # Changed from bool to int
    quiet: bool,
) -> None:
    """Search AWS documentation using the AWS Knowledge MCP Server.

    Search across AWS documentation, blogs, solutions library, architecture center,
    and prescriptive guidance for content matching your query.

    Examples:

    \b
        # Basic search
        aws-knowledge-tool search "Lambda function URLs"

    \b
        # Search with limit
        aws-knowledge-tool search "S3 bucket versioning" --limit 5

    \b
        # Search with pagination
        aws-knowledge-tool search "EC2 instances" --limit 10 --offset 20

    \b
        # JSON output for processing
        aws-knowledge-tool search "DynamoDB" --json

    \b
        # Pipeline usage with stdin
        echo "Lambda functions" | aws-knowledge-tool search --stdin --json

    \b
        # Verbose mode for debugging
        aws-knowledge-tool search "CloudFormation" -v

    \b
        # Debug mode with full details
        aws-knowledge-tool search "CloudFormation" -vv

    \b
        # Trace mode with library internals
        aws-knowledge-tool search "CloudFormation" -vvv

    \b
    Output Format:
        Default (markdown): Formatted list with rank, title, URL, and context
        JSON: Array of objects with rank_order, title, url, context fields
    """
    # Setup logging based on verbosity count
    setup_logging(verbose)
    logger.info("Search command started")

    try:
        # Get query from stdin or argument
        if use_stdin:
            query = read_stdin()
            logger.info(f"Read query from stdin: {query}")
        elif not query:
            raise click.UsageError("QUERY argument required (or use --stdin)")

        logger.info(f"Searching for: {query}")
        logger.debug(f"Parameters: limit={limit}, offset={offset}")

        # Run synchronous search
        results = _search_sync(query, limit, offset)

        logger.info(f"Found {len(results)} results")

        # Output results
        if output_json_format:
            output_json(results, quiet)
        else:
            output_search_results_markdown(results, quiet)

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


def _search_sync(query: str, limit: int, offset: int) -> list[dict[str, Any]]:
    """Synchronous search implementation.

    Args:
        query: Search query
        limit: Maximum results
        offset: Results to skip

    Returns:
        List of search results
    """
    logger.debug("Connecting to AWS Knowledge API...")

    with MCPClient() as client:
        logger.debug("Connected. Initiating search...")
        results = client.search_documentation(query, limit, offset)
        logger.debug("Search API call complete")
        return results
