"""
Group by query builder for aggregations.

Provides grouped aggregation queries like count by status,
sum by category, etc.
"""

from typing import Any, Dict, List, TYPE_CHECKING

if TYPE_CHECKING:
    from .builder import QueryBuilder


class GroupByQueryBuilder:
    """
    Builder for grouped aggregation queries.

    Allows performing aggregations (count, sum, avg, max, min)
    grouped by a specific field.

    Example:
        count_by_status = (client.query_builder()
            .collection("orders")
            .group_by("status")
            .count())
        # Returns: {"pending": 10, "completed": 50, "cancelled": 5}
    """

    def __init__(self, query_builder: "QueryBuilder", group_by_field: str):
        """
        Initialize a group by query builder.

        Args:
            query_builder: The parent query builder.
            group_by_field: The field to group by (supports dot notation).
        """
        self._query_builder = query_builder
        self._group_by_field = group_by_field

    def _get_group_key(self, record: Dict[str, Any]) -> str:
        """
        Get the group key from a record, supporting nested field paths.

        Args:
            record: The record to extract the key from.

        Returns:
            The string key for grouping.
        """
        # Support nested field paths (e.g., "user.country")
        if "." in self._group_by_field:
            parts = self._group_by_field.split(".")
            current: Any = record
            for part in parts:
                if isinstance(current, dict):
                    current = current.get(part)
                else:
                    current = None
            return str(current) if current is not None else "null"

        value = record.get(self._group_by_field)
        return str(value) if value is not None else "null"

    def count(self) -> Dict[str, int]:
        """
        Count records in each group.

        Returns:
            Dictionary mapping group keys to counts.
        """
        response = self._query_builder.clone().execute()
        records = response.get("records", [])

        groups: Dict[str, int] = {}
        for record in records:
            key = self._get_group_key(record)
            groups[key] = groups.get(key, 0) + 1

        return groups

    def sum_by(self, field: str) -> Dict[str, float]:
        """
        Sum a numeric field within each group.

        Args:
            field: The field to sum.

        Returns:
            Dictionary mapping group keys to sums.
        """
        response = self._query_builder.clone().execute()
        records = response.get("records", [])

        groups: Dict[str, float] = {}
        for record in records:
            key = self._get_group_key(record)
            value = record.get(field, 0)
            numeric_value = float(value) if isinstance(value, (int, float)) else 0.0
            groups[key] = groups.get(key, 0.0) + numeric_value

        return groups

    def avg_by(self, field: str) -> Dict[str, float]:
        """
        Calculate average of a numeric field within each group.

        Args:
            field: The field to average.

        Returns:
            Dictionary mapping group keys to averages.
        """
        response = self._query_builder.clone().execute()
        records = response.get("records", [])

        groups: Dict[str, Dict[str, float]] = {}
        for record in records:
            key = self._get_group_key(record)
            if key not in groups:
                groups[key] = {"sum": 0.0, "count": 0}
            value = record.get(field, 0)
            numeric_value = float(value) if isinstance(value, (int, float)) else 0.0
            groups[key]["sum"] += numeric_value
            groups[key]["count"] += 1

        result: Dict[str, float] = {}
        for key, data in groups.items():
            if data["count"] > 0:
                result[key] = data["sum"] / data["count"]
            else:
                result[key] = 0.0

        return result

    def max_by(self, field: str) -> Dict[str, Any]:
        """
        Find maximum value of a field within each group.

        Args:
            field: The field to find maximum of.

        Returns:
            Dictionary mapping group keys to maximum values.
        """
        response = self._query_builder.clone().execute()
        records = response.get("records", [])

        groups: Dict[str, Any] = {}
        for record in records:
            key = self._get_group_key(record)
            value = record.get(field)
            if key not in groups or (value is not None and value > groups[key]):
                groups[key] = value

        return groups

    def min_by(self, field: str) -> Dict[str, Any]:
        """
        Find minimum value of a field within each group.

        Args:
            field: The field to find minimum of.

        Returns:
            Dictionary mapping group keys to minimum values.
        """
        response = self._query_builder.clone().execute()
        records = response.get("records", [])

        groups: Dict[str, Any] = {}
        for record in records:
            key = self._get_group_key(record)
            value = record.get(field)
            if key not in groups or (value is not None and value < groups[key]):
                groups[key] = value

        return groups
