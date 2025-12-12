"""Tests for condition builders."""

import pytest

from onchaindb.query import (
    ConditionBuilder,
    ConditionFieldBuilder,
    FieldCondition,
    LogicalOperator,
)


class TestFieldCondition:
    """Tests for FieldCondition class."""

    def test_equals(self):
        """Test equals operator."""
        cond = FieldCondition("status")
        cond.equals("active")

        result = cond.to_dict()
        assert result == {"status": {"is": "active"}}

    def test_not_equals(self):
        """Test not equals operator."""
        cond = FieldCondition("status")
        cond.not_equals("deleted")

        result = cond.to_dict()
        assert result == {"status": {"isNot": "deleted"}}

    def test_greater_than(self):
        """Test greater than operator."""
        cond = FieldCondition("age")
        cond.greater_than(18)

        result = cond.to_dict()
        assert result == {"age": {"greaterThan": 18}}

    def test_greater_than_or_equal(self):
        """Test greater than or equal operator."""
        cond = FieldCondition("age")
        cond.greater_than_or_equal(18)

        result = cond.to_dict()
        assert result == {"age": {"greaterThanOrEqual": 18}}

    def test_less_than(self):
        """Test less than operator."""
        cond = FieldCondition("age")
        cond.less_than(65)

        result = cond.to_dict()
        assert result == {"age": {"lessThan": 65}}

    def test_less_than_or_equal(self):
        """Test less than or equal operator."""
        cond = FieldCondition("age")
        cond.less_than_or_equal(65)

        result = cond.to_dict()
        assert result == {"age": {"lessThanOrEqual": 65}}

    def test_between(self):
        """Test between operator."""
        cond = FieldCondition("age")
        cond.between(18, 65)

        result = cond.to_dict()
        assert result == {"age": {"betweenOp": {"from": 18, "to": 65}}}

    def test_contains(self):
        """Test contains operator."""
        cond = FieldCondition("email")
        cond.contains("@example")

        result = cond.to_dict()
        assert result == {"email": {"includes": "@example"}}

    def test_starts_with(self):
        """Test starts with operator."""
        cond = FieldCondition("name")
        cond.starts_with("John")

        result = cond.to_dict()
        assert result == {"name": {"startsWith": "John"}}

    def test_ends_with(self):
        """Test ends with operator."""
        cond = FieldCondition("email")
        cond.ends_with(".com")

        result = cond.to_dict()
        assert result == {"email": {"endsWith": ".com"}}

    def test_reg_exp_matches(self):
        """Test regex matches operator."""
        cond = FieldCondition("email")
        cond.reg_exp_matches(r"^[a-z]+@")

        result = cond.to_dict()
        assert result == {"email": {"regExpMatches": r"^[a-z]+@"}}

    def test_includes_case_insensitive(self):
        """Test case insensitive contains."""
        cond = FieldCondition("name")
        cond.includes_case_insensitive("john")

        result = cond.to_dict()
        assert result == {"name": {"includesCaseInsensitive": "john"}}

    def test_is_in(self):
        """Test is_in operator."""
        cond = FieldCondition("role")
        cond.is_in(["admin", "moderator"])

        result = cond.to_dict()
        assert result == {"role": {"in": ["admin", "moderator"]}}

    def test_not_in(self):
        """Test not_in operator."""
        cond = FieldCondition("status")
        cond.not_in(["deleted", "banned"])

        result = cond.to_dict()
        assert result == {"status": {"notIn": ["deleted", "banned"]}}

    def test_exists(self):
        """Test exists operator."""
        cond = FieldCondition("email")
        cond.exists()

        result = cond.to_dict()
        assert result == {"email": {"exists": True}}

    def test_not_exists(self):
        """Test not exists operator."""
        cond = FieldCondition("deleted_at")
        cond.not_exists()

        result = cond.to_dict()
        assert result == {"deleted_at": {"exists": False}}

    def test_is_null(self):
        """Test is null operator."""
        cond = FieldCondition("deleted_at")
        cond.is_null()

        result = cond.to_dict()
        assert result == {"deleted_at": {"isNull": True}}

    def test_is_not_null(self):
        """Test is not null operator."""
        cond = FieldCondition("email")
        cond.is_not_null()

        result = cond.to_dict()
        assert result == {"email": {"isNull": False}}

    def test_is_true(self):
        """Test is true operator."""
        cond = FieldCondition("is_active")
        cond.is_true()

        result = cond.to_dict()
        assert result == {"is_active": {"is": True}}

    def test_is_false(self):
        """Test is false operator."""
        cond = FieldCondition("is_deleted")
        cond.is_false()

        result = cond.to_dict()
        assert result == {"is_deleted": {"is": False}}

    def test_is_local_ip(self):
        """Test is local IP operator."""
        cond = FieldCondition("ip")
        cond.is_local_ip()

        result = cond.to_dict()
        assert result == {"ip": {"isLocalIp": True}}

    def test_is_external_ip(self):
        """Test is external IP operator."""
        cond = FieldCondition("ip")
        cond.is_external_ip()

        result = cond.to_dict()
        assert result == {"ip": {"isExternalIp": True}}

    def test_in_country(self):
        """Test in country operator."""
        cond = FieldCondition("ip")
        cond.in_country("US")

        result = cond.to_dict()
        assert result == {"ip": {"inCountry": "US"}}

    def test_cidr(self):
        """Test CIDR operator."""
        cond = FieldCondition("ip")
        cond.cidr("192.168.0.0/16")

        result = cond.to_dict()
        assert result == {"ip": {"cidr": "192.168.0.0/16"}}

    def test_b64(self):
        """Test base64 operator."""
        cond = FieldCondition("data")
        cond.b64("SGVsbG8gV29ybGQ=")

        result = cond.to_dict()
        assert result == {"data": {"b64": "SGVsbG8gV29ybGQ="}}

    def test_in_dataset(self):
        """Test in dataset operator."""
        cond = FieldCondition("email")
        cond.in_dataset("blocklist")

        result = cond.to_dict()
        assert result == {"email": {"inDataset": "blocklist"}}

    def test_nested_field(self):
        """Test nested field (dot notation)."""
        cond = FieldCondition("user.address.city")
        cond.equals("New York")

        result = cond.to_dict()
        assert result == {"user": {"address": {"city": {"is": "New York"}}}}


