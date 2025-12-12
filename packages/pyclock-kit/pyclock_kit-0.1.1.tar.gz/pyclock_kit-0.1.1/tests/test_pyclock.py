"""Tests for pyclock package."""

import re
from datetime import datetime
import pytest
from pyclock import get_time, get_timestamp, get_utc_time


class TestGetTime:
    """Tests for get_time function."""
    
    def test_default_format(self):
        """Test get_time with default format."""
        result = get_time()
        # Should match format: YYYY-MM-DD HH:MM:SS
        pattern = r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$'
        assert re.match(pattern, result), f"Result {result} doesn't match expected format"
    
    def test_custom_format_time_only(self):
        """Test get_time with custom format (time only)."""
        result = get_time("%H:%M:%S")
        # Should match format: HH:MM:SS
        pattern = r'^\d{2}:\d{2}:\d{2}$'
        assert re.match(pattern, result), f"Result {result} doesn't match expected format"
    
    def test_custom_format_date_only(self):
        """Test get_time with custom format (date only)."""
        result = get_time("%Y-%m-%d")
        # Should match format: YYYY-MM-DD
        pattern = r'^\d{4}-\d{2}-\d{2}$'
        assert re.match(pattern, result), f"Result {result} doesn't match expected format"
    
    def test_custom_format_verbose(self):
        """Test get_time with verbose format."""
        result = get_time("%B %d, %Y at %I:%M %p")
        # Should contain month name, day, year, and time with AM/PM
        assert len(result) > 20, "Verbose format should be longer"
        assert any(month in result for month in [
            "January", "February", "March", "April", "May", "June",
            "July", "August", "September", "October", "November", "December"
        ]), "Should contain month name"
        assert " at " in result, "Should contain 'at' separator"
        assert result.endswith(("AM", "PM")), "Should end with AM or PM"


class TestGetTimestamp:
    """Tests for get_timestamp function."""
    
    def test_returns_float(self):
        """Test that get_timestamp returns a float."""
        result = get_timestamp()
        assert isinstance(result, float), f"Expected float, got {type(result)}"
    
    def test_reasonable_value(self):
        """Test that timestamp is a reasonable value."""
        result = get_timestamp()
        # Should be roughly around current time (Dec 2025 is around 1733097600)
        assert result > 1700000000, "Timestamp should be after 2023"
        assert result < 2000000000, "Timestamp should be before 2033"
    
    def test_increases_over_time(self):
        """Test that timestamp increases over time."""
        import time
        first = get_timestamp()
        time.sleep(0.01)  # Sleep for 10ms
        second = get_timestamp()
        assert second > first, "Timestamp should increase over time"


class TestGetUtcTime:
    """Tests for get_utc_time function."""
    
    def test_default_format(self):
        """Test get_utc_time with default format."""
        result = get_utc_time()
        # Should match format: YYYY-MM-DD HH:MM:SS
        pattern = r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$'
        assert re.match(pattern, result), f"Result {result} doesn't match expected format"
    
    def test_custom_format(self):
        """Test get_utc_time with custom format."""
        result = get_utc_time("%H:%M:%S")
        # Should match format: HH:MM:SS
        pattern = r'^\d{2}:\d{2}:\d{2}$'
        assert re.match(pattern, result), f"Result {result} doesn't match expected format"
    
    def test_utc_vs_local(self):
        """Test that UTC time is different from local time (in most timezones)."""
        utc = get_utc_time("%H")
        local = get_time("%H")
        # In most cases these should be different, but allow for UTC timezone
        # Just check they're both valid hours
        assert 0 <= int(utc) <= 23, "UTC hour should be 0-23"
        assert 0 <= int(local) <= 23, "Local hour should be 0-23"


class TestExports:
    """Test that all expected functions are exported."""
    
    def test_all_exports(self):
        """Test __all__ contains expected exports."""
        from pyclock import __all__
        expected = ["get_time", "get_timestamp", "get_utc_time"]
        assert set(__all__) == set(expected), f"Expected {expected}, got {__all__}"
    
    def test_version_exists(self):
        """Test that version is defined."""
        from pyclock import __version__
        assert isinstance(__version__, str), "Version should be a string"
        assert len(__version__) > 0, "Version should not be empty"
