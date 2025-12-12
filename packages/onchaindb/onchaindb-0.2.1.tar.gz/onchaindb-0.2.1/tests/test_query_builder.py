"""Tests for QueryBuilder."""

import pytest
from unittest.mock import Mock

from onchaindb import QueryBuilder
from onchaindb.exceptions import QueryException


class TestQueryBuilderBasics:
    """Tests for basic query builder functionality."""

    def test_collection(self):
        """Test setting collection."""
        mock_http = Mock()
        builder = QueryBuilder(mock_http, "https://api.example.com", "test-app")

        result = builder.collection("users")

        assert result is builder  # Method chaining
        assert builder._collection_name == "users"

    def test_limit_and_offset(self):
        """Test limit and offset."""
        mock_http = Mock()
        builder = QueryBuilder(mock_http, "https://api.example.com", "test-app")

        builder.collection("users").limit(10).offset(5)

        request = builder.get_query_request()
        assert request["limit"] == 10
        assert request["offset"] == 5

    def test_order_by(self):
        """Test order by."""
        mock_http = Mock()
        builder = QueryBuilder(mock_http, "https://api.example.com", "test-app")

        builder.collection("users").order_by("created_at", "desc")

        request = builder.get_query_request()
        assert request["sortBy"] == "created_at"

    def test_include_history(self):
        """Test include history flag."""
        mock_http = Mock()
        builder = QueryBuilder(mock_http, "https://api.example.com", "test-app")

        builder.collection("users").include_history(True)

        request = builder.get_query_request()
        assert request["include_history"] is True


class TestRootFormat:
    """Tests for root field format."""

    def test_root_format(self):
        """Test that root is correctly formatted as app_id::collection."""
        mock_http = Mock()
        builder = QueryBuilder(mock_http, "https://api.example.com", "my-app")

        builder.collection("users")

        request = builder.get_query_request()
        assert request["root"] == "my-app::users"


class TestWhereField:
    """Tests for where_field conditions."""

    def test_equals(self):
        """Test equals operator."""
        mock_http = Mock()
        mock_http.post.return_value = {"records": []}

        builder = QueryBuilder(mock_http, "https://api.example.com", "test-app")
        builder.collection("users").where_field("status").equals("active")

        request = builder.get_query_request()
        assert request["find"]["status"]["is"] == "active"

    def test_not_equals(self):
        """Test not equals operator."""
        mock_http = Mock()
        builder = QueryBuilder(mock_http, "https://api.example.com", "test-app")

        builder.collection("users").where_field("status").not_equals("deleted")

        request = builder.get_query_request()
        assert request["find"]["status"]["isNot"] == "deleted"

    def test_greater_than(self):
        """Test greater than operator."""
        mock_http = Mock()
        builder = QueryBuilder(mock_http, "https://api.example.com", "test-app")

        builder.collection("users").where_field("age").greater_than(18)

        request = builder.get_query_request()
        assert request["find"]["age"]["greaterThan"] == 18

    def test_less_than(self):
        """Test less than operator."""
        mock_http = Mock()
        builder = QueryBuilder(mock_http, "https://api.example.com", "test-app")

        builder.collection("users").where_field("age").less_than(65)

        request = builder.get_query_request()
        assert request["find"]["age"]["lessThan"] == 65

    def test_between(self):
        """Test between operator."""
        mock_http = Mock()
        builder = QueryBuilder(mock_http, "https://api.example.com", "test-app")

        builder.collection("users").where_field("age").between(18, 65)

        request = builder.get_query_request()
        assert request["find"]["age"]["betweenOp"]["from"] == 18
        assert request["find"]["age"]["betweenOp"]["to"] == 65

    def test_contains(self):
        """Test contains (includes) operator."""
        mock_http = Mock()
        builder = QueryBuilder(mock_http, "https://api.example.com", "test-app")

        builder.collection("users").where_field("email").contains("@example")

        request = builder.get_query_request()
        assert request["find"]["email"]["includes"] == "@example"

    def test_starts_with(self):
        """Test starts with operator."""
        mock_http = Mock()
        builder = QueryBuilder(mock_http, "https://api.example.com", "test-app")

        builder.collection("users").where_field("name").starts_with("John")

        request = builder.get_query_request()
        assert request["find"]["name"]["startsWith"] == "John"

    def test_ends_with(self):
        """Test ends with operator."""
        mock_http = Mock()
        builder = QueryBuilder(mock_http, "https://api.example.com", "test-app")

        builder.collection("users").where_field("email").ends_with(".com")

        request = builder.get_query_request()
        assert request["find"]["email"]["endsWith"] == ".com"

    def test_is_in(self):
        """Test is_in operator."""
        mock_http = Mock()
        builder = QueryBuilder(mock_http, "https://api.example.com", "test-app")

        builder.collection("users").where_field("role").is_in(["admin", "moderator"])

        request = builder.get_query_request()
        assert request["find"]["role"]["in"] == ["admin", "moderator"]

    def test_not_in(self):
        """Test not_in operator."""
        mock_http = Mock()
        builder = QueryBuilder(mock_http, "https://api.example.com", "test-app")

        builder.collection("users").where_field("status").not_in(["deleted", "banned"])

        request = builder.get_query_request()
        assert request["find"]["status"]["notIn"] == ["deleted", "banned"]

    def test_is_null(self):
        """Test is_null operator."""
        mock_http = Mock()
        builder = QueryBuilder(mock_http, "https://api.example.com", "test-app")

        builder.collection("users").where_field("deleted_at").is_null()

        request = builder.get_query_request()
        assert request["find"]["deleted_at"]["isNull"] is True

    def test_is_not_null(self):
        """Test is_not_null operator."""
        mock_http = Mock()
        builder = QueryBuilder(mock_http, "https://api.example.com", "test-app")

        builder.collection("users").where_field("email").is_not_null()

        request = builder.get_query_request()
        assert request["find"]["email"]["isNull"] is False

    def test_is_true(self):
        """Test is_true operator."""
        mock_http = Mock()
        builder = QueryBuilder(mock_http, "https://api.example.com", "test-app")

        builder.collection("users").where_field("is_active").is_true()

        request = builder.get_query_request()
        assert request["find"]["is_active"]["is"] is True

    def test_is_false(self):
        """Test is_false operator."""
        mock_http = Mock()
        builder = QueryBuilder(mock_http, "https://api.example.com", "test-app")

        builder.collection("users").where_field("is_deleted").is_false()

        request = builder.get_query_request()
        assert request["find"]["is_deleted"]["is"] is False


