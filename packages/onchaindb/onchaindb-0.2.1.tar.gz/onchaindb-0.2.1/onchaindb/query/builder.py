"""
Fluent query builder for constructing OnChainDB queries.

The main interface for building and executing queries against OnChainDB.
"""

from typing import Any, Dict, List, Optional, Callable, Union
import copy

from .where_clause import WhereClause
from .condition_builder import ConditionBuilder
from .selection_builder import SelectionBuilder
from .join_builder import JoinBuilder
from .group_by_builder import GroupByQueryBuilder
from .logical_operator import LogicalOperator
from ..exceptions import QueryException


class QueryBuilder:
    """
    Fluent query builder for OnChainDB.

    Provides a chainable API for constructing queries with filtering,
    selection, sorting, pagination, JOINs, and aggregations.

    Example:
        results = (client.query_builder()
            .collection("users")
            .where_field("status").equals("active")
            .where_field("age").greater_than(18)
            .select_all()
            .limit(10)
            .offset(0)
            .order_by("created_at", "desc")
            .execute())
    """

    def __init__(
        self,
        http_client: Any,
        endpoint: str,
        app_id: str,
    ):
        """
        Initialize a query builder.

        Args:
            http_client: The HTTP client for making requests.
            endpoint: The OnChainDB API endpoint.
            app_id: The application ID.
        """
        self._http_client = http_client
        self._endpoint = endpoint
        self._app_id = app_id
        self._collection_name: Optional[str] = None
        self._find_conditions: Optional[Dict[str, Any]] = None
        self._selections: Optional[Dict[str, Any]] = None
        self._limit_value: Optional[int] = None
        self._offset_value: Optional[int] = None
        self._sort_by: Optional[str] = None
        self._sort_direction: Optional[str] = None
        self._include_history_value: Optional[bool] = None
        self._server_join_configs: List[Dict[str, Any]] = []

    def collection(self, name: str) -> "QueryBuilder":
        """
        Set the target collection.

        Args:
            name: The name of the collection to query.

        Returns:
            Self for method chaining.
        """
        self._collection_name = name
        return self

    def where_field(self, field_name: str) -> WhereClause:
        """
        Add a where field condition.

        Args:
            field_name: The name of the field to filter on.

        Returns:
            A WhereClause for specifying the condition.
        """
        return WhereClause(self, field_name)

    def find(
        self,
        builder_fn: Callable[[ConditionBuilder], Union[Dict[str, Any], LogicalOperator]],
    ) -> "QueryBuilder":
        """
        Set complex find conditions using a builder function.

        Args:
            builder_fn: A function that builds conditions using ConditionBuilder.

        Returns:
            Self for method chaining.

        Example:
            .find(lambda c: c.and_group(lambda: [
                c.field("status").equals("active"),
                c.or_group(lambda: [
                    c.field("role").equals("admin"),
                    c.field("role").equals("moderator"),
                ]),
            ]))
        """
        builder = ConditionBuilder()
        result = builder_fn(builder)
        if isinstance(result, LogicalOperator):
            self._find_conditions = result.to_dict()
        else:
            self._find_conditions = result
        return self

    def select_fields(self, fields: List[str]) -> "QueryBuilder":
        """
        Select specific fields to return.

        Args:
            fields: List of field names to include.

        Returns:
            Self for method chaining.
        """
        self._selections = {}
        for field in fields:
            self._selections[field] = True
        return self

    def select_all(self) -> "QueryBuilder":
        """
        Select all fields (default behavior).

        Returns:
            Self for method chaining.
        """
        self._selections = {}
        return self

    def select(
        self,
        builder_fn: Callable[[SelectionBuilder], SelectionBuilder],
    ) -> "QueryBuilder":
        """
        Configure selection with a builder function.

        Args:
            builder_fn: A function that configures the selection.

        Returns:
            Self for method chaining.
        """
        builder = SelectionBuilder()
        builder_fn(builder)
        self._selections = builder.build()
        return self

    def limit(self, n: int) -> "QueryBuilder":
        """
        Limit the number of results.

        Args:
            n: Maximum number of results to return.

        Returns:
            Self for method chaining.
        """
        self._limit_value = n
        return self

    def offset(self, n: int) -> "QueryBuilder":
        """
        Skip a number of results (for pagination).

        Args:
            n: Number of results to skip.

        Returns:
            Self for method chaining.
        """
        self._offset_value = n
        return self

    def order_by(self, field: str, direction: str = "asc") -> "QueryBuilder":
        """
        Sort results by a field.

        Args:
            field: The field to sort by.
            direction: Sort direction ('asc' or 'desc').

        Returns:
            Self for method chaining.
        """
        self._sort_by = field
        self._sort_direction = direction
        return self

    def include_history(self, include: bool = True) -> "QueryBuilder":
        """
        Include historical versions of records.

        Args:
            include: Whether to include history.

        Returns:
            Self for method chaining.
        """
        self._include_history_value = include
        return self

    def join_one(self, alias: str, model: str) -> JoinBuilder:
        """
        Add a one-to-one JOIN.

        Args:
            alias: The alias for the joined data in results.
            model: The name of the collection to join.

        Returns:
            A JoinBuilder for configuring the join.
        """
        return JoinBuilder(self, alias, model, False)

    def join_many(self, alias: str, model: str) -> JoinBuilder:
        """
        Add a one-to-many JOIN.

        Args:
            alias: The alias for the joined data in results.
            model: The name of the collection to join.

        Returns:
            A JoinBuilder for configuring the join.
        """
        return JoinBuilder(self, alias, model, True)

    def join_with(self, alias: str, model: str) -> JoinBuilder:
        """
        Add a JOIN with default behavior (returns array).

        Args:
            alias: The alias for the joined data in results.
            model: The name of the collection to join.

        Returns:
            A JoinBuilder for configuring the join.
        """
        return JoinBuilder(self, alias, model, None)

    def group_by(self, field: str) -> GroupByQueryBuilder:
        """
        Start a grouped aggregation.

        Args:
            field: The field to group by.

        Returns:
            A GroupByQueryBuilder for performing aggregations.
        """
        return GroupByQueryBuilder(self, field)

    def _set_find_conditions(self, conditions: Dict[str, Any]) -> None:
        """Internal: Set find conditions from WhereClause."""
        self._find_conditions = conditions

    def _add_server_join(self, config: Dict[str, Any]) -> None:
        """Internal: Add a server join configuration."""
        self._server_join_configs.append(config)

    def _build_query_value(self) -> Dict[str, Any]:
        """Build the query value object."""
        find = dict(self._find_conditions) if self._find_conditions else {}
        select = dict(self._selections) if self._selections else {}

        # Add server-side JOINs to the find conditions
        for join in self._server_join_configs:
            join_config: Dict[str, Any] = {
                "resolve": join["resolve"],
                "model": join["model"],
            }

            if "many" in join:
                join_config["many"] = join["many"]

            find[join["alias"]] = join_config

        # Cast to empty object to ensure JSON encodes as {} not []
        query_value: Dict[str, Any] = {
            "find": find if find else {},
            "select": select if select else {},
        }

        if self._include_history_value is not None:
            query_value["include_history"] = self._include_history_value

        return query_value

    def get_query_request(self) -> Dict[str, Any]:
        """
        Get the raw query request object (for debugging).

        Returns:
            Dictionary representing the full query request.
        """
        query_value = self._build_query_value()

        request = {
            **query_value,
            "root": f"{self._app_id}::{self._collection_name}",
        }

        if self._limit_value is not None:
            request["limit"] = self._limit_value

        if self._offset_value is not None:
            request["offset"] = self._offset_value

        if self._sort_by is not None:
            request["sortBy"] = self._sort_by

        return request

    def build_raw_query(self) -> Dict[str, Any]:
        """
        Build raw query for debugging (alias for get_query_request).

        Returns:
            Dictionary representing the full query request.
        """
        return self.get_query_request()

    def execute(self) -> Dict[str, Any]:
        """
        Execute the query and return results.

        Returns:
            Dictionary containing the query results.

        Raises:
            QueryException: If the query execution fails.
        """
        if self._http_client is None:
            raise QueryException("HTTP client is required for query execution")

        if self._endpoint is None:
            raise QueryException("Server URL is required for query execution")

        request = self.get_query_request()

        try:
            url = f"{self._endpoint}/list"
            response = self._http_client.post(url, request)
            return response
        except Exception as e:
            raise QueryException(f"Query execution failed: {str(e)}") from e

    def execute_unique(self) -> Optional[Dict[str, Any]]:
        """
        Execute the query and return the most recent record.

        This method retrieves records and sorts them by metadata
        timestamp (updatedAt or createdAt) to return the latest one.

        Returns:
            The most recent matching record, or None if no matches.
        """
        response = self.execute()
        records = response.get("records", [])

        if not records:
            return None

        # Sort by metadata timestamp (updatedAt first, then createdAt) descending
        def get_timestamp(record: Dict[str, Any]) -> str:
            return (
                record.get("updatedAt")
                or record.get("updated_at")
                or record.get("createdAt")
                or record.get("created_at")
                or ""
            )

        sorted_records = sorted(records, key=get_timestamp, reverse=True)
        return sorted_records[0]

    # ===== AGGREGATION METHODS =====

    def count(self) -> int:
        """
        Count matching records.

        Returns:
            The number of matching records.
        """
        response = self.execute()
        return len(response.get("records", []))

    def sum_by(self, field: str) -> float:
        """
        Sum values of a numeric field.

        Args:
            field: The field to sum.

        Returns:
            The sum of values.
        """
        response = self.execute()
        records = response.get("records", [])

        total = 0.0
        for record in records:
            value = record.get(field, 0)
            if isinstance(value, (int, float)):
                total += float(value)

        return total

    def avg_by(self, field: str) -> float:
        """
        Calculate average of a numeric field.

        Args:
            field: The field to average.

        Returns:
            The average value.
        """
        response = self.execute()
        records = response.get("records", [])

        if not records:
            return 0.0

        total = self.sum_by(field)
        return total / len(records)

    def max_by(self, field: str) -> Any:
        """
        Find maximum value of a field.

        Args:
            field: The field to find maximum of.

        Returns:
            The maximum value, or None if no records.
        """
        response = self.execute()
        records = response.get("records", [])

        if not records:
            return None

        max_val = None
        for record in records:
            value = record.get(field)
            if max_val is None or (value is not None and value > max_val):
                max_val = value

        return max_val

    def min_by(self, field: str) -> Any:
        """
        Find minimum value of a field.

        Args:
            field: The field to find minimum of.

        Returns:
            The minimum value, or None if no records.
        """
        response = self.execute()
        records = response.get("records", [])

        if not records:
            return None

        min_val = None
        for record in records:
            value = record.get(field)
            if min_val is None or (value is not None and value < min_val):
                min_val = value

        return min_val

    def distinct_by(self, field: str) -> List[Any]:
        """
        Get distinct values of a field.

        Args:
            field: The field to get distinct values from.

        Returns:
            List of distinct values.
        """
        response = self.execute()
        records = response.get("records", [])

        unique: List[Any] = []
        for record in records:
            value = record.get(field)
            if value is not None and value not in unique:
                unique.append(value)

        return unique

    def count_distinct(self, field: str) -> int:
        """
        Count distinct values of a field.

        Args:
            field: The field to count distinct values from.

        Returns:
            The number of distinct values.
        """
        return len(self.distinct_by(field))

    def is_valid(self) -> bool:
        """
        Check if the query is valid.

        Returns:
            True if the query has conditions or selections.
        """
        return self._find_conditions is not None or self._selections is not None

    def clone(self) -> "QueryBuilder":
        """
        Clone the query builder.

        Returns:
            A deep copy of this QueryBuilder.
        """
        return copy.deepcopy(self)
