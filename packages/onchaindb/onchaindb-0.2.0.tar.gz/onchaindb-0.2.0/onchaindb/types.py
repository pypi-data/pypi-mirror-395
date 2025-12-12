"""
Type definitions for OnChainDB SDK.

These TypedDict classes provide IDE autocomplete and type checking support.
"""

from typing import TypedDict, List, Optional, Any, Dict


# ============================================================================
# X402 Payment Types
# ============================================================================

class X402PaymentRequirement(TypedDict, total=False):
    """A single payment requirement from x402 protocol."""
    kind: str  # "onchain" or "offchain"
    chain: str  # "celestia", "ethereum", etc.
    network: str  # "mainnet", "mocha-4", etc.
    asset: str  # "TIA", "ETH", etc.
    payTo: str  # Payment destination address
    maxAmountRequired: str  # Amount in smallest unit
    resource: str  # Resource being paid for
    scheme: str  # "exact" or "upto"
    quoteId: str  # Quote identifier
    expiresAt: str  # Expiration timestamp
    extra: Dict[str, Any]  # Additional metadata


class X402Quote(TypedDict, total=False):
    """Payment quote from x402 protocol."""
    paymentRequirements: List[X402PaymentRequirement]
    error: str


# ============================================================================
# Pricing Types
# ============================================================================

class PricingQuoteRequest(TypedDict, total=False):
    """Request for a pricing quote."""
    app_id: str
    operation_type: str  # "read" or "write"
    size_kb: int
    collection: str
    monthly_volume_kb: int
    data: Any  # Sample data for price index calculation


class CreatorPremium(TypedDict, total=False):
    """Creator premium breakdown in pricing."""
    premium_total: float
    premium_total_utia: int
    premium_type: str
    premium_amount: float
    creator_revenue: float
    creator_revenue_utia: int
    platform_revenue: float
    platform_revenue_utia: int
    revenue_split: str


class PricingQuoteResponse(TypedDict, total=False):
    """Response from pricing quote API."""
    type: str  # "write_quote_with_indexing" or "read_quote"
    # Base costs
    base_celestia_cost: float
    base_celestia_cost_utia: int
    broker_fee: float
    broker_fee_utia: int
    # Indexing costs per field
    indexing_costs: Dict[str, float]
    indexing_costs_utia: Dict[str, int]
    # Totals
    base_total_cost: float
    base_total_cost_utia: int
    total_cost: float
    total_cost_utia: int
    # Metadata
    indexed_fields_count: int
    request: PricingQuoteRequest
    monthly_volume_kb: int
    currency: str
    # Optional breakdowns
    creator_premium: CreatorPremium
    price: Any  # Price index breakdown


# ============================================================================
# Collection Schema Types
# ============================================================================

class ReadPricing(TypedDict, total=False):
    """Read pricing configuration for a field."""
    pricePerAccess: float
    pricePerKb: float


class SimpleFieldDefinition(TypedDict, total=False):
    """Field definition for collection schema."""
    type: str  # "string", "number", "boolean", "date", "object", "array"
    index: bool
    indexType: str  # "btree", "hash", "fulltext", "price"
    readPricing: ReadPricing


class SimpleCollectionSchema(TypedDict, total=False):
    """Collection schema for createCollection/syncCollection."""
    name: str
    fields: Dict[str, SimpleFieldDefinition]
    use_base_fields: bool  # defaults to True


class IndexResult(TypedDict, total=False):
    """Result of a single index operation."""
    field: str
    type: str
    status: str  # "created", "updated", "failed"
    error: str


class CreateCollectionResult(TypedDict):
    """Result of createCollection operation."""
    collection: str
    indexes: List[IndexResult]
    success: bool
    warnings: List[str]


class SyncIndexResult(TypedDict):
    """Result of a single index in sync operation."""
    field: str
    type: str


class SyncCollectionResult(TypedDict):
    """Result of syncCollection operation."""
    collection: str
    created: List[SyncIndexResult]
    removed: List[SyncIndexResult]
    unchanged: List[SyncIndexResult]
    success: bool
    errors: List[str]


# ============================================================================
# Materialized Views Types
# ============================================================================

class MaterializedView(TypedDict, total=False):
    """Materialized view definition."""
    name: str
    source_collections: List[str]
    query: Dict[str, Any]
    created_at: str


class ViewInfo(TypedDict):
    """Basic info about a materialized view."""
    name: str
    source_collections: List[str]
    created_at: str


# ============================================================================
# Store Types
# ============================================================================

class StoreResult(TypedDict, total=False):
    """Result of a store operation."""
    results: List[Dict[str, Any]]
    ticket_id: str
    status: str


class TaskInfo(TypedDict, total=False):
    """Task status information."""
    ticket_id: str
    status: str
    created_at: str
    updated_at: str
    operation_type: str
    user_address: str
    transaction_hash: str
    block_height: int
    result: Any
    progress_log: List[str]


# ============================================================================
# Query Types
# ============================================================================

class QueryResult(TypedDict):
    """Result of a query operation."""
    records: List[Dict[str, Any]]
    total: int
    page: int
    limit: int
