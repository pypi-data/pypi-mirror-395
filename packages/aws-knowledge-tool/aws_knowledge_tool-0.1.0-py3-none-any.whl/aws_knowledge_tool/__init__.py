"""AWS Knowledge Tool - CLI for querying AWS documentation via MCP Server.

A professional CLI tool for searching, reading, and discovering AWS documentation
through the AWS Knowledge MCP Server. Features agent-friendly design with composable
commands, JSON output, and pipeline support.

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""

from aws_knowledge_tool.core import (
    AWSKnowledgeError,
    ClientError,
    MCPClient,
    NetworkError,
    ServerError,
)

__version__ = "0.1.0"

__all__ = [
    "__version__",
    "MCPClient",
    "AWSKnowledgeError",
    "ClientError",
    "ServerError",
    "NetworkError",
]
