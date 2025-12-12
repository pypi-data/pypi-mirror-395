"""
Where clause builder for the fluent query API.

Used with QueryBuilder.where_field() to add field conditions directly.
"""

from typing import Any, List, Dict, Union, TYPE_CHECKING

if TYPE_CHECKING:
    from .builder import QueryBuilder


class WhereClause:
    """
    Fluent where clause builder with all operators.

    This class is returned by QueryBuilder.where_field() and provides
    all available operators for filtering.
    """

    def __init__(self, query_builder: "QueryBuilder", field_name: str):
        """
        Initialize a where clause.

        Args:
            query_builder: The parent query builder.
            field_name: The name of the field to filter on.
        """
        self._query_builder = query_builder
        self._field_name = field_name

    def _build_nested_condition(self, condition: Dict[str, Any]) -> Dict[str, Any]:
        """Build nested field condition for dot notation."""
        parts = self._field_name.split(".")

        if len(parts) == 1:
            return {self._field_name: condition}

        # Build nested structure from inside out
        result = condition
        for i in range(len(parts) - 1, -1, -1):
            result = {parts[i]: result}

        return result

    def _set_condition(self, condition: Dict[str, Any]) -> "QueryBuilder":
        """Set the condition and return the query builder."""
        nested_condition = self._build_nested_condition(condition)
        self._query_builder._set_find_conditions(nested_condition)
        return self._query_builder

    # ===== COMPARISON OPERATORS =====

    def equals(self, value: Any) -> "QueryBuilder":
        """Match documents where the field equals the value."""
        return self._set_condition({"is": value})

    def not_equals(self, value: Any) -> "QueryBuilder":
        """Match documents where the field does not equal the value."""
        return self._set_condition({"isNot": value})

    def greater_than(self, value: Union[int, float]) -> "QueryBuilder":
        """Match documents where the field is greater than the value."""
        return self._set_condition({"greaterThan": value})

    def greater_than_or_equal(self, value: Union[int, float]) -> "QueryBuilder":
        """Match documents where the field is >= the value."""
        return self._set_condition({"greaterThanOrEqual": value})

    def less_than(self, value: Union[int, float]) -> "QueryBuilder":
        """Match documents where the field is less than the value."""
        return self._set_condition({"lessThan": value})

    def less_than_or_equal(self, value: Union[int, float]) -> "QueryBuilder":
        """Match documents where the field is <= the value."""
        return self._set_condition({"lessThanOrEqual": value})

    def between(
        self, min_val: Union[int, float], max_val: Union[int, float]
    ) -> "QueryBuilder":
        """Match documents where the field is between min and max values."""
        return self._set_condition({"betweenOp": {"from": min_val, "to": max_val}})

    # ===== STRING OPERATORS =====

    def contains(self, value: str) -> "QueryBuilder":
        """Match documents where the field contains the substring."""
        return self._set_condition({"includes": value})

    def starts_with(self, value: str) -> "QueryBuilder":
        """Match documents where the field starts with the value."""
        return self._set_condition({"startsWith": value})

    def ends_with(self, value: str) -> "QueryBuilder":
        """Match documents where the field ends with the value."""
        return self._set_condition({"endsWith": value})

    def reg_exp_matches(self, pattern: str) -> "QueryBuilder":
        """Match documents where the field matches the regular expression."""
        return self._set_condition({"regExpMatches": pattern})

    def includes_case_insensitive(self, value: str) -> "QueryBuilder":
        """Match documents where field contains value (case insensitive)."""
        return self._set_condition({"includesCaseInsensitive": value})

    def starts_with_case_insensitive(self, value: str) -> "QueryBuilder":
        """Match documents where field starts with value (case insensitive)."""
        return self._set_condition({"startsWithCaseInsensitive": value})

    def ends_with_case_insensitive(self, value: str) -> "QueryBuilder":
        """Match documents where field ends with value (case insensitive)."""
        return self._set_condition({"endsWithCaseInsensitive": value})

    # ===== ARRAY OPERATORS =====

    def is_in(self, values: List[Any]) -> "QueryBuilder":
        """Match documents where the field value is in the list."""
        return self._set_condition({"in": values})

    def not_in(self, values: List[Any]) -> "QueryBuilder":
        """Match documents where the field value is not in the list."""
        return self._set_condition({"notIn": values})

    # ===== EXISTENCE OPERATORS =====

    def exists(self) -> "QueryBuilder":
        """Match documents where the field exists."""
        return self._set_condition({"exists": True})

    def not_exists(self) -> "QueryBuilder":
        """Match documents where the field does not exist."""
        return self._set_condition({"exists": False})

    def is_null(self) -> "QueryBuilder":
        """Match documents where the field is null."""
        return self._set_condition({"isNull": True})

    def is_not_null(self) -> "QueryBuilder":
        """Match documents where the field is not null."""
        return self._set_condition({"isNull": False})

    # ===== BOOLEAN OPERATORS =====

    def is_true(self) -> "QueryBuilder":
        """Match documents where the field is true."""
        return self.equals(True)

    def is_false(self) -> "QueryBuilder":
        """Match documents where the field is false."""
        return self.equals(False)

    # ===== IP OPERATORS =====

    def is_local_ip(self) -> "QueryBuilder":
        """Match documents where the field is a local IP address."""
        return self._set_condition({"isLocalIp": True})

    def is_external_ip(self) -> "QueryBuilder":
        """Match documents where the field is an external IP address."""
        return self._set_condition({"isExternalIp": True})

    def in_country(self, country_code: str) -> "QueryBuilder":
        """Match documents where the IP field is in the specified country."""
        return self._set_condition({"inCountry": country_code})

    def cidr(self, cidr_range: str) -> "QueryBuilder":
        """Match documents where the IP field is within the CIDR range."""
        return self._set_condition({"cidr": cidr_range})

    # ===== SPECIAL OPERATORS =====

    def b64(self, value: str) -> "QueryBuilder":
        """Match documents using base64 encoded value."""
        return self._set_condition({"b64": value})

    def in_dataset(self, dataset: str) -> "QueryBuilder":
        """Match documents where the field value is in the dataset."""
        return self._set_condition({"inDataset": dataset})
