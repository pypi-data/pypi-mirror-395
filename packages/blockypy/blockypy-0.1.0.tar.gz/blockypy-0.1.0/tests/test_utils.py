"""Tests for shared utilities."""

import pytest
from blocky.utils import validate_decimal, parse_timeframe_ns
from blocky.exceptions import BlockyValidationError


class TestValidateDecimal:
    """Test decimal validation."""

    def test_valid_decimal(self):
        """Valid decimals are normalized."""
        assert validate_decimal("100.5") == "100.5"
        assert validate_decimal("0.123") == "0.123"

    def test_empty_decimal_raises(self):
        """Empty decimals raise."""
        with pytest.raises(BlockyValidationError, match="empty"):
            validate_decimal("")

    def test_none_decimal_raises(self):
        """None decimals raise."""
        with pytest.raises(BlockyValidationError, match="empty"):
            validate_decimal(None)

    def test_invalid_format_raises(self):
        """Invalid formats raise."""
        with pytest.raises(BlockyValidationError, match="Invalid decimal"):
            validate_decimal("abc")

    def test_out_of_range_raises(self):
        """Out of range values raise."""
        # Value with valid format (8 digits) but exceeds max range
        with pytest.raises(BlockyValidationError, match="must be between"):
            validate_decimal("99999999.1", max_value="99999999.0")


class TestParseTimeframeNs:
    """Test timeframe parsing."""

    def test_integer_passthrough(self):
        """Integer timeframes pass through."""
        assert parse_timeframe_ns(60_000_000_000) == 60_000_000_000

    def test_standard_timeframes(self):
        """Standard timeframe strings are parsed."""
        assert parse_timeframe_ns("1m") == 60_000_000_000
        assert parse_timeframe_ns("1H") == 3_600_000_000_000
        assert parse_timeframe_ns("1D") == 86_400_000_000_000

    def test_regex_fallback(self):
        """Non-standard timeframes use regex."""
        assert parse_timeframe_ns("10m") == 600_000_000_000
        assert parse_timeframe_ns("2h") == 7_200_000_000_000

    def test_invalid_timeframe_raises(self):
        """Invalid timeframes raise."""
        with pytest.raises(BlockyValidationError, match="Invalid timeframe"):
            parse_timeframe_ns("invalid")
