"""Recommend command for AWS Knowledge Tool.

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""

from typing import Any

import click

from aws_knowledge_tool.core import AWSKnowledgeError, MCPClient
from aws_knowledge_tool.logging_config import get_logger, setup_logging
from aws_knowledge_tool.utils import (
    output_json,
    output_recommendations_markdown,
    read_stdin,
    validate_url,
)

logger = get_logger(__name__)


@click.command(name="recommend")
@click.argument("url", required=False)
@click.option(
    "--type",
    "-t",
    "recommendation_type",
    type=click.Choice(["highly_rated", "new", "similar", "journey"], case_sensitive=False),
    help="Filter by recommendation type",
)
@click.option(
    "--limit",
    "-l",
    type=int,
    default=5,
    help="Maximum results per category (default: 5)",
    show_default=True,
)
@click.option(
    "--offset",
    "-o",
    type=int,
    default=0,
    help="Skip first N results per category (default: 0)",
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
def recommend_command(
    url: str | None,
    recommendation_type: str | None,
    limit: int,
    offset: int,
    output_json_format: bool,
    output_markdown_format: bool,
    use_stdin: bool,
    verbose: int,
    quiet: bool,
) -> None:
    """Get related AWS documentation recommendations.

    Discover related documentation through four recommendation types:
    - highly_rated: Popular pages within the same AWS service
    - new: Recently added pages (useful for finding new features)
    - similar: Pages covering similar topics
    - journey: Pages commonly viewed next by other users

    Examples:

    \b
        # Get all recommendations
        aws-knowledge-tool recommend "https://docs.aws.amazon.com/lambda/latest/dg/welcome.html"

    \b
        # Filter by type
        aws-knowledge-tool recommend "https://docs.aws.amazon.com/..." --type new

    \b
        # Limit results per category
        aws-knowledge-tool recommend "https://docs.aws.amazon.com/..." --limit 3

    \b
        # JSON output for processing
        aws-knowledge-tool recommend "https://docs.aws.amazon.com/..." --json

    \b
        # Pipeline usage
        aws-knowledge-tool search "Lambda" --json | jq -r '.[0].url' | \\
            aws-knowledge-tool recommend --stdin --type similar

    \b
        # Pagination per category
        aws-knowledge-tool recommend "https://docs.aws.amazon.com/..." \\
            --limit 5 --offset 5

    \b
    Output Format:
        Default: Grouped by category with title, URL, and context
        JSON: Object with category keys and arrays of recommendation objects
    """
    # Setup logging based on verbosity count
    setup_logging(verbose)
    logger.info("Recommend command started")

    try:
        # Get URL from stdin or argument
        if use_stdin:
            url = read_stdin()
            logger.info(f"Read URL from stdin: {url}")
        elif not url:
            raise click.UsageError("URL argument required (or use --stdin)")

        # Validate URL
        validate_url(url)
        logger.info(f"Getting recommendations for: {url}")

        if recommendation_type:
            logger.debug(f"Filter type: {recommendation_type}")
        logger.debug(f"Parameters: limit={limit}, offset={offset}")

        # Run synchronous recommend
        recommendations = _recommend_sync(url, recommendation_type, limit, offset)

        logger.info("Retrieved recommendations")

        # Output recommendations
        if output_json_format:
            output_json(recommendations, quiet)
        else:
            output_recommendations_markdown(recommendations, quiet)

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


def _recommend_sync(
    url: str,
    recommendation_type: str | None,
    limit: int,
    offset: int,
) -> dict[str, Any]:
    """Synchronous recommend implementation.

    Args:
        url: Documentation URL
        recommendation_type: Filter by type
        limit: Maximum results per category
        offset: Results to skip per category

    Returns:
        Dict of recommendations by category
    """
    logger.debug("Connecting to AWS Knowledge API...")

    with MCPClient() as client:
        logger.debug("Connected. Getting recommendations...")
        recommendations = client.get_recommendations(url, recommendation_type, limit, offset)
        logger.debug("Recommendations API call complete")
        return recommendations
