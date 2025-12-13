"""Basic tests for the MCP server."""

import pytest
from cv_resume_builder_mcp.server import parse_time_range
from datetime import datetime, timedelta


def test_parse_time_range():
    """Test time range parsing."""
    # Test various time ranges
    result = parse_time_range("6 months ago")
    assert isinstance(result, datetime)
    assert result < datetime.now()
    
    result = parse_time_range("1 year ago")
    assert isinstance(result, datetime)
    
    result = parse_time_range("30 days ago")
    assert isinstance(result, datetime)


def test_parse_time_range_default():
    """Test default time range."""
    result = parse_time_range("invalid")
    assert isinstance(result, datetime)
    # Should default to 6 months (180 days)
    expected = datetime.now() - timedelta(days=180)
    assert abs((result - expected).days) <= 1  # Allow 1 day difference