class TestConditionFieldBuilder:
    """Tests for ConditionFieldBuilder class."""

    def test_equals(self):
        """Test equals returns dict directly."""
        builder = ConditionFieldBuilder("status")
        result = builder.equals("active")

        assert result == {"status": {"is": "active"}}

    def test_not_equals(self):
        """Test not equals returns dict directly."""
        builder = ConditionFieldBuilder("status")
        result = builder.not_equals("deleted")

        assert result == {"status": {"isNot": "deleted"}}

    def test_nested_field(self):
        """Test nested field in condition builder."""
        builder = ConditionFieldBuilder("user.email")
        result = builder.equals("test@example.com")

        assert result == {"user": {"email": {"is": "test@example.com"}}}


class TestConditionBuilder:
    """Tests for ConditionBuilder class."""

    def test_and_group(self):
        """Test AND group."""
        builder = ConditionBuilder()

        result = builder.and_group(lambda: [
            builder.field("status").equals("active"),
            builder.field("age").greater_than(18),
        ])

        assert result == {
            "and": [
                {"status": {"is": "active"}},
                {"age": {"greaterThan": 18}},
            ]
        }

    def test_or_group(self):
        """Test OR group."""
        builder = ConditionBuilder()

        result = builder.or_group(lambda: [
            builder.field("role").equals("admin"),
            builder.field("role").equals("moderator"),
        ])

        assert result == {
            "or": [
                {"role": {"is": "admin"}},
                {"role": {"is": "moderator"}},
            ]
        }

    def test_not_group(self):
        """Test NOT group."""
        builder = ConditionBuilder()

        result = builder.not_group(lambda: [
            builder.field("status").equals("deleted"),
        ])

        assert result == {
            "not": [
                {"status": {"is": "deleted"}},
            ]
        }

    def test_nested_groups(self):
        """Test nested AND/OR groups."""
        builder = ConditionBuilder()

        result = builder.and_group(lambda: [
            builder.field("status").equals("active"),
            builder.or_group(lambda: [
                builder.field("role").equals("admin"),
                builder.field("role").equals("moderator"),
            ]),
        ])

        assert result == {
            "and": [
                {"status": {"is": "active"}},
                {
                    "or": [
                        {"role": {"is": "admin"}},
                        {"role": {"is": "moderator"}},
                    ]
                },
            ]
        }


class TestLogicalOperator:
    """Tests for LogicalOperator class."""

    def test_and(self):
        """Test AND operator."""
        cond1 = FieldCondition("status")
        cond1.equals("active")

        cond2 = FieldCondition("age")
        cond2.greater_than(18)

        result = LogicalOperator.And([
            LogicalOperator.Condition(cond1),
            LogicalOperator.Condition(cond2),
        ])

        assert result.to_dict() == {
            "and": [
                {"status": {"is": "active"}},
                {"age": {"greaterThan": 18}},
            ]
        }

    def test_or(self):
        """Test OR operator."""
        cond1 = FieldCondition("role")
        cond1.equals("admin")

        cond2 = FieldCondition("role")
        cond2.equals("moderator")

        result = LogicalOperator.Or([
            LogicalOperator.Condition(cond1),
            LogicalOperator.Condition(cond2),
        ])

        assert result.to_dict() == {
            "or": [
                {"role": {"is": "admin"}},
                {"role": {"is": "moderator"}},
            ]
        }

    def test_not(self):
        """Test NOT operator."""
        cond = FieldCondition("status")
        cond.equals("deleted")

        result = LogicalOperator.Not([
            LogicalOperator.Condition(cond),
        ])

        assert result.to_dict() == {
            "not": [
                {"status": {"is": "deleted"}},
            ]
        }

    def test_condition_wrapper(self):
        """Test Condition static method wraps properly."""
        cond = FieldCondition("email")
        cond.equals("test@example.com")

        result = LogicalOperator.Condition(cond)

        assert result.to_dict() == {"email": {"is": "test@example.com"}}

    def test_static_condition_method(self):
        """Test static condition method passes through."""
        cond = {"status": {"is": "active"}}
        result = LogicalOperator.condition(cond)

        assert result == cond

    def test_aliases(self):
        """Test method aliases."""
        cond = FieldCondition("status")
        cond.equals("active")

        # Using aliases
        result1 = LogicalOperator.and_group([LogicalOperator.Condition(cond)])
        result2 = LogicalOperator.And([LogicalOperator.Condition(cond)])

        assert result1.to_dict() == result2.to_dict()
