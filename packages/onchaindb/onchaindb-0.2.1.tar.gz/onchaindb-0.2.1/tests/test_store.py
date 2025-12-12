"""Tests for store functionality."""

import pytest
from unittest.mock import Mock

from onchaindb import OnChainDBClient
from onchaindb.exceptions import StoreException, TaskTimeoutException


class TestStoreRoot:
    """Tests for store root field."""

    def test_store_includes_root(self):
        """Test that store includes root in correct format."""
        mock_http = Mock()
        mock_http.post.return_value = {"success": True}

        client = OnChainDBClient(
            endpoint="https://api.example.com",
            app_id="my-app",
            app_key="test-key",
            http_client=mock_http,
        )

        client.store(
            collection="users",
            data=[{"id": "user_1", "name": "Test"}],
            payment_proof={"payment_tx_hash": "abc123"},
        )

        # Verify root format
        call_args = mock_http.post.call_args
        request = call_args[0][1]
        assert request["root"] == "my-app::users"

    def test_store_includes_data(self):
        """Test that store includes data correctly."""
        mock_http = Mock()
        mock_http.post.return_value = {"success": True}

        client = OnChainDBClient(
            endpoint="https://api.example.com",
            app_id="test-app",
            app_key="test-key",
            http_client=mock_http,
        )

        data = [
            {"id": "user_1", "name": "Alice", "email": "alice@example.com"},
            {"id": "user_2", "name": "Bob", "email": "bob@example.com"},
        ]

        client.store(
            collection="users",
            data=data,
            payment_proof={"payment_tx_hash": "abc123"},
        )

        call_args = mock_http.post.call_args
        request = call_args[0][1]
        assert request["data"] == data

    def test_store_includes_payment_proof(self):
        """Test that store includes payment proof correctly."""
        mock_http = Mock()
        mock_http.post.return_value = {"success": True}

        client = OnChainDBClient(
            endpoint="https://api.example.com",
            app_id="test-app",
            app_key="test-key",
            http_client=mock_http,
        )

        payment_proof = {
            "payment_tx_hash": "abc123",
            "amount_utia": 10000,
            "sender": "celestia1abc...",
        }

        client.store(
            collection="users",
            data=[{"id": "user_1"}],
            payment_proof=payment_proof,
        )

        call_args = mock_http.post.call_args
        request = call_args[0][1]
        assert request["payment_tx_hash"] == "abc123"
        assert request["amount_utia"] == 10000
        assert request["sender"] == "celestia1abc..."


