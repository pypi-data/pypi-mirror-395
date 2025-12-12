"""
Join builder for constructing server-side JOINs.

Provides a fluent interface for creating one-to-one and one-to-many
relationships between collections.
"""

from typing import Any, Dict, List, Optional, Callable, Union, TYPE_CHECKING

from .condition_builder import ConditionBuilder
from .selection_builder import SelectionBuilder
from .logical_operator import LogicalOperator

if TYPE_CHECKING:
    from .builder import QueryBuilder


class JoinWhereClause:
    """
    Where clause for JOIN conditions.

    Provides operators for specifying JOIN conditions.
    """

    def __init__(self, join_builder: "JoinBuilder", field_name: str):
        """
        Initialize a join where clause.

        Args:
            join_builder: The parent join builder.
            field_name: The name of the field to filter on.
        """
        self._join_builder = join_builder
        self._field_name = field_name

    def equals(self, value: Any) -> "JoinBuilder":
        """
        Match where the field equals the value.

        Use '$parent.field_name' to reference parent document fields.
        """
        self._join_builder._set_find_conditions({self._field_name: {"is": value}})
        return self._join_builder

    def is_in(self, values: List[Any]) -> "JoinBuilder":
        """Match where the field value is in the list."""
        self._join_builder._set_find_conditions({self._field_name: {"in": values}})
        return self._join_builder

    def greater_than(self, value: Union[int, float]) -> "JoinBuilder":
        """Match where the field is greater than the value."""
        self._join_builder._set_find_conditions(
            {self._field_name: {"greaterThan": value}}
        )
        return self._join_builder

    def less_than(self, value: Union[int, float]) -> "JoinBuilder":
        """Match where the field is less than the value."""
        self._join_builder._set_find_conditions(
            {self._field_name: {"lessThan": value}}
        )
        return self._join_builder

    def is_null(self) -> "JoinBuilder":
        """Match where the field is null."""
        self._join_builder._set_find_conditions({self._field_name: {"isNull": True}})
        return self._join_builder

    def is_not_null(self) -> "JoinBuilder":
        """Match where the field is not null."""
        self._join_builder._set_find_conditions({self._field_name: {"isNull": False}})
        return self._join_builder


class NestedJoinWhereClause:
    """Where clause for nested JOIN conditions."""

    def __init__(self, join_builder: "NestedJoinBuilder", field_name: str):
        """
        Initialize a nested join where clause.

        Args:
            join_builder: The parent nested join builder.
            field_name: The name of the field to filter on.
        """
        self._join_builder = join_builder
        self._field_name = field_name

    def equals(self, value: Any) -> "NestedJoinBuilder":
        """Match where the field equals the value."""
        self._join_builder._set_find_conditions({self._field_name: {"is": value}})
        return self._join_builder


class NestedJoinBuilder:
    """
    Builder for nested JOINs (JOINs within JOINs).
    """

    def __init__(
        self,
        parent_builder: "JoinBuilder",
        alias: str,
        model: str,
        many: Optional[bool] = None,
    ):
        """
        Initialize a nested join builder.

        Args:
            parent_builder: The parent join builder.
            alias: The alias for the joined data in the result.
            model: The name of the collection to join.
            many: If True, returns array; if False, returns single object.
        """
        self._parent_builder = parent_builder
        self._alias = alias
        self._model = model
        self._many = many
        self._find_conditions: Dict[str, Any] = {}
        self._selections: Optional[Dict[str, bool]] = None

    def on_field(self, field_name: str) -> NestedJoinWhereClause:
        """
        Add a condition on a field.

        Args:
            field_name: The name of the field to filter on.

        Returns:
            A NestedJoinWhereClause for specifying the condition.
        """
        return NestedJoinWhereClause(self, field_name)

    def select_fields(self, fields: List[str]) -> "NestedJoinBuilder":
        """
        Select specific fields from the joined collection.

        Args:
            fields: List of field names to include.

        Returns:
            Self for method chaining.
        """
        self._selections = {}
        for field in fields:
            self._selections[field] = True
        return self

    def select_all(self) -> "NestedJoinBuilder":
        """
        Select all fields from the joined collection.

        Returns:
            Self for method chaining.
        """
        self._selections = {}
        return self

    def _set_find_conditions(self, conditions: Dict[str, Any]) -> None:
        """Internal: Set find conditions."""
        self._find_conditions = conditions

    def build(self) -> "JoinBuilder":
        """
        Complete the nested JOIN and return to the parent join builder.

        Returns:
            The parent JoinBuilder for method chaining.
        """
        config: Dict[str, Any] = {
            "alias": self._alias,
            "model": self._model,
            "resolve": {
                "find": self._find_conditions if self._find_conditions else None,
                "select": self._selections if self._selections is not None else {},
            },
        }

        if self._many is not None:
            config["many"] = self._many

        self._parent_builder._add_nested_join(config)

        return self._parent_builder


