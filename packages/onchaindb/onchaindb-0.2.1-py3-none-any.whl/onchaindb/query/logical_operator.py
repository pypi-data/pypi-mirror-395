"""
Logical operator for building complex query conditions.
"""

from typing import Dict, List, Any, Union, TYPE_CHECKING

if TYPE_CHECKING:
    from .field_condition import FieldCondition


class LogicalOperator:
    """
    Factory class for creating logical operators (AND, OR, NOT).

    Used to combine multiple conditions in complex queries.
    """

    def __init__(self, operator_type: str, conditions: List[Any]):
        """
        Initialize a logical operator.

        Args:
            operator_type: The type of operator ('and', 'or', 'not', 'condition').
            conditions: The conditions to combine.
        """
        self._type = operator_type
        self._conditions = conditions

    @classmethod
    def And(cls, conditions: List["LogicalOperator"]) -> "LogicalOperator":
        """
        Create an AND condition that matches all provided conditions.

        Args:
            conditions: List of conditions that must all be true.

        Returns:
            A LogicalOperator representing the AND condition.
        """
        return cls("and", conditions)

    @classmethod
    def Or(cls, conditions: List["LogicalOperator"]) -> "LogicalOperator":
        """
        Create an OR condition that matches any of the provided conditions.

        Args:
            conditions: List of conditions where at least one must be true.

        Returns:
            A LogicalOperator representing the OR condition.
        """
        return cls("or", conditions)

    @classmethod
    def Not(cls, conditions: List["LogicalOperator"]) -> "LogicalOperator":
        """
        Create a NOT condition that negates the provided conditions.

        Args:
            conditions: List of conditions to negate.

        Returns:
            A LogicalOperator representing the NOT condition.
        """
        return cls("not", conditions)

    @classmethod
    def Condition(cls, field_condition: "FieldCondition") -> "LogicalOperator":
        """
        Wrap a field condition as a logical operator.

        Args:
            field_condition: The field condition to wrap.

        Returns:
            A LogicalOperator representing the condition.
        """
        return cls("condition", [field_condition.to_dict()])

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the logical operator to a dictionary for JSON serialization.

        Returns:
            Dictionary representation of the operator.
        """
        if self._type == "condition":
            return self._conditions[0]

        result = []
        for condition in self._conditions:
            if isinstance(condition, LogicalOperator):
                result.append(condition.to_dict())
            else:
                result.append(condition)

        return {self._type: result}

    # Aliases for Pythonic naming
    @classmethod
    def and_group(cls, conditions: List["LogicalOperator"]) -> "LogicalOperator":
        """Alias for And()."""
        return cls.And(conditions)

    @classmethod
    def or_group(cls, conditions: List["LogicalOperator"]) -> "LogicalOperator":
        """Alias for Or()."""
        return cls.Or(conditions)

    @classmethod
    def not_group(cls, conditions: List["LogicalOperator"]) -> "LogicalOperator":
        """Alias for Not()."""
        return cls.Not(conditions)

    @staticmethod
    def condition(cond: Dict[str, Any]) -> Dict[str, Any]:
        """
        Pass through a condition dictionary.

        Args:
            cond: The condition dictionary.

        Returns:
            The same condition dictionary.
        """
        return cond
