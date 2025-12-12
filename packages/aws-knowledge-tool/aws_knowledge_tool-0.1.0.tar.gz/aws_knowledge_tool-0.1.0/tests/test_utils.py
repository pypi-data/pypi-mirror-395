"""Tests for aws_knowledge_tool.utils module.

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""

import pytest

from aws_knowledge_tool.utils import validate_url


def test_validate_url_valid_docs_domain() -> None:
    """Test URL validation with valid docs.aws.amazon.com domain."""
    # Should not raise any exception
    validate_url("https://docs.aws.amazon.com/lambda/latest/dg/welcome.html")


def test_validate_url_valid_aws_domain() -> None:
    """Test URL validation with valid aws.amazon.com domain."""
    # Should not raise any exception
    validate_url("https://aws.amazon.com/blogs/developer/example")


def test_validate_url_invalid_protocol() -> None:
    """Test URL validation with invalid protocol."""
    with pytest.raises(Exception) as exc_info:
        validate_url("ftp://docs.aws.amazon.com/test")
    assert "must start with http" in str(exc_info.value).lower()


def test_validate_url_invalid_domain() -> None:
    """Test URL validation with invalid domain."""
    with pytest.raises(Exception) as exc_info:
        validate_url("https://example.com/docs")
    assert "must be from" in str(exc_info.value).lower()


def test_validate_url_http_protocol() -> None:
    """Test URL validation with http protocol."""
    # Should not raise exception (will be upgraded to https by server)
    validate_url("http://docs.aws.amazon.com/test")