class TestNestedFields:
    """Tests for nested field queries (dot notation)."""

    def test_nested_field_equals(self):
        """Test nested field with equals."""
        mock_http = Mock()
        builder = QueryBuilder(mock_http, "https://api.example.com", "test-app")

        builder.collection("users").where_field("address.city").equals("New York")

        request = builder.get_query_request()
        assert request["find"]["address"]["city"]["is"] == "New York"


class TestSelectFields:
    """Tests for field selection."""

    def test_select_fields(self):
        """Test selecting specific fields."""
        mock_http = Mock()
        builder = QueryBuilder(mock_http, "https://api.example.com", "test-app")

        builder.collection("users").select_fields(["id", "name", "email"])

        request = builder.get_query_request()
        assert request["select"]["id"] is True
        assert request["select"]["name"] is True
        assert request["select"]["email"] is True

    def test_select_all(self):
        """Test selecting all fields (empty select)."""
        mock_http = Mock()
        builder = QueryBuilder(mock_http, "https://api.example.com", "test-app")

        builder.collection("users").select_all()

        request = builder.get_query_request()
        assert request["select"] == {}


class TestAggregations:
    """Tests for aggregation methods."""

    def test_count(self):
        """Test count aggregation."""
        mock_http = Mock()
        mock_http.post.return_value = {
            "records": [{"id": "1"}, {"id": "2"}, {"id": "3"}]
        }

        builder = QueryBuilder(mock_http, "https://api.example.com", "test-app")
        count = builder.collection("users").count()

        assert count == 3

    def test_sum_by(self):
        """Test sum aggregation."""
        mock_http = Mock()
        mock_http.post.return_value = {
            "records": [
                {"amount": 100},
                {"amount": 200},
                {"amount": 300},
            ]
        }

        builder = QueryBuilder(mock_http, "https://api.example.com", "test-app")
        total = builder.collection("orders").sum_by("amount")

        assert total == 600.0

    def test_avg_by(self):
        """Test average aggregation."""
        mock_http = Mock()
        mock_http.post.return_value = {
            "records": [
                {"amount": 100},
                {"amount": 200},
                {"amount": 300},
            ]
        }

        builder = QueryBuilder(mock_http, "https://api.example.com", "test-app")
        avg = builder.collection("orders").avg_by("amount")

        assert avg == 200.0

    def test_max_by(self):
        """Test max aggregation."""
        mock_http = Mock()
        mock_http.post.return_value = {
            "records": [
                {"amount": 100},
                {"amount": 300},
                {"amount": 200},
            ]
        }

        builder = QueryBuilder(mock_http, "https://api.example.com", "test-app")
        max_val = builder.collection("orders").max_by("amount")

        assert max_val == 300

    def test_min_by(self):
        """Test min aggregation."""
        mock_http = Mock()
        mock_http.post.return_value = {
            "records": [
                {"amount": 100},
                {"amount": 300},
                {"amount": 200},
            ]
        }

        builder = QueryBuilder(mock_http, "https://api.example.com", "test-app")
        min_val = builder.collection("orders").min_by("amount")

        assert min_val == 100

    def test_distinct_by(self):
        """Test distinct aggregation."""
        mock_http = Mock()
        mock_http.post.return_value = {
            "records": [
                {"status": "active"},
                {"status": "pending"},
                {"status": "active"},
                {"status": "completed"},
            ]
        }

        builder = QueryBuilder(mock_http, "https://api.example.com", "test-app")
        distinct = builder.collection("orders").distinct_by("status")

        assert len(distinct) == 3
        assert "active" in distinct
        assert "pending" in distinct
        assert "completed" in distinct

    def test_count_distinct(self):
        """Test count distinct aggregation."""
        mock_http = Mock()
        mock_http.post.return_value = {
            "records": [
                {"status": "active"},
                {"status": "pending"},
                {"status": "active"},
                {"status": "completed"},
            ]
        }

        builder = QueryBuilder(mock_http, "https://api.example.com", "test-app")
        count = builder.collection("orders").count_distinct("status")

        assert count == 3


