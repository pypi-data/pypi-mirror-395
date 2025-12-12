"""
OnChainDB Client - Main entry point for interacting with OnChainDB.

Provides a Prisma-like interface for querying and storing data
in the decentralized database built on Celestia blockchain.
"""

import time
from typing import Any, Dict, List, Optional

from .query.builder import QueryBuilder
from .http.client import HttpClient
from .http.interface import HttpClientInterface
from .exceptions import OnChainDBException, StoreException, TaskTimeoutException


class OnChainDBClient:
    """
    Main client for interacting with OnChainDB.

    Provides methods for querying, storing, and managing data in OnChainDB
    with built-in support for blockchain confirmation polling.

    Example:
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

        # Store data
        result = client.store(
            collection="users",
            data=[{"id": "user_1", "name": "Alice", "email": "alice@example.com"}],
            payment_proof={"payment_tx_hash": "...", "amount_utia": 10000}
        )
    """

    def __init__(
        self,
        endpoint: str,
        app_id: str,
        app_key: str,
        user_key: Optional[str] = None,
        http_client: Optional[HttpClientInterface] = None,
    ):
        """
        Initialize the OnChainDB client.

        Args:
            endpoint: The OnChainDB API endpoint URL.
            app_id: Your application ID.
            app_key: Your application API key (required for authentication).
            user_key: Optional user key for Auto-Pay functionality.
            http_client: Optional custom HTTP client implementation.
        """
        self._endpoint = endpoint.rstrip("/")
        self._app_id = app_id
        self._app_key = app_key
        self._user_key = user_key

        # Build default headers for authentication
        headers = {
            "Content-Type": "application/json",
            "X-App-Key": app_key,
        }

        if user_key is not None:
            headers["X-User-Key"] = user_key

        self._http_client = http_client or HttpClient(headers)

    def query_builder(self) -> QueryBuilder:
        """
        Create a new query builder instance.

        Returns:
            A QueryBuilder for constructing queries.

        Example:
            results = (client.query_builder()
                .collection("users")
                .where_field("status").equals("active")
                .limit(10)
                .execute())
        """
        return QueryBuilder(self._http_client, self._endpoint, self._app_id)

    def find_unique(
        self,
        collection: str,
        where: Dict[str, Any],
    ) -> Optional[Dict[str, Any]]:
        """
        Find a single document by query.

        Returns the latest record by metadata (updatedAt or createdAt).
        This is similar to Prisma's findUnique method.

        Args:
            collection: The collection name.
            where: Query conditions as field-value pairs.

        Returns:
            The matching document, or None if not found.

        Example:
            user = client.find_unique("users", {"email": "john@example.com"})
        """
        query = self.query_builder().collection(collection)

        for field, value in where.items():
            query = query.where_field(field).equals(value)

        return query.select_all().execute_unique()

    def find_many(
        self,
        collection: str,
        where: Optional[Dict[str, Any]] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> List[Dict[str, Any]]:
        """
        Find multiple documents by query.

        Args:
            collection: The collection name.
            where: Optional query conditions as field-value pairs.
            limit: Maximum number of records to return.
            offset: Number of records to skip (for pagination).

        Returns:
            List of matching documents.

        Example:
            active_users = client.find_many(
                "users",
                {"status": "active"},
                limit=10,
                offset=0
            )
        """
        query = self.query_builder().collection(collection)

        if where:
            for field, value in where.items():
                query = query.where_field(field).equals(value)

        if limit is not None:
            query = query.limit(limit)

        if offset is not None:
            query = query.offset(offset)

        response = query.select_all().execute()
        return response.get("records", [])

    def count_documents(
        self,
        collection: str,
        where: Optional[Dict[str, Any]] = None,
    ) -> int:
        """
        Count documents matching criteria.

        Args:
            collection: The collection name.
            where: Optional query conditions as field-value pairs.

        Returns:
            The number of matching documents.

        Example:
            count = client.count_documents("users", {"status": "active"})
        """
        query = self.query_builder().collection(collection)

        if where:
            for field, value in where.items():
                query = query.where_field(field).equals(value)

        return query.count()

    def store(
        self,
        collection: str,
        data: List[Dict[str, Any]],
        payment_proof: Dict[str, Any],
        wait_for_confirmation: bool = True,
        poll_interval_ms: int = 2000,
        max_wait_time_ms: int = 600000,
    ) -> Dict[str, Any]:
        """
        Store documents in a collection.

        By default, waits for blockchain confirmation before returning.
        The store operation is asynchronous - it returns a ticket_id that
        must be polled until the transaction is confirmed on the blockchain.

        Args:
            collection: The collection name.
            data: List of documents to store.
            payment_proof: Payment proof for the transaction.
            wait_for_confirmation: Whether to wait for blockchain confirmation.
            poll_interval_ms: Polling interval in milliseconds (default: 2000).
            max_wait_time_ms: Maximum wait time in milliseconds (default: 600000 = 10 min).

        Returns:
            The storage result including Celestia height and other metadata.

        Raises:
            StoreException: If the store operation fails.
            TaskTimeoutException: If the task times out.

        Example:
            result = client.store(
                collection="users",
                data=[{"id": "user_1", "name": "Alice"}],
                payment_proof={"payment_tx_hash": "...", "amount_utia": 10000}
            )
        """
        # Build root in format app_id::collection
        root = f"{self._app_id}::{collection}"

        payload = {
            "root": root,
            "data": data,
            **payment_proof,
        }

        url = f"{self._endpoint}/store"

        try:
            response = self._http_client.post(url, payload)

            # Check if we got an async response with ticket_id
            if "ticket_id" in response and wait_for_confirmation:
                ticket_id = response["ticket_id"]

                # Poll for task completion
                task_info = self.wait_for_task_completion(
                    ticket_id,
                    poll_interval_ms,
                    max_wait_time_ms,
                )

                # Extract the actual storage result from the completed task
                if "result" in task_info:
                    return task_info["result"]

                return task_info

            return response

        except OnChainDBException:
            raise
        except Exception as e:
            raise StoreException(f"Store operation failed: {str(e)}") from e

    def store_blob(
        self,
        collection: str,
        blob_data: bytes,
        payment_proof: Dict[str, Any],
        filename: Optional[str] = None,
        content_type: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
        wait_for_confirmation: bool = True,
        poll_interval_ms: int = 2000,
        max_wait_time_ms: int = 600000,
    ) -> Dict[str, Any]:
        """
        Store a binary blob (image, file, etc.) on Celestia.

        Args:
            collection: The collection name for blobs.
            blob_data: Binary data to store.
            payment_proof: Payment proof for the transaction.
            filename: Optional filename for the blob.
            content_type: Optional MIME type (auto-detected from filename if not provided).
            metadata: Optional additional metadata.
            wait_for_confirmation: Whether to wait for blockchain confirmation.
            poll_interval_ms: Polling interval in milliseconds.
            max_wait_time_ms: Maximum wait time in milliseconds.

        Returns:
            The storage result including blob_id and Celestia metadata.

        Example:
            with open("image.png", "rb") as f:
                result = client.store_blob(
                    collection="images",
                    blob_data=f.read(),
                    payment_proof={"payment_tx_hash": "...", "amount_utia": 50000},
                    filename="image.png"
                )
            print(f"Blob ID: {result['blob_id']}")
        """
        import io

        url = f"{self._endpoint}/api/apps/{self._app_id}/blobs/{collection}"

        # Prepare multipart form data
        files = {
            "blob": (filename or "blob", io.BytesIO(blob_data), content_type or "application/octet-stream")
        }

        form_data = {
            "payment_tx_hash": payment_proof.get("payment_tx_hash", ""),
            "user_address": payment_proof.get("user_address", ""),
            "broker_address": payment_proof.get("broker_address", ""),
            "amount_utia": str(payment_proof.get("amount_utia", 0)),
        }

        if metadata:
            import json
            form_data["metadata"] = json.dumps(metadata)

        try:
            response = self._http_client.post_multipart(url, files, form_data)

            # Check if we got an async response with ticket_id
            if "ticket_id" in response and wait_for_confirmation:
                ticket_id = response["ticket_id"]
                blob_id = response.get("blob_id")

                # Poll for task completion
                task_info = self.wait_for_task_completion(
                    ticket_id,
                    poll_interval_ms,
                    max_wait_time_ms,
                )

                # Include blob_id in result
                result = task_info.get("result", task_info)
                if blob_id and "blob_id" not in result:
                    result["blob_id"] = blob_id

                return result

            return response

        except OnChainDBException:
            raise
        except Exception as e:
            raise StoreException(f"Blob store operation failed: {str(e)}") from e

    def get_blob_url(self, collection: str, blob_id: str) -> str:
        """
        Get the URL to retrieve a blob.

        Args:
            collection: The collection name.
            blob_id: The blob ID.

        Returns:
            The URL to fetch the blob.
        """
        return f"{self._endpoint}/api/apps/{self._app_id}/blobs/{collection}/{blob_id}"

    def get_pricing_quote(
        self,
        collection: str,
        operation_type: str = "write",
        size_kb: int = 1,
    ) -> Dict[str, Any]:
        """
        Get pricing quote for an operation.

        Args:
            collection: The collection name.
            operation_type: "write" or "read".
            size_kb: Size in KB for the operation.

        Returns:
            Pricing quote with total_cost, total_cost_tia, etc.

        Example:
            quote = client.get_pricing_quote("images", "write", 100)
            cost_utia = int(quote["total_cost_tia"] * 1_000_000)
        """
        url = f"{self._endpoint}/api/pricing/quote"

        payload = {
            "app_id": self._app_id,
            "operation_type": operation_type,
            "size_kb": size_kb,
            "collection": collection,
        }

        return self._http_client.post(url, payload)

    def get_task_status(self, ticket_id: str) -> Dict[str, Any]:
        """
        Get task status by ticket ID.

        Args:
            ticket_id: The ticket ID returned from async operations.

        Returns:
            Task info including status, result, etc.

        Example:
            task_info = client.get_task_status(ticket_id)
            print(f"Status: {task_info['status']}")
        """
        url = f"{self._endpoint}/task/{ticket_id}"
        return self._http_client.get(url)

    def wait_for_task_completion(
        self,
        ticket_id: str,
        poll_interval_ms: int = 2000,
        max_wait_time_ms: int = 600000,
    ) -> Dict[str, Any]:
        """
        Wait for a task to complete by polling.

        Polls the task status until it completes, fails, or times out.

        Args:
            ticket_id: The ticket ID to poll.
            poll_interval_ms: Polling interval in milliseconds (default: 2000).
            max_wait_time_ms: Maximum wait time in milliseconds (default: 600000 = 10 min).

        Returns:
            The completed task info.

        Raises:
            OnChainDBException: If the task fails.
            TaskTimeoutException: If the task times out.

        Example:
            result = client.wait_for_task_completion(
                ticket_id,
                poll_interval_ms=1000,
                max_wait_time_ms=300000
            )
        """
        start_time = time.time() * 1000
        poll_interval_sec = poll_interval_ms / 1000

        while (time.time() * 1000) - start_time < max_wait_time_ms:
            try:
                task_info = self.get_task_status(ticket_id)
                status = task_info.get("status")

                # Handle string status
                if isinstance(status, str):
                    if status == "Completed":
                        return task_info

                    if "error" in status.lower() or "failed" in status.lower():
                        raise OnChainDBException(f"Task failed: {status}")

                # Handle object status like {"Failed": {"error": "..."}}
                elif isinstance(status, dict):
                    if "Failed" in status:
                        error = status["Failed"].get("error", "Unknown error")
                        raise OnChainDBException(f"Task failed: {error}")

                time.sleep(poll_interval_sec)

            except OnChainDBException:
                raise
            except Exception:
                # Continue polling on transient errors
                time.sleep(poll_interval_sec)

        raise TaskTimeoutException(
            f"Task {ticket_id} timed out after {max_wait_time_ms / 1000} seconds"
        )

    @property
    def endpoint(self) -> str:
        """Get the endpoint URL."""
        return self._endpoint

    @property
    def app_id(self) -> str:
        """Get the application ID."""
        return self._app_id

    @property
    def app_key(self) -> str:
        """Get the application key."""
        return self._app_key

    @property
    def user_key(self) -> Optional[str]:
        """Get the user key (if set)."""
        return self._user_key

    # Aliases for property access (for backwards compatibility)
    def get_endpoint(self) -> str:
        """Get the endpoint URL."""
        return self._endpoint

    def get_app_id(self) -> str:
        """Get the application ID."""
        return self._app_id

    def get_app_key(self) -> str:
        """Get the application key."""
        return self._app_key

    def get_user_key(self) -> Optional[str]:
        """Get the user key (if set)."""
        return self._user_key

    # ========================================================================
    # Collection Schema Methods
    # ========================================================================

    # Base fields that are automatically indexed when use_base_fields is True
    _BASE_FIELDS: Dict[str, Dict[str, Any]] = {
        "id": {"type": "string", "index": True},
        "createdAt": {"type": "date", "index": True},
        "updatedAt": {"type": "date", "index": True},
        "deletedAt": {"type": "date", "index": True},
    }

    def _get_default_index_type(self, field_type: str) -> str:
        """Get default index type for a field type."""
        return {
            "string": "string",
            "number": "number",
            "boolean": "boolean",
            "date": "date",
        }.get(field_type, "string")

    def create_collection(
        self,
        schema: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Create a collection with schema-defined indexes.

        Args:
            schema: Collection schema definition with:
                - name: Collection name
                - fields: Dict of field definitions (field_name -> {type, index?, indexType?, readPricing?})
                - use_base_fields: Whether to include base fields (default: True)

        Returns:
            Result with collection name, indexes list, success status, and warnings.

        Example:
            result = client.create_collection({
                "name": "users",
                "fields": {
                    "email": {"type": "string", "index": True},
                    "username": {"type": "string", "index": True},
                    "age": {"type": "number"},
                    "address.city": {"type": "string", "index": True}
                },
                "use_base_fields": True
            })
        """
        result: Dict[str, Any] = {
            "collection": schema["name"],
            "indexes": [],
            "success": True,
            "warnings": [],
        }

        # Merge base fields if enabled (default: True)
        all_fields: Dict[str, Dict[str, Any]] = {}
        use_base_fields = schema.get("use_base_fields", True)

        if use_base_fields:
            all_fields.update(self._BASE_FIELDS)

        all_fields.update(schema.get("fields", {}))

        # Create indexes only for fields marked with index: True
        for field_name, field_def in all_fields.items():
            if not field_def.get("index"):
                continue

            index_type = field_def.get("indexType") or self._get_default_index_type(field_def["type"])

            index_request: Dict[str, Any] = {
                "name": f"{schema['name']}_{field_name}_idx",
                "collection": schema["name"],
                "field_name": field_name,
                "index_type": index_type,
                "store_values": True,
            }

            read_pricing = field_def.get("readPricing")
            if read_pricing:
                pricing_model = "per_kb" if read_pricing.get("pricePerKb") else "per_access"
                index_request["read_price_config"] = {
                    "pricing_model": pricing_model,
                    "price_per_access_tia": read_pricing.get("pricePerAccess"),
                    "price_per_kb_tia": read_pricing.get("pricePerKb"),
                }

            try:
                url = f"{self._endpoint}/api/apps/{self._app_id}/indexes"
                response = self._http_client.post(url, index_request)

                status = "updated" if response.get("updated") else "created"

                if response.get("_warning"):
                    result["warnings"].append(f"{field_name}: {response['_warning']}")

                result["indexes"].append({
                    "field": field_name,
                    "type": index_type,
                    "status": status,
                })
            except Exception as e:
                result["indexes"].append({
                    "field": field_name,
                    "type": index_type,
                    "status": "failed",
                    "error": str(e),
                })
                result["success"] = False

        return result

    def sync_collection(
        self,
        schema: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Sync collection schema - applies diff on indexes.

        Compares the provided schema with existing indexes and:
        - Creates missing indexes for new fields with index: True
        - Removes indexes for fields no longer in schema or without index: True
        - Leaves unchanged indexes intact

        Args:
            schema: Updated collection schema definition.

        Returns:
            Result with created, removed, unchanged indexes, success status, and errors.

        Example:
            result = client.sync_collection({
                "name": "users",
                "fields": {
                    "email": {"type": "string", "index": True},
                    "age": {"type": "number", "index": True}  # new index
                }
            })
            print(f"Created: {result['created']}")
            print(f"Removed: {result['removed']}")
        """
        result: Dict[str, Any] = {
            "collection": schema["name"],
            "created": [],
            "removed": [],
            "unchanged": [],
            "success": True,
            "errors": [],
        }

        # Get existing indexes for this collection
        existing_indexes: Dict[str, Dict[str, str]] = {}
        try:
            url = f"{self._endpoint}/api/apps/{self._app_id}/collections/{schema['name']}/indexes"
            response = self._http_client.get(url)
            indexes = response.get("indexes") or response or []

            for idx in indexes:
                existing_indexes[idx["field_name"]] = {
                    "type": idx["index_type"],
                    "name": idx["name"],
                }
        except Exception:
            # Collection might not exist yet, that's okay
            pass

        # Merge base fields if enabled (default: True)
        all_fields: Dict[str, Dict[str, Any]] = {}
        use_base_fields = schema.get("use_base_fields", True)

        if use_base_fields:
            all_fields.update(self._BASE_FIELDS)

        all_fields.update(schema.get("fields", {}))

        # Build set of desired indexed fields
        desired_indexed_fields: Dict[str, Dict[str, Any]] = {}
        for field_name, field_def in all_fields.items():
            if field_def.get("index"):
                desired_indexed_fields[field_name] = field_def

        # Find indexes to create (in desired but not existing)
        for field_name, field_def in desired_indexed_fields.items():
            if field_name not in existing_indexes:
                index_type = field_def.get("indexType") or self._get_default_index_type(field_def["type"])

                index_request: Dict[str, Any] = {
                    "name": f"{schema['name']}_{field_name}_idx",
                    "collection": schema["name"],
                    "field_name": field_name,
                    "index_type": index_type,
                    "store_values": True,
                }

                read_pricing = field_def.get("readPricing")
                if read_pricing:
                    pricing_model = "per_kb" if read_pricing.get("pricePerKb") else "per_access"
                    index_request["read_price_config"] = {
                        "pricing_model": pricing_model,
                        "price_per_access_tia": read_pricing.get("pricePerAccess"),
                        "price_per_kb_tia": read_pricing.get("pricePerKb"),
                    }

                try:
                    url = f"{self._endpoint}/api/apps/{self._app_id}/indexes"
                    self._http_client.post(url, index_request)
                    result["created"].append({"field": field_name, "type": index_type})
                except Exception as e:
                    result["errors"].append(f"Failed to create index on {field_name}: {str(e)}")
                    result["success"] = False

        # Find indexes to remove (existing but not in desired)
        for field_name, existing in existing_indexes.items():
            if field_name not in desired_indexed_fields:
                try:
                    # Index ID format: {collection}_{field_name}_index
                    index_id = f"{schema['name']}_{field_name}_index"
                    url = f"{self._endpoint}/api/apps/{self._app_id}/indexes/{index_id}"
                    self._http_client.delete(url)
                    result["removed"].append({"field": field_name, "type": existing["type"]})
                except Exception as e:
                    result["errors"].append(f"Failed to remove index on {field_name}: {str(e)}")
                    result["success"] = False

        # Track unchanged indexes
        for field_name, existing in existing_indexes.items():
            if field_name in desired_indexed_fields:
                result["unchanged"].append({"field": field_name, "type": existing["type"]})

        return result

    # ========================================================================
    # Materialized Views Methods
    # ========================================================================

    def create_view(
        self,
        name: str,
        source_collections: List[str],
        query: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Create a new materialized view.

        Materialized views are pre-computed query results that update automatically
        when source data changes. Great for complex aggregations and joins.

        Args:
            name: Unique name for the view.
            source_collections: Collections this view depends on.
            query: Query definition for the view.

        Returns:
            Created view definition.

        Example:
            view = client.create_view(
                name="top_sellers",
                source_collections=["products", "orders"],
                query={
                    "select": ["id", "name", "price", "sales_count"],
                    "where": {"status": "active"},
                    "order_by": {"sales_count": "desc"},
                    "limit": 100
                }
            )
        """
        payload = {
            "name": name,
            "source_collections": source_collections,
            "query": query,
        }

        url = f"{self._endpoint}/api/apps/{self._app_id}/views"
        return self._http_client.post(url, payload)

    def list_views(self) -> List[Dict[str, Any]]:
        """
        List all materialized views for the app.

        Returns:
            List of view info objects with name, source_collections, and created_at.

        Example:
            views = client.list_views()
            for view in views:
                print(f"{view['name']}: {view['source_collections']}")
        """
        url = f"{self._endpoint}/api/apps/{self._app_id}/views"
        response = self._http_client.get(url)
        return response.get("views", response)

    def get_view(self, name: str) -> Dict[str, Any]:
        """
        Get a specific materialized view by name.

        Args:
            name: View name.

        Returns:
            View definition with name, source_collections, query, and created_at.

        Example:
            view = client.get_view("top_sellers")
            print(f"Query: {view['query']}")
        """
        url = f"{self._endpoint}/api/apps/{self._app_id}/views/{name}"
        return self._http_client.get(url)

    def delete_view(self, name: str) -> Dict[str, Any]:
        """
        Delete a materialized view.

        Args:
            name: View name.

        Returns:
            Result with success status and message.

        Example:
            result = client.delete_view("old_view")
            print(f"Deleted: {result['success']}")
        """
        url = f"{self._endpoint}/api/apps/{self._app_id}/views/{name}"
        return self._http_client.delete(url)

    def refresh_view(self, name: str) -> Dict[str, Any]:
        """
        Refresh/rebuild a materialized view.

        Forces the view to recompute its results from the source collections.

        Args:
            name: View name.

        Returns:
            Result with success status and message.

        Example:
            result = client.refresh_view("top_sellers")
            print(f"Refreshed: {result['success']}")
        """
        url = f"{self._endpoint}/api/apps/{self._app_id}/views/{name}/refresh"
        return self._http_client.post(url, {})
