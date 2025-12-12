"""HTTP client for AWS Knowledge API.

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""

import json
from typing import Any

import requests

from aws_knowledge_tool.core.exceptions import ClientError, NetworkError, ServerError


class MCPClient:
    """Client for AWS Knowledge HTTP API."""

    SERVER_URL = "https://knowledge-mcp.global.api.aws"

    def __init__(self, timeout: float = 30.0) -> None:
        """Initialize HTTP client.

        Args:
            timeout: Request timeout in seconds
        """
        self.timeout = timeout
        self._session: requests.Session | None = None

    def __enter__(self) -> MCPClient:
        """Context manager entry."""
        self.connect()
        return self

    def __exit__(self, *args: Any) -> None:
        """Context manager exit."""
        self.close()

    def connect(self) -> None:
        """Initialize HTTP session.

        Creates a requests.Session for connection pooling and persistent settings.
        """
        self._session = requests.Session()
        self._session.headers.update(
            {
                "Content-Type": "application/json",
                "Accept": "application/json",
            }
        )

    def close(self) -> None:
        """Close HTTP session."""
        if self._session:
            self._session.close()
            self._session = None

    def _call_tool(self, tool_name: str, arguments: dict[str, Any]) -> Any:
        """Call MCP tool via JSON-RPC 2.0 over HTTP.

        Args:
            tool_name: Name of tool (e.g., "aws___search_documentation")
            arguments: Tool arguments

        Returns:
            Parsed result from tool

        Raises:
            NetworkError: If request fails
            ServerError: If server returns error or MCP error
            ClientError: If client error (4xx status)
        """
        if not self._session:
            raise NetworkError("HTTP session not initialized. Call connect() first.")

        try:
            # Format as JSON-RPC 2.0 request
            jsonrpc_request = {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "tools/call",
                "params": {
                    "name": tool_name,
                    "arguments": arguments,
                },
            }

            # Make HTTP POST request to MCP endpoint
            response = self._session.post(
                self.SERVER_URL,
                json=jsonrpc_request,
                timeout=self.timeout,
            )

            # Handle HTTP errors
            if 400 <= response.status_code < 500:
                raise ClientError(f"Client error {response.status_code}: {response.text}")
            elif 500 <= response.status_code < 600:
                raise ServerError(f"Server error {response.status_code}: {response.text}")

            response.raise_for_status()

            # Parse JSON-RPC response
            rpc_response = response.json()

            # Check for JSON-RPC error
            if "error" in rpc_response:
                error = rpc_response["error"]
                error_code = error.get("code", "unknown")
                error_msg = error.get("message", "Unknown error")
                raise ServerError(f"MCP error {error_code}: {error_msg}")

            # Extract result from JSON-RPC response
            if "result" not in rpc_response:
                raise ServerError("Invalid MCP response: missing 'result' field")

            result = rpc_response["result"]

            # MCP wraps tool results in 'content' array with text/data
            if isinstance(result, dict) and "content" in result:
                content_items = result["content"]
                if content_items and len(content_items) > 0:
                    first_item = content_items[0]
                    # Return text or data from first content item
                    if "text" in first_item:
                        # Try to parse as JSON if it looks like JSON
                        text = first_item["text"]
                        try:
                            return json.loads(text)
                        except json.JSONDecodeError:
                            return text
                    elif "data" in first_item:
                        return first_item["data"]

            return result

        except requests.exceptions.Timeout as e:
            raise NetworkError(f"Request timeout after {self.timeout}s: {e}") from e
        except requests.exceptions.ConnectionError as e:
            raise NetworkError(f"Connection error: {e}") from e
        except requests.exceptions.RequestException as e:
            raise NetworkError(f"HTTP request failed: {e}") from e
        except json.JSONDecodeError as e:
            raise ServerError(f"Invalid JSON response: {e}") from e

    def search_documentation(
        self, search_phrase: str, limit: int = 10, offset: int = 0
    ) -> list[dict[str, Any]]:
        """Search AWS documentation.

        Args:
            search_phrase: Search query
            limit: Maximum number of results
            offset: Number of results to skip

        Returns:
            List of search results with url, title, context, rank_order

        Raises:
            ServerError: If search fails
            NetworkError: If not connected
        """
        # Note: AWS API doesn't support offset directly
        # We fetch limit + offset and slice client-side
        actual_limit = limit + offset

        response = self._call_tool(
            "aws___search_documentation",
            {"search_phrase": search_phrase, "limit": actual_limit},
        )

        # Extract results from response structure: {content: {result: [...]}}
        results: list[dict[str, Any]] = []
        if isinstance(response, dict) and "content" in response:
            content = response["content"]
            if isinstance(content, dict) and "result" in content:
                results = content["result"]
        elif isinstance(response, list):
            # Already a list
            results = response
        else:
            raise ServerError(f"Unexpected response structure: {type(response)}")

        # Apply offset client-side
        return results[offset : offset + limit]

    def read_documentation(
        self,
        url: str,
        start_index: int | None = None,
        max_length: int | None = None,
    ) -> str:
        """Read AWS documentation page as markdown.

        Args:
            url: AWS documentation URL
            start_index: Starting character index for pagination
            max_length: Maximum characters to return

        Returns:
            Markdown-formatted documentation content

        Raises:
            ServerError: If read fails
            NetworkError: If not connected
        """
        arguments: dict[str, Any] = {"url": url}

        if start_index is not None:
            arguments["start_index"] = start_index
        if max_length is not None:
            arguments["max_length"] = max_length

        response = self._call_tool("aws___read_documentation", arguments)

        # Extract markdown from response structure: {content: {result: "..."}}
        if isinstance(response, dict) and "content" in response:
            content = response["content"]
            if isinstance(content, dict) and "result" in content:
                result = content["result"]
                return str(result) if not isinstance(result, str) else result

        # Fallback: return as-is if already a string
        return response if isinstance(response, str) else str(response)

    def get_recommendations(
        self,
        url: str,
        recommendation_type: str | None = None,
        limit: int = 5,
        offset: int = 0,
    ) -> dict[str, list[dict[str, Any]]]:
        """Get documentation recommendations.

        Args:
            url: AWS documentation URL
            recommendation_type: Filter by type (highly_rated, new, similar, journey)
            limit: Maximum results per category
            offset: Number of results to skip per category

        Returns:
            Dict with recommendation categories and their pages

        Raises:
            ServerError: If recommendation fetch fails
            NetworkError: If not connected
        """
        response = self._call_tool("aws___recommend", {"url": url})

        # Extract results from response structure: {content: {result: [...]}} or {...}
        raw_result: list[dict[str, Any]] | dict[str, list[dict[str, Any]]] = []
        if isinstance(response, dict) and "content" in response:
            content = response["content"]
            if isinstance(content, dict) and "result" in content:
                raw_result = content["result"]
        elif isinstance(response, (dict, list)):
            # Already in expected format
            raw_result = response
        else:
            raise ServerError(f"Unexpected response structure: {type(response)}")

        # Handle two possible formats: flat list or categorized dict
        results: dict[str, list[dict[str, Any]]] = {}
        if isinstance(raw_result, list):
            # Flat list format - wrap in "all" category
            results = {"all": raw_result}
        elif isinstance(raw_result, dict):
            # Categorized format
            results = raw_result
        else:
            raise ServerError(f"Unexpected result format: {type(raw_result)}")

        # Filter by type if specified
        if recommendation_type:
            if recommendation_type not in results:
                raise ServerError(
                    f"Invalid recommendation type: {recommendation_type}. "
                    f"Valid types: {', '.join(results.keys())}"
                )
            results = {recommendation_type: results[recommendation_type]}

        # Apply limit and offset to each category
        filtered_results: dict[str, list[dict[str, Any]]] = {}
        for category, pages in results.items():
            if isinstance(pages, list):
                filtered_results[category] = pages[offset : offset + limit]
            else:
                # If pages is not a list, it might be improperly structured
                raise ServerError(
                    f"Invalid recommendation data structure for category '{category}': "
                    f"expected list, got {type(pages)}"
                )

        return filtered_results