class TestStorePolling:
    """Tests for store polling behavior."""

    def test_store_polls_for_completion(self):
        """Test that store polls for completion when ticket_id returned."""
        mock_http = Mock()

        # First call returns ticket_id
        mock_http.post.return_value = {"ticket_id": "ticket-123"}

        # Simulate pending then completed
        mock_http.get.side_effect = [
            {"status": "Pending"},
            {"status": "Processing"},
            {"status": "Completed", "result": {"success": True, "celestia_height": 12345}},
        ]

        client = OnChainDBClient(
            endpoint="https://api.example.com",
            app_id="test-app",
            app_key="test-key",
            http_client=mock_http,
        )

        result = client.store(
            collection="users",
            data=[{"id": "user_1"}],
            payment_proof={"payment_tx_hash": "abc123"},
            poll_interval_ms=1,  # Fast polling for test
        )

        assert result["success"] is True
        assert result["celestia_height"] == 12345
        assert mock_http.get.call_count == 3

    def test_store_handles_task_failure_string(self):
        """Test that store handles failed task with string status."""
        mock_http = Mock()
        mock_http.post.return_value = {"ticket_id": "ticket-123"}
        mock_http.get.return_value = {"status": "Failed: Insufficient funds"}

        client = OnChainDBClient(
            endpoint="https://api.example.com",
            app_id="test-app",
            app_key="test-key",
            http_client=mock_http,
        )

        with pytest.raises(Exception) as exc_info:
            client.store(
                collection="users",
                data=[{"id": "user_1"}],
                payment_proof={"payment_tx_hash": "abc123"},
                poll_interval_ms=1,
            )

        assert "failed" in str(exc_info.value).lower()

    def test_store_handles_task_failure_object(self):
        """Test that store handles failed task with object status."""
        mock_http = Mock()
        mock_http.post.return_value = {"ticket_id": "ticket-123"}
        mock_http.get.return_value = {
            "status": {"Failed": {"error": "Invalid payment proof"}}
        }

        client = OnChainDBClient(
            endpoint="https://api.example.com",
            app_id="test-app",
            app_key="test-key",
            http_client=mock_http,
        )

        with pytest.raises(Exception) as exc_info:
            client.store(
                collection="users",
                data=[{"id": "user_1"}],
                payment_proof={"payment_tx_hash": "abc123"},
                poll_interval_ms=1,
            )

        assert "Invalid payment proof" in str(exc_info.value)

    def test_store_handles_timeout(self):
        """Test that store times out correctly."""
        mock_http = Mock()
        mock_http.post.return_value = {"ticket_id": "ticket-123"}
        mock_http.get.return_value = {"status": "Pending"}

        client = OnChainDBClient(
            endpoint="https://api.example.com",
            app_id="test-app",
            app_key="test-key",
            http_client=mock_http,
        )

        with pytest.raises(TaskTimeoutException) as exc_info:
            client.store(
                collection="users",
                data=[{"id": "user_1"}],
                payment_proof={"payment_tx_hash": "abc123"},
                poll_interval_ms=1,
                max_wait_time_ms=10,
            )

        assert "timed out" in str(exc_info.value)


class TestStoreWithoutWaiting:
    """Tests for store without waiting."""

    def test_store_returns_ticket_immediately(self):
        """Test that store returns ticket_id when not waiting."""
        mock_http = Mock()
        mock_http.post.return_value = {"ticket_id": "ticket-123"}

        client = OnChainDBClient(
            endpoint="https://api.example.com",
            app_id="test-app",
            app_key="test-key",
            http_client=mock_http,
        )

        result = client.store(
            collection="users",
            data=[{"id": "user_1"}],
            payment_proof={"payment_tx_hash": "abc123"},
            wait_for_confirmation=False,
        )

        assert result["ticket_id"] == "ticket-123"
        mock_http.get.assert_not_called()


class TestStoreCustomPollingSettings:
    """Tests for custom polling settings."""

    def test_store_custom_poll_interval(self):
        """Test that custom poll interval is used."""
        mock_http = Mock()
        mock_http.post.return_value = {"ticket_id": "ticket-123"}
        mock_http.get.return_value = {
            "status": "Completed",
            "result": {"success": True},
        }

        client = OnChainDBClient(
            endpoint="https://api.example.com",
            app_id="test-app",
            app_key="test-key",
            http_client=mock_http,
        )

        # This should work with custom settings
        result = client.store(
            collection="users",
            data=[{"id": "user_1"}],
            payment_proof={"payment_tx_hash": "abc123"},
            poll_interval_ms=1000,
            max_wait_time_ms=300000,
        )

        assert result["success"] is True


class TestStoreErrors:
    """Tests for store error handling."""

    def test_store_http_error(self):
        """Test that HTTP errors are wrapped properly."""
        mock_http = Mock()
        mock_http.post.side_effect = Exception("Network error")

        client = OnChainDBClient(
            endpoint="https://api.example.com",
            app_id="test-app",
            app_key="test-key",
            http_client=mock_http,
        )

        with pytest.raises(StoreException) as exc_info:
            client.store(
                collection="users",
                data=[{"id": "user_1"}],
                payment_proof={"payment_tx_hash": "abc123"},
            )

        assert "Store operation failed" in str(exc_info.value)
        assert "Network error" in str(exc_info.value)
