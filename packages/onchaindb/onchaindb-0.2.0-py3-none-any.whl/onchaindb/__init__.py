"""
OnChainDB Python SDK

A Python SDK for OnChainDB - a decentralized database built on Celestia blockchain.
Provides a fluent, Prisma-like interface for querying and storing data.

Example:
    from onchaindb import OnChainDBClient

    client = OnChainDBClient(
        endpoint="https://api.onchaindb.io",
        app_id="your-app-id",
        app_key="your-app-key",
        user_key="optional-user-key"  # Optional: enables Auto-Pay
    )

    # Find a single user
    user = client.find_unique("users", {"email": "john@example.com"})

    # Find multiple users
    active_users = client.find_many("users", {"status": "active"}, limit=10)

    # Use the query builder for complex queries
    results = (client.query_builder()
        .collection("users")
        .where_field("status").equals("active")
        .where_field("age").greater_than(18)
        .select_all()
        .limit(10)
        .order_by("created_at", "desc")
        .execute())
"""

from .client import OnChainDBClient
from .exceptions import (
    OnChainDBException,
    QueryException,
    StoreException,
    TaskTimeoutException,
    HttpException,
    PaymentRequiredException,
)
from .query import (
    QueryBuilder,
    LogicalOperator,
    FieldCondition,
    ConditionBuilder,
    ConditionFieldBuilder,
    SelectionBuilder,
    JoinBuilder,
    GroupByQueryBuilder,
    WhereClause,
)
from .http import HttpClient, HttpClientInterface
from .types import (
    # X402 Payment Types
    X402PaymentRequirement,
    X402Quote,
    # Pricing Types
    PricingQuoteRequest,
    PricingQuoteResponse,
    CreatorPremium,
    # Collection Schema Types
    SimpleFieldDefinition,
    SimpleCollectionSchema,
    ReadPricing,
    IndexResult,
    CreateCollectionResult,
    SyncIndexResult,
    SyncCollectionResult,
    # Materialized Views Types
    MaterializedView,
    ViewInfo,
    # Store/Query Types
    StoreResult,
    TaskInfo,
    QueryResult,
)

__version__ = "0.1.0"

__all__ = [
    # Main client
    "OnChainDBClient",
    # Exceptions
    "OnChainDBException",
    "QueryException",
    "StoreException",
    "TaskTimeoutException",
    "HttpException",
    "PaymentRequiredException",
    # Query building
    "QueryBuilder",
    "LogicalOperator",
    "FieldCondition",
    "ConditionBuilder",
    "ConditionFieldBuilder",
    "SelectionBuilder",
    "JoinBuilder",
    "GroupByQueryBuilder",
    "WhereClause",
    # HTTP
    "HttpClient",
    "HttpClientInterface",
    # Types
    "X402PaymentRequirement",
    "X402Quote",
    "PricingQuoteRequest",
    "PricingQuoteResponse",
    "CreatorPremium",
    "SimpleFieldDefinition",
    "SimpleCollectionSchema",
    "ReadPricing",
    "IndexResult",
    "CreateCollectionResult",
    "SyncIndexResult",
    "SyncCollectionResult",
    "MaterializedView",
    "ViewInfo",
    "StoreResult",
    "TaskInfo",
    "QueryResult",
]
