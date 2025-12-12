"""
Field condition builder for creating individual field conditions.

Used within ConditionBuilder for complex queries with AND/OR/NOT groups.
"""

from typing import Any, List, Dict, Union


class FieldCondition:
    """
    Builder for creating field conditions.

    This class is used within ConditionBuilder to create conditions
    that can be combined with logical operators.
    """

    def __init__(self, field_name: str):
        """
        Initialize a field condition.

        Args:
            field_name: The name of the field to filter on.
                       Supports dot notation for nested fields (e.g., 'user.email').
        """
        self._field_name = field_name
        self._operator: str | None = None
        self._value: Any = None

    # ===== COMPARISON OPERATORS =====

    def equals(self, value: Any) -> "FieldCondition":
        """Match documents where the field equals the value."""
        self._operator = "is"
        self._value = value
        return self

    def not_equals(self, value: Any) -> "FieldCondition":
        """Match documents where the field does not equal the value."""
        self._operator = "isNot"
        self._value = value
        return self

    def greater_than(self, value: Union[int, float]) -> "FieldCondition":
        """Match documents where the field is greater than the value."""
        self._operator = "greaterThan"
        self._value = value
        return self

    def greater_than_or_equal(self, value: Union[int, float]) -> "FieldCondition":
        """Match documents where the field is greater than or equal to the value."""
        self._operator = "greaterThanOrEqual"
        self._value = value
        return self

    def less_than(self, value: Union[int, float]) -> "FieldCondition":
        """Match documents where the field is less than the value."""
        self._operator = "lessThan"
        self._value = value
        return self

    def less_than_or_equal(self, value: Union[int, float]) -> "FieldCondition":
        """Match documents where the field is less than or equal to the value."""
        self._operator = "lessThanOrEqual"
        self._value = value
        return self

    def between(
        self, min_val: Union[int, float], max_val: Union[int, float]
    ) -> "FieldCondition":
        """Match documents where the field is between min and max values."""
        self._operator = "betweenOp"
        self._value = {"from": min_val, "to": max_val}
        return self

    # ===== STRING OPERATORS =====

    def contains(self, value: str) -> "FieldCondition":
        """Match documents where the field contains the substring."""
        self._operator = "includes"
        self._value = value
        return self

    def starts_with(self, value: str) -> "FieldCondition":
        """Match documents where the field starts with the value."""
        self._operator = "startsWith"
        self._value = value
        return self

    def ends_with(self, value: str) -> "FieldCondition":
        """Match documents where the field ends with the value."""
        self._operator = "endsWith"
        self._value = value
        return self

    def reg_exp_matches(self, pattern: str) -> "FieldCondition":
        """Match documents where the field matches the regular expression."""
        self._operator = "regExpMatches"
        self._value = pattern
        return self

    def includes_case_insensitive(self, value: str) -> "FieldCondition":
        """Match documents where the field contains the substring (case insensitive)."""
        self._operator = "includesCaseInsensitive"
        self._value = value
        return self

    def starts_with_case_insensitive(self, value: str) -> "FieldCondition":
        """Match documents where the field starts with the value (case insensitive)."""
        self._operator = "startsWithCaseInsensitive"
        self._value = value
        return self

    def ends_with_case_insensitive(self, value: str) -> "FieldCondition":
        """Match documents where the field ends with the value (case insensitive)."""
        self._operator = "endsWithCaseInsensitive"
        self._value = value
        return self

    # ===== ARRAY OPERATORS =====

    def is_in(self, values: List[Any]) -> "FieldCondition":
        """Match documents where the field value is in the list."""
        self._operator = "in"
        self._value = values
        return self

    def not_in(self, values: List[Any]) -> "FieldCondition":
        """Match documents where the field value is not in the list."""
        self._operator = "notIn"
        self._value = values
        return self

    # ===== EXISTENCE OPERATORS =====

    def exists(self) -> "FieldCondition":
        """Match documents where the field exists."""
        self._operator = "exists"
        self._value = True
        return self

    def not_exists(self) -> "FieldCondition":
        """Match documents where the field does not exist."""
        self._operator = "exists"
        self._value = False
        return self

    def is_null(self) -> "FieldCondition":
        """Match documents where the field is null."""
        self._operator = "isNull"
        self._value = True
        return self

    def is_not_null(self) -> "FieldCondition":
        """Match documents where the field is not null."""
        self._operator = "isNull"
        self._value = False
        return self

    # ===== BOOLEAN OPERATORS =====

    def is_true(self) -> "FieldCondition":
        """Match documents where the field is true."""
        return self.equals(True)

    def is_false(self) -> "FieldCondition":
        """Match documents where the field is false."""
        return self.equals(False)

    # ===== IP OPERATORS =====

    def is_local_ip(self) -> "FieldCondition":
        """Match documents where the field is a local IP address."""
        self._operator = "isLocalIp"
        self._value = True
        return self

    def is_external_ip(self) -> "FieldCondition":
        """Match documents where the field is an external IP address."""
        self._operator = "isExternalIp"
        self._value = True
        return self

    def in_country(self, country_code: str) -> "FieldCondition":
        """Match documents where the IP field is in the specified country."""
        self._operator = "inCountry"
        self._value = country_code
        return self

    def cidr(self, cidr_range: str) -> "FieldCondition":
        """Match documents where the IP field is within the CIDR range."""
        self._operator = "cidr"
        self._value = cidr_range
        return self

    # ===== SPECIAL OPERATORS =====

    def b64(self, value: str) -> "FieldCondition":
        """Match documents using base64 encoded value."""
        self._operator = "b64"
        self._value = value
        return self

    def in_dataset(self, dataset: str) -> "FieldCondition":
        """Match documents where the field value is in the specified dataset."""
        self._operator = "inDataset"
        self._value = dataset
        return self

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the field condition to a dictionary for JSON serialization.

        Returns:
            Dictionary representation supporting nested field paths.
        """
        condition = {self._operator: self._value}

        # Handle nested field names with dot notation
        parts = self._field_name.split(".")

        if len(parts) == 1:
            return {self._field_name: condition}

        # Build nested structure from inside out
        result = condition
        for i in range(len(parts) - 1, -1, -1):
            result = {parts[i]: result}

        return result
