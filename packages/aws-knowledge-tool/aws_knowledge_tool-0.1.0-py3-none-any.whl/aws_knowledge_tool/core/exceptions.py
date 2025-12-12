"""Custom exceptions for AWS Knowledge Tool.

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""


class AWSKnowledgeError(Exception):
    """Base exception for AWS Knowledge Tool."""

    def __init__(self, message: str, exit_code: int = 1) -> None:
        """Initialize the exception.

        Args:
            message: Error message
            exit_code: Exit code for CLI (1=client, 2=server, 3=network)
        """
        self.message = message
        self.exit_code = exit_code
        super().__init__(message)


class ClientError(AWSKnowledgeError):
    """Client-side error (invalid input, validation failure)."""

    def __init__(self, message: str) -> None:
        """Initialize client error with exit code 1.

        Args:
            message: Error message
        """
        super().__init__(message, exit_code=1)


class ServerError(AWSKnowledgeError):
    """Server-side error (MCP server error, API error)."""

    def __init__(self, message: str) -> None:
        """Initialize server error with exit code 2.

        Args:
            message: Error message
        """
        super().__init__(message, exit_code=2)


class NetworkError(AWSKnowledgeError):
    """Network-related error (connection failure, timeout)."""

    def __init__(self, message: str) -> None:
        """Initialize network error with exit code 3.

        Args:
            message: Error message
        """
        super().__init__(message, exit_code=3)
