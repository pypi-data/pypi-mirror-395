"""Tests for the Blocky sync client."""

import pytest
from blocky import Blocky
from blocky.exceptions import BlockyAuthenticationError, BlockyValidationError


class TestBlockyClient:
    """Test cases for the synchronous Blocky client."""

    def test_init_without_api_key(self):
        """Client can be initialized without an API key for public endpoints."""
        client = Blocky()
        assert client.authenticated is False
        assert client.api_key is None

    def test_init_with_api_key(self):
        """Client can be initialized with an API key."""
        client = Blocky(api_key="test-key")
        assert client.authenticated is True
        assert client.api_key == "test-key"

    def test_custom_endpoint(self):
        """Client accepts custom endpoint."""
        client = Blocky(endpoint="https://custom.example.com/api/v1/")
        assert client.endpoint == "https://custom.example.com/api/v1"

    def test_require_auth_raises(self):
        """Private endpoints raise when not authenticated."""
        client = Blocky()
        with pytest.raises(BlockyAuthenticationError):
            client.get_wallets()

    def test_create_order_validation_side(self):
        """Order validation checks side parameter."""
        client = Blocky(api_key="test-key")
        with pytest.raises(BlockyValidationError, match="Side must be"):
            client.create_order(
                type_="limit",
                market="xno_xbrl",
                side="invalid",
                price="100",
                quantity="1"
            )

    def test_create_order_validation_type(self):
        """Order validation checks type parameter."""
        client = Blocky(api_key="test-key")
        with pytest.raises(BlockyValidationError, match="Type must be"):
            client.create_order(
                type_="invalid",
                market="xno_xbrl",
                side="buy",
                price="100",
                quantity="1"
            )

    def test_create_transfer_same_wallet(self):
        """Transfer validation rejects same source/destination."""
        client = Blocky(api_key="test-key")
        with pytest.raises(BlockyValidationError, match="cannot be the same"):
            client.create_transfer(
                instrument="xbrl",
                quantity="100",
                source_sub_wallet_id=0,
                destination_sub_wallet_id=0
            )

    def test_create_transfer_invalid_wallet_id(self):
        """Transfer validation rejects invalid wallet IDs."""
        client = Blocky(api_key="test-key")
        with pytest.raises(BlockyValidationError, match="cannot exceed"):
            client.create_transfer(
                instrument="xbrl",
                quantity="100",
                source_sub_wallet_id=0,
                destination_sub_wallet_id=99999
            )
