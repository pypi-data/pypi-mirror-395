"""
Default HTTP client implementation using httpx.
"""

from typing import Dict, Any, Optional
import httpx

from ..exceptions import HttpException, PaymentRequiredException


def _parse_402_response(response_data: Dict[str, Any]) -> PaymentRequiredException:
    """Parse a 402 Payment Required response into a PaymentRequiredException."""
    accepts = response_data.get("accepts", [])
    if accepts and len(accepts) > 0:
        accept = accepts[0]
        amount_str = accept.get("maxAmountRequired", "0")
        return PaymentRequiredException(
            message="Payment required",
            amount_utia=int(amount_str),
            pay_to=accept.get("payTo", ""),
            quote_id=accept.get("quoteId"),
            expires_at=accept.get("expiresAt"),
            resource=accept.get("resource"),
            description=accept.get("description"),
        )
    # Fallback if no accepts array
    return PaymentRequiredException(
        message="Payment required (no payment details provided)",
        amount_utia=0,
        pay_to="",
    )


class HttpClient:
    """
    Default HTTP client implementation using httpx.

    This is the default HTTP client used by OnChainDBClient if no custom
    client is provided.
    """

    def __init__(
        self,
        headers: Optional[Dict[str, str]] = None,
        timeout: float = 30.0,
    ):
        """
        Initialize the HTTP client.

        Args:
            headers: Default headers to include in all requests.
            timeout: Request timeout in seconds.
        """
        self._headers = headers or {}
        self._timeout = timeout
        self._client = httpx.Client(
            headers=self._headers,
            timeout=timeout,
        )

    def post(self, url: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Send a POST request with JSON data.

        Args:
            url: The URL to send the request to.
            data: The JSON data to send in the request body.

        Returns:
            The JSON response as a dictionary.

        Raises:
            PaymentRequiredException: If payment is required (402 status).
            HttpException: If the request fails.
        """
        try:
            response = self._client.post(url, json=data)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            # Handle 402 Payment Required specially
            if e.response.status_code == 402:
                try:
                    response_data = e.response.json()
                    raise _parse_402_response(response_data) from e
                except ValueError:
                    # Not valid JSON
                    raise PaymentRequiredException(
                        message="Payment required",
                        amount_utia=0,
                        pay_to="",
                    ) from e
            raise HttpException(
                f"HTTP error {e.response.status_code}: {e.response.text}",
                status_code=e.response.status_code,
            ) from e
        except httpx.RequestError as e:
            raise HttpException(f"Request failed: {str(e)}") from e

    def get(self, url: str) -> Dict[str, Any]:
        """
        Send a GET request.

        Args:
            url: The URL to send the request to.

        Returns:
            The JSON response as a dictionary.

        Raises:
            HttpException: If the request fails.
        """
        try:
            response = self._client.get(url)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            raise HttpException(
                f"HTTP error {e.response.status_code}: {e.response.text}",
                status_code=e.response.status_code,
            ) from e
        except httpx.RequestError as e:
            raise HttpException(f"Request failed: {str(e)}") from e

    def post_multipart(
        self,
        url: str,
        files: Dict[str, Any],
        data: Dict[str, str],
    ) -> Dict[str, Any]:
        """
        Send a POST request with multipart form data (for file uploads).

        Args:
            url: The URL to send the request to.
            files: Dictionary of files to upload. Format: {"field_name": (filename, file_obj, content_type)}
            data: Dictionary of form fields.

        Returns:
            The JSON response as a dictionary.

        Raises:
            PaymentRequiredException: If payment is required (402 status).
            HttpException: If the request fails.
        """
        try:
            # For multipart requests, we need a fresh client without Content-Type header
            # The persistent client has Content-Type: application/json which breaks multipart
            multipart_headers = {k: v for k, v in self._headers.items() if k.lower() != "content-type"}

            # Use a separate httpx request without the persistent client's headers
            with httpx.Client(timeout=self._timeout) as client:
                response = client.post(
                    url,
                    files=files,
                    data=data,
                    headers=multipart_headers,
                )
                response.raise_for_status()
                return response.json()
        except httpx.HTTPStatusError as e:
            # Handle 402 Payment Required specially
            if e.response.status_code == 402:
                try:
                    response_data = e.response.json()
                    raise _parse_402_response(response_data) from e
                except ValueError:
                    raise PaymentRequiredException(
                        message="Payment required",
                        amount_utia=0,
                        pay_to="",
                    ) from e
            raise HttpException(
                f"HTTP error {e.response.status_code}: {e.response.text}",
                status_code=e.response.status_code,
            ) from e
        except httpx.RequestError as e:
            raise HttpException(f"Request failed: {str(e)}") from e

    def delete(self, url: str) -> Dict[str, Any]:
        """
        Send a DELETE request.

        Args:
            url: The URL to send the request to.

        Returns:
            The JSON response as a dictionary.

        Raises:
            HttpException: If the request fails.
        """
        try:
            response = self._client.delete(url)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            raise HttpException(
                f"HTTP error {e.response.status_code}: {e.response.text}",
                status_code=e.response.status_code,
            ) from e
        except httpx.RequestError as e:
            raise HttpException(f"Request failed: {str(e)}") from e

    def close(self) -> None:
        """Close the HTTP client and release resources."""
        self._client.close()

    def __enter__(self) -> "HttpClient":
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Context manager exit - closes the client."""
        self.close()
