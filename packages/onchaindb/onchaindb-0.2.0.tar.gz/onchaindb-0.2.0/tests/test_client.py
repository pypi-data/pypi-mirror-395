"""Tests for OnChainDBClient."""

import pytest
from unittest.mock import Mock, patch, MagicMock
import time

from onchaindb import OnChainDBClient
from onchaindb.exceptions import (
    OnChainDBException,
    StoreException,
    TaskTimeoutException,
)


class TestClientInitialization:
    """Tests for client initialization."""

    def test_client_initialization(self):
        """Test basic client initialization."""
        client = OnChainDBClient(
            endpoint="https://api.example.com",
            app_id="test-app",
            app_key="test-key",
        )

        assert client.endpoint == "https://api.example.com"
        assert client.app_id == "test-app"
        assert client.app_key == "test-key"
        assert client.user_key is None

    def test_client_initialization_with_user_key(self):
        """Test client initialization with user key."""
        client = OnChainDBClient(
            endpoint="https://api.example.com",
            app_id="test-app",
            app_key="test-key",
            user_key="test-user-key",
        )

        assert client.user_key == "test-user-key"

    def test_client_strips_trailing_slash(self):
        """Test that trailing slash is stripped from endpoint."""
        client = OnChainDBClient(
            endpoint="https://api.example.com/",
            app_id="test-app",
            app_key="test-key",
        )

        assert client.endpoint == "https://api.example.com"

    def test_client_with_custom_http_client(self):
        """Test client with custom HTTP client."""
        mock_http = Mock()
        client = OnChainDBClient(
            endpoint="https://api.example.com",
            app_id="test-app",
            app_key="test-key",
            http_client=mock_http,
        )

        # Verify the custom client is used
        assert client._http_client is mock_http


class TestFindUnique:
    """Tests for find_unique method."""

    def test_find_unique_success(self):
        """Test successful find_unique."""
        mock_http = Mock()
        mock_http.post.return_value = {
            "records": [
                {"id": "user_1", "email": "test@example.com", "name": "Test User"}
            ]
        }

        client = OnChainDBClient(
            endpoint="https://api.example.com",
            app_id="test-app",
            app_key="test-key",
            http_client=mock_http,
        )

        result = client.find_unique("users", {"email": "test@example.com"})

        assert result is not None
        assert result["id"] == "user_1"
        assert result["email"] == "test@example.com"

        # Verify the request was made correctly
        mock_http.post.assert_called_once()
        call_args = mock_http.post.call_args
        assert call_args[0][0] == "https://api.example.com/list"
        assert "root" in call_args[0][1]
        assert call_args[0][1]["root"] == "test-app::users"

    def test_find_unique_not_found(self):
        """Test find_unique returns None when no records found."""
        mock_http = Mock()
        mock_http.post.return_value = {"records": []}

        client = OnChainDBClient(
            endpoint="https://api.example.com",
            app_id="test-app",
            app_key="test-key",
            http_client=mock_http,
        )

        result = client.find_unique("users", {"email": "nonexistent@example.com"})

        assert result is None


class TestFindMany:
    """Tests for find_many method."""

    def test_find_many_success(self):
        """Test successful find_many."""
        mock_http = Mock()
        mock_http.post.return_value = {
            "records": [
                {"id": "user_1", "status": "active"},
                {"id": "user_2", "status": "active"},
            ]
        }

        client = OnChainDBClient(
            endpoint="https://api.example.com",
            app_id="test-app",
            app_key="test-key",
            http_client=mock_http,
        )

        results = client.find_many("users", {"status": "active"})

        assert len(results) == 2
        assert results[0]["id"] == "user_1"
        assert results[1]["id"] == "user_2"

    def test_find_many_with_limit_and_offset(self):
        """Test find_many with limit and offset."""
        mock_http = Mock()
        mock_http.post.return_value = {"records": [{"id": "user_1"}]}

        client = OnChainDBClient(
            endpoint="https://api.example.com",
            app_id="test-app",
            app_key="test-key",
            http_client=mock_http,
        )

        client.find_many("users", limit=10, offset=5)

        call_args = mock_http.post.call_args
        request = call_args[0][1]
        assert request["limit"] == 10
        assert request["offset"] == 5

    def test_find_many_empty_results(self):
        """Test find_many returns empty list when no records found."""
        mock_http = Mock()
        mock_http.post.return_value = {"records": []}

        client = OnChainDBClient(
            endpoint="https://api.example.com",
            app_id="test-app",
            app_key="test-key",
            http_client=mock_http,
        )

        results = client.find_many("users", {"status": "nonexistent"})

        assert results == []


class TestCountDocuments:
    """Tests for count_documents method."""

    def test_count_documents(self):
        """Test count_documents returns correct count."""
        mock_http = Mock()
        mock_http.post.return_value = {
            "records": [{"id": "1"}, {"id": "2"}, {"id": "3"}]
        }

        client = OnChainDBClient(
            endpoint="https://api.example.com",
            app_id="test-app",
            app_key="test-key",
            http_client=mock_http,
        )

        count = client.count_documents("users", {"status": "active"})

        assert count == 3


