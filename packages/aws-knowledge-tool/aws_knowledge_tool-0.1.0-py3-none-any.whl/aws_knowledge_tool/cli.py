"""CLI entry point for aws-knowledge-tool.

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""

import click

from aws_knowledge_tool.commands import (
    completion_command,
    read_command,
    recommend_command,
    search_command,
)


@click.group()
@click.version_option(version="0.1.0", prog_name="aws-knowledge-tool")
def main() -> None:
    """AWS Knowledge Tool - Query AWS documentation via MCP Server.

    A CLI tool for searching, reading, and discovering AWS documentation through
    the AWS Knowledge MCP Server. Features agent-friendly design with composable
    commands, JSON output, and pipeline support.

    Commands:
      search      Search AWS documentation
      read        Read AWS documentation pages
      recommend   Get related documentation recommendations
      completion  Generate shell completion script

    Examples:

    \b
        # Search for Lambda documentation
        aws-knowledge-tool search "Lambda function URLs"

    \b
        # Read a documentation page
        aws-knowledge-tool read "https://docs.aws.amazon.com/lambda/latest/dg/welcome.html"

    \b
        # Get recommendations for a page
        aws-knowledge-tool recommend "https://docs.aws.amazon.com/..." --type new

    \b
        # Pipeline composition
        aws-knowledge-tool search "Lambda" --json | \\
            jq -r '.[0].url' | \\
            aws-knowledge-tool read --stdin

    For detailed command help:
        aws-knowledge-tool COMMAND --help
    """


# Register commands
main.add_command(search_command)
main.add_command(read_command)
main.add_command(recommend_command)
main.add_command(completion_command)


if __name__ == "__main__":
    main()
