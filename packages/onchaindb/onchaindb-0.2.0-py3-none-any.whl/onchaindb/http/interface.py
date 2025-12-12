"""
HTTP client interface for OnChainDB SDK.

Defines the protocol for HTTP clients that can be used with the SDK.
"""

from typing import Dict, Any, Protocol, runtime_checkable


@runtime_checkable
class HttpClientInterface(Protocol):
    """
    Protocol defining the interface for HTTP clients.

    This allows users to provide their own HTTP client implementation
    if they prefer a different library than httpx.
    """

    def post(self, url: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Send a POST request with JSON data.

        Args:
            url: The URL to send the request to.
            data: The JSON data to send in the request body.

        Returns:
            The JSON response as a dictionary.

        Raises:
            HttpException: If the request fails.
        """
        ...

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
        ...

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
        ...