class JoinBuilder:
    """
    Fluent builder for constructing server-side JOINs.

    Allows specifying conditions, field selection, and nested JOINs.

    Example:
        users = (client.query_builder()
            .collection("users")
            .join_one("profile", "profiles")
                .on_field("user_id").equals("$parent.id")
                .select_fields(["avatar", "bio"])
                .build()
            .execute())
    """

    def __init__(
        self,
        parent_builder: "QueryBuilder",
        alias: str,
        model: str,
        many: Optional[bool] = None,
    ):
        """
        Initialize a join builder.

        Args:
            parent_builder: The parent query builder.
            alias: The alias for the joined data in the result.
            model: The name of the collection to join.
            many: If True, returns array; if False, returns single object.
        """
        self._parent_builder = parent_builder
        self._alias = alias
        self._model = model
        self._many = many
        self._find_conditions: Dict[str, Any] = {}
        self._selections: Optional[Dict[str, bool]] = None
        self._nested_joins: List[Dict[str, Any]] = []

    def on_field(self, field_name: str) -> JoinWhereClause:
        """
        Add a simple equality condition on a field.

        Args:
            field_name: The name of the field to filter on.

        Returns:
            A JoinWhereClause for specifying the condition.
        """
        return JoinWhereClause(self, field_name)

    def on(
        self,
        builder_fn: Callable[[ConditionBuilder], LogicalOperator],
    ) -> "JoinBuilder":
        """
        Add complex filter conditions.

        Args:
            builder_fn: A function that builds conditions using ConditionBuilder.

        Returns:
            Self for method chaining.
        """
        builder = ConditionBuilder()
        operator = builder_fn(builder)
        if isinstance(operator, LogicalOperator):
            self._find_conditions = operator.to_dict()
        else:
            self._find_conditions = operator
        return self

    def select_fields(self, fields: List[str]) -> "JoinBuilder":
        """
        Select specific fields from the joined collection.

        Args:
            fields: List of field names to include.

        Returns:
            Self for method chaining.
        """
        self._selections = {}
        for field in fields:
            self._selections[field] = True
        return self

    def select_all(self) -> "JoinBuilder":
        """
        Select all fields from the joined collection.

        Returns:
            Self for method chaining.
        """
        self._selections = {}
        return self

    def selecting(
        self,
        builder_fn: Callable[[SelectionBuilder], SelectionBuilder],
    ) -> "JoinBuilder":
        """
        Configure selection with a builder function.

        Args:
            builder_fn: A function that builds the selection.

        Returns:
            Self for method chaining.
        """
        builder = SelectionBuilder()
        builder_fn(builder)
        self._selections = builder.build()
        return self

    def join_one(self, alias: str, model: str) -> NestedJoinBuilder:
        """
        Add a nested one-to-one JOIN.

        Args:
            alias: The alias for the nested joined data.
            model: The name of the collection to join.

        Returns:
            A NestedJoinBuilder for configuring the join.
        """
        return NestedJoinBuilder(self, alias, model, False)

    def join_many(self, alias: str, model: str) -> NestedJoinBuilder:
        """
        Add a nested one-to-many JOIN.

        Args:
            alias: The alias for the nested joined data.
            model: The name of the collection to join.

        Returns:
            A NestedJoinBuilder for configuring the join.
        """
        return NestedJoinBuilder(self, alias, model, True)

    def _set_find_conditions(self, conditions: Dict[str, Any]) -> None:
        """Internal: Set find conditions."""
        self._find_conditions = conditions

    def _add_nested_join(self, config: Dict[str, Any]) -> None:
        """Internal: Add a nested join configuration."""
        self._nested_joins.append(config)

    def build(self) -> "QueryBuilder":
        """
        Complete the JOIN and return to the parent query builder.

        Returns:
            The parent QueryBuilder for method chaining.
        """
        find = dict(self._find_conditions)

        # Add nested JOINs to find conditions
        for nested_join in self._nested_joins:
            join_config: Dict[str, Any] = {
                "resolve": nested_join["resolve"],
                "model": nested_join["model"],
            }

            if "many" in nested_join:
                join_config["many"] = nested_join["many"]

            find[nested_join["alias"]] = join_config

        config: Dict[str, Any] = {
            "alias": self._alias,
            "model": self._model,
            "resolve": {
                "find": find if find else None,
                "select": self._selections if self._selections is not None else {},
            },
        }

        if self._many is not None:
            config["many"] = self._many

        self._parent_builder._add_server_join(config)

        return self._parent_builder
