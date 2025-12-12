"""
Selection builder for constructing field selections.

Provides a fluent interface for specifying which fields to include
or exclude in query results.
"""

from typing import Dict, List, Any, Callable


class SelectionBuilder:
    """
    Builder for constructing field selections.

    Allows specifying which fields to include or exclude in query results,
    as well as configuring nested field selections.

    Example:
        query.select(lambda s: s
            .field("name")
            .field("email")
            .nested("profile", lambda n: n.field("avatar").field("bio"))
        )
    """

    def __init__(self):
        """Initialize the selection builder."""
        self._selections: Dict[str, Any] = {}

    def field(self, name: str) -> "SelectionBuilder":
        """
        Include a field in the selection.

        Args:
            name: The name of the field to include.

        Returns:
            Self for method chaining.
        """
        self._selections[name] = True
        return self

    def fields(self, names: List[str]) -> "SelectionBuilder":
        """
        Include multiple fields in the selection.

        Args:
            names: List of field names to include.

        Returns:
            Self for method chaining.
        """
        for name in names:
            self._selections[name] = True
        return self

    def nested(
        self,
        name: str,
        builder_fn: Callable[["SelectionBuilder"], "SelectionBuilder"],
    ) -> "SelectionBuilder":
        """
        Configure nested field selection.

        Args:
            name: The name of the nested field/object.
            builder_fn: A function that configures the nested selection.

        Returns:
            Self for method chaining.
        """
        nested_builder = SelectionBuilder()
        builder_fn(nested_builder)
        self._selections[name] = nested_builder.build()
        return self

    def exclude(self, name: str) -> "SelectionBuilder":
        """
        Exclude a field from the selection.

        Args:
            name: The name of the field to exclude.

        Returns:
            Self for method chaining.
        """
        self._selections[name] = False
        return self

    def exclude_fields(self, names: List[str]) -> "SelectionBuilder":
        """
        Exclude multiple fields from the selection.

        Args:
            names: List of field names to exclude.

        Returns:
            Self for method chaining.
        """
        for name in names:
            self._selections[name] = False
        return self

    def clear(self) -> "SelectionBuilder":
        """
        Clear all selections.

        Returns:
            Self for method chaining.
        """
        self._selections = {}
        return self

    def build(self) -> Dict[str, Any]:
        """
        Build the selection dictionary.

        Returns:
            Dictionary representing the field selection.
        """
        return self._selections

    @staticmethod
    def all() -> Dict[str, Any]:
        """
        Create a selection that includes all fields.

        Returns:
            Empty dictionary (signals all fields should be included).
        """
        return {}