class TestStore:
    """Tests for store method."""

    def test_store_with_immediate_response(self):
        """Test store with immediate (non-async) response."""
        mock_http = Mock()
        mock_http.post.return_value = {
            "success": True,
            "celestia_height": 12345,
        }

        client = OnChainDBClient(
            endpoint="https://api.example.com",
            app_id="test-app",
            app_key="test-key",
            http_client=mock_http,
        )

        result = client.store(
            collection="users",
            data=[{"id": "user_1", "name": "Test"}],
            payment_proof={"payment_tx_hash": "abc123", "amount_utia": 10000},
        )

        assert result["success"] is True
        assert result["celestia_height"] == 12345

        # Verify correct request
        call_args = mock_http.post.call_args
        assert call_args[0][0] == "https://api.example.com/store"
        request = call_args[0][1]
        assert request["root"] == "test-app::users"
        assert request["data"] == [{"id": "user_1", "name": "Test"}]
        assert request["payment_tx_hash"] == "abc123"
        assert request["amount_utia"] == 10000

    def test_store_with_async_response_and_polling(self):
        """Test store with async response that requires polling."""
        mock_http = Mock()

        # First call returns ticket_id
        # Second call (get) returns completed status
        mock_http.post.return_value = {"ticket_id": "ticket-123"}
        mock_http.get.return_value = {
            "status": "Completed",
            "result": {"success": True, "celestia_height": 12345},
        }

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
            poll_interval_ms=10,  # Short interval for testing
        )

        assert result["success"] is True
        assert result["celestia_height"] == 12345

        # Verify task status was checked
        mock_http.get.assert_called_with(
            "https://api.example.com/task/ticket-123"
        )

    def test_store_without_waiting(self):
        """Test store without waiting for confirmation."""
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


class TestTaskPolling:
    """Tests for task polling functionality."""

    def test_wait_for_task_completion_success(self):
        """Test successful task completion polling."""
        mock_http = Mock()
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

        result = client.wait_for_task_completion("ticket-123")

        assert result["status"] == "Completed"
        assert result["result"]["success"] is True

    def test_wait_for_task_completion_failed_string(self):
        """Test task failure with string status."""
        mock_http = Mock()
        mock_http.get.return_value = {"status": "Failed: Something went wrong"}

        client = OnChainDBClient(
            endpoint="https://api.example.com",
            app_id="test-app",
            app_key="test-key",
            http_client=mock_http,
        )

        with pytest.raises(OnChainDBException) as exc_info:
            client.wait_for_task_completion("ticket-123", poll_interval_ms=10)

        assert "Task failed" in str(exc_info.value)

    def test_wait_for_task_completion_failed_object(self):
        """Test task failure with object status."""
        mock_http = Mock()
        mock_http.get.return_value = {
            "status": {"Failed": {"error": "Insufficient funds"}}
        }

        client = OnChainDBClient(
            endpoint="https://api.example.com",
            app_id="test-app",
            app_key="test-key",
            http_client=mock_http,
        )

        with pytest.raises(OnChainDBException) as exc_info:
            client.wait_for_task_completion("ticket-123", poll_interval_ms=10)

        assert "Insufficient funds" in str(exc_info.value)

    def test_wait_for_task_completion_timeout(self):
        """Test task timeout."""
        mock_http = Mock()
        mock_http.get.return_value = {"status": "Pending"}

        client = OnChainDBClient(
            endpoint="https://api.example.com",
            app_id="test-app",
            app_key="test-key",
            http_client=mock_http,
        )

        with pytest.raises(TaskTimeoutException) as exc_info:
            client.wait_for_task_completion(
                "ticket-123",
                poll_interval_ms=10,
                max_wait_time_ms=50,
            )

        assert "timed out" in str(exc_info.value)


class TestQueryBuilder:
    """Tests for query_builder method."""

    def test_query_builder_returns_builder(self):
        """Test that query_builder returns a QueryBuilder instance."""
        mock_http = Mock()
        client = OnChainDBClient(
            endpoint="https://api.example.com",
            app_id="test-app",
            app_key="test-key",
            http_client=mock_http,
        )

        builder = client.query_builder()

        from onchaindb import QueryBuilder
        assert isinstance(builder, QueryBuilder)

    def test_query_builder_fluent_api(self):
        """Test the fluent API of query builder."""
        mock_http = Mock()
        mock_http.post.return_value = {"records": [{"id": "user_1"}]}

        client = OnChainDBClient(
            endpoint="https://api.example.com",
            app_id="test-app",
            app_key="test-key",
            http_client=mock_http,
        )

        result = (
            client.query_builder()
            .collection("users")
            .where_field("status").equals("active")
            .where_field("age").greater_than(18)
            .select_all()
            .limit(10)
            .offset(5)
            .order_by("created_at", "desc")
            .execute()
        )

        assert result["records"][0]["id"] == "user_1"

        # Verify request structure
        call_args = mock_http.post.call_args
        request = call_args[0][1]
        assert request["root"] == "test-app::users"
        assert request["limit"] == 10
        assert request["offset"] == 5