class TestClone:
    """Tests for query builder cloning."""

    def test_clone(self):
        """Test that clone creates a deep copy."""
        mock_http = Mock()
        builder = QueryBuilder(mock_http, "https://api.example.com", "test-app")

        builder.collection("users").where_field("status").equals("active").limit(10)

        cloned = builder.clone()

        # Modify the original
        builder.limit(20)

        # Clone should not be affected
        assert cloned._limit_value == 10


class TestExecuteUnique:
    """Tests for execute_unique method."""

    def test_execute_unique_returns_latest(self):
        """Test that execute_unique returns the most recent record."""
        mock_http = Mock()
        mock_http.post.return_value = {
            "records": [
                {"id": "1", "updatedAt": "2024-01-01T00:00:00Z"},
                {"id": "2", "updatedAt": "2024-01-15T00:00:00Z"},
                {"id": "3", "updatedAt": "2024-01-10T00:00:00Z"},
            ]
        }

        builder = QueryBuilder(mock_http, "https://api.example.com", "test-app")
        result = builder.collection("users").execute_unique()

        assert result["id"] == "2"  # Most recent by updatedAt

    def test_execute_unique_empty_results(self):
        """Test that execute_unique returns None for empty results."""
        mock_http = Mock()
        mock_http.post.return_value = {"records": []}

        builder = QueryBuilder(mock_http, "https://api.example.com", "test-app")
        result = builder.collection("users").execute_unique()

        assert result is None


class TestErrors:
    """Tests for error handling."""

    def test_execute_without_http_client(self):
        """Test that execute raises error without HTTP client."""
        builder = QueryBuilder(None, "https://api.example.com", "test-app")
        builder.collection("users")

        with pytest.raises(QueryException) as exc_info:
            builder.execute()

        assert "HTTP client is required" in str(exc_info.value)

    def test_execute_without_endpoint(self):
        """Test that execute raises error without endpoint."""
        mock_http = Mock()
        builder = QueryBuilder(mock_http, None, "test-app")
        builder.collection("users")

        with pytest.raises(QueryException) as exc_info:
            builder.execute()

        assert "Server URL is required" in str(exc_info.value)
