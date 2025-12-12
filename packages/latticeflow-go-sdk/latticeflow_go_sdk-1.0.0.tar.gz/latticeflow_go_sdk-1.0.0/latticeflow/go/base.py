from __future__ import annotations

from latticeflow.go._generated.client import Client as _Client


class BaseClient:
    def __init__(
        self, base_url: str, api_key: str | None, verify_ssl: bool = True
    ) -> None:
        """Base API Client.

        Args:
            base_url: The base URL for the API, all requests are made to a relative path to this URL
            api_key: The API key to use for authentication (`None` if no authentication)
            verify_ssl: Whether to verify the SSL certificate of the API server. This should be True in production, but can be set to False for testing purposes.
        """
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.verify_ssl = verify_ssl

    def get_client(self) -> _Client:
        return _Client(
            base_url=f"{self.base_url}/api",
            headers={"X-LatticeFlow-API-Key": self.api_key} if self.api_key else {},
            verify_ssl=self.verify_ssl,
        )
