"""
Condition builder for creating complex query conditions.

Provides a fluent interface for building AND/OR/NOT condition groups.
"""

from typing import Any, List, Dict, Callable, Union

from .field_condition import FieldCondition
from .logical_operator import LogicalOperator


class ConditionFieldBuilder:
    """
    Field builder for use within condition callbacks.

    This class provides the same operators as FieldCondition but returns
    dictionaries directly for use in logical operator groups.
    """

    def __init__(self, field_name: str):
        """
        Initialize a condition field builder.

        Args:
            field_name: The name of the field to filter on.
        """
        self._field_name = field_name

    def _make_condition(
        self, operator: str, value: Any = None
    ) -> Dict[str, Any]:
        """Build a condition dictionary."""
        condition = {operator: value}

        # Handle nested field names with dot notation
        parts = self._field_name.split(".")

        if len(parts) == 1:
            return {self._field_name: condition}

        # Build nested structure from inside out
        result = condition
        for i in range(len(parts) - 1, -1, -1):
            result = {parts[i]: result}

        return result

    # ===== COMPARISON OPERATORS =====

    def equals(self, value: Any) -> Dict[str, Any]:
        """Match documents where the field equals the value."""
        return self._make_condition("is", value)

    def not_equals(self, value: Any) -> Dict[str, Any]:
        """Match documents where the field does not equal the value."""
        return self._make_condition("isNot", value)

    def greater_than(self, value: Union[int, float]) -> Dict[str, Any]:
        """Match documents where the field is greater than the value."""
        return self._make_condition("greaterThan", value)

    def greater_than_or_equal(self, value: Union[int, float]) -> Dict[str, Any]:
        """Match documents where the field is >= the value."""
        return self._make_condition("greaterThanOrEqual", value)

    def less_than(self, value: Union[int, float]) -> Dict[str, Any]:
        """Match documents where the field is less than the value."""
        return self._make_condition("lessThan", value)

    def less_than_or_equal(self, value: Union[int, float]) -> Dict[str, Any]:
        """Match documents where the field is <= the value."""
        return self._make_condition("lessThanOrEqual", value)

    def between(
        self, min_val: Union[int, float], max_val: Union[int, float]
    ) -> Dict[str, Any]:
        """Match documents where the field is between min and max."""
        return self._make_condition("betweenOp", {"from": min_val, "to": max_val})

    # ===== STRING OPERATORS =====

    def contains(self, value: str) -> Dict[str, Any]:
        """Match documents where the field contains the substring."""
        return self._make_condition("includes", value)

    def starts_with(self, value: str) -> Dict[str, Any]:
        """Match documents where the field starts with the value."""
        return self._make_condition("startsWith", value)

    def ends_with(self, value: str) -> Dict[str, Any]:
        """Match documents where the field ends with the value."""
        return self._make_condition("endsWith", value)

    def reg_exp_matches(self, pattern: str) -> Dict[str, Any]:
        """Match documents where the field matches the regex."""
        return self._make_condition("regExpMatches", pattern)

    def includes_case_insensitive(self, value: str) -> Dict[str, Any]:
        """Match documents where field contains value (case insensitive)."""
        return self._make_condition("includesCaseInsensitive", value)

    def starts_with_case_insensitive(self, value: str) -> Dict[str, Any]:
        """Match documents where field starts with value (case insensitive)."""
        return self._make_condition("startsWithCaseInsensitive", value)

    def ends_with_case_insensitive(self, value: str) -> Dict[str, Any]:
        """Match documents where field ends with value (case insensitive)."""
        return self._make_condition("endsWithCaseInsensitive", value)

    # ===== ARRAY OPERATORS =====

    def is_in(self, values: List[Any]) -> Dict[str, Any]:
        """Match documents where the field value is in the list."""
        return self._make_condition("in", values)

    def not_in(self, values: List[Any]) -> Dict[str, Any]:
        """Match documents where the field value is not in the list."""
        return self._make_condition("notIn", values)

    # ===== EXISTENCE OPERATORS =====

    def exists(self) -> Dict[str, Any]:
        """Match documents where the field exists."""
        return self._make_condition("exists", True)

    def not_exists(self) -> Dict[str, Any]:
        """Match documents where the field does not exist."""
        return self._make_condition("exists", False)

    def is_null(self) -> Dict[str, Any]:
        """Match documents where the field is null."""
        return self._make_condition("isNull", True)

    def is_not_null(self) -> Dict[str, Any]:
        """Match documents where the field is not null."""
        return self._make_condition("isNull", False)

    # ===== BOOLEAN OPERATORS =====

    def is_true(self) -> Dict[str, Any]:
        """Match documents where the field is true."""
        return self.equals(True)

    def is_false(self) -> Dict[str, Any]:
        """Match documents where the field is false."""
        return self.equals(False)

    # ===== IP OPERATORS =====

    def is_local_ip(self) -> Dict[str, Any]:
        """Match documents where the field is a local IP address."""
        return self._make_condition("isLocalIp", True)

    def is_external_ip(self) -> Dict[str, Any]:
        """Match documents where the field is an external IP address."""
        return self._make_condition("isExternalIp", True)

    def in_country(self, country_code: str) -> Dict[str, Any]:
        """Match documents where the IP field is in the specified country."""
        return self._make_condition("inCountry", country_code)

    def cidr(self, cidr_range: str) -> Dict[str, Any]:
        """Match documents where the IP field is within the CIDR range."""
        return self._make_condition("cidr", cidr_range)

    # ===== SPECIAL OPERATORS =====

    def b64(self, value: str) -> Dict[str, Any]:
        """Match documents using base64 encoded value."""
        return self._make_condition("b64", value)

    def in_dataset(self, dataset: str) -> Dict[str, Any]:
        """Match documents where the field value is in the dataset."""
        return self._make_condition("inDataset", dataset)


class ConditionBuilder:
    """
    Builder for creating complex conditions with AND/OR/NOT groups.

    Used with the QueryBuilder.find() method to create complex queries.

    Example:
        results = (client.query_builder()
            .collection("users")
            .find(lambda c: c.and_group(lambda: [
                c.field("status").equals("active"),
                c.or_group(lambda: [
                    c.field("role").equals("admin"),
                    c.field("role").equals("moderator"),
                ]),
            ]))
            .execute())
    """

    def field(self, name: str) -> ConditionFieldBuilder:
        """
        Create a field condition builder.

        Args:
            name: The name of the field to filter on.

        Returns:
            A ConditionFieldBuilder for the specified field.
        """
        return ConditionFieldBuilder(name)

    def and_group(
        self, builder_fn: Callable[[], List[Dict[str, Any]]]
    ) -> Dict[str, Any]:
        """
        Create an AND group that matches all conditions.

        Args:
            builder_fn: A callable that returns a list of conditions.

        Returns:
            Dictionary representing the AND group.
        """
        conditions = builder_fn()
        return {"and": conditions}

    def or_group(
        self, builder_fn: Callable[[], List[Dict[str, Any]]]
    ) -> Dict[str, Any]:
        """
        Create an OR group that matches any condition.

        Args:
            builder_fn: A callable that returns a list of conditions.

        Returns:
            Dictionary representing the OR group.
        """
        conditions = builder_fn()
        return {"or": conditions}

    def not_group(
        self, builder_fn: Callable[[], List[Dict[str, Any]]]
    ) -> Dict[str, Any]:
        """
        Create a NOT group that negates conditions.

        Args:
            builder_fn: A callable that returns a list of conditions.

        Returns:
            Dictionary representing the NOT group.
        """
        conditions = builder_fn()
        return {"not": conditions}
