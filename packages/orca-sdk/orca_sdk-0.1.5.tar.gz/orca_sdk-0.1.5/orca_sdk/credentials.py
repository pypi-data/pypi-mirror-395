import os
from datetime import datetime
from typing import Literal, NamedTuple

import httpx
from httpx import ConnectError, Headers, HTTPTransport
from typing_extensions import deprecated

from .async_client import OrcaAsyncClient
from .client import OrcaClient

Scope = Literal["ADMINISTER", "PREDICT"]
"""
The scopes of an API key.

- `ADMINISTER`: Can do anything, including creating and deleting organizations, models, and API keys.
- `PREDICT`: Can only call model.predict and perform CRUD operations on predictions.
"""


class ApiKeyInfo:
    """
    Information about an API key

    Note:
        The value of the API key is only available at creation time.

    Attributes:
        name: Unique name of the API key
        created_at: When the API key was created
        scopes: The scopes of the API key
    """

    name: str
    created_at: datetime
    scopes: set[Scope]

    def __init__(self, name: str, created_at: datetime, scopes: set[Scope]):
        self.name = name
        self.created_at = created_at
        self.scopes = scopes

    def __repr__(self) -> str:
        return "ApiKey({ " + f"name: '{self.name}', scopes: <{'|'.join(self.scopes)}>" + "})"


class OrcaCredentials:
    """
    Class for managing Orca API credentials
    """

    @staticmethod
    def is_authenticated() -> bool:
        """
        Check if you are authenticated to interact with the Orca API

        Returns:
            True if you are authenticated, False otherwise
        """
        client = OrcaClient._resolve_client()
        try:
            return client.GET("/auth")
        except ValueError as e:
            if "Invalid API key" in str(e):
                return False
            raise e

    @staticmethod
    def is_healthy() -> bool:
        """
        Check whether the API is healthy

        Returns:
            True if the API is healthy, False otherwise
        """
        client = OrcaClient._resolve_client()
        try:
            # we don't want a retry transport here, so we use httpx directly
            httpx.get(f"{client.base_url}/check/healthy")
        except Exception:
            return False
        return True

    @staticmethod
    def list_api_keys() -> list[ApiKeyInfo]:
        """
        List all API keys that have been created for your org

        Returns:
            A list of named tuples, with the name and creation date time of the API key
        """
        client = OrcaClient._resolve_client()
        return [
            ApiKeyInfo(
                name=api_key["name"],
                created_at=datetime.fromisoformat(api_key["created_at"]),
                scopes=set(api_key["scope"]),
            )
            for api_key in client.GET("/auth/api_key")
        ]

    @staticmethod
    def create_api_key(name: str, scopes: set[Scope] = {"ADMINISTER"}) -> str:
        """
        Create a new API key with the given name and scopes

        Params:
            name: The name of the API key
            scopes: The scopes of the API key

        Returns:
            The secret value of the API key. Make sure to save this value as it will not be shown again.
        """
        client = OrcaClient._resolve_client()
        res = client.POST(
            "/auth/api_key",
            json={"name": name, "scope": list(scopes)},
        )
        return res["api_key"]

    @staticmethod
    def revoke_api_key(name: str) -> None:
        """
        Delete an API key

        Params:
            name: The name of the API key to delete

        Raises:
            ValueError: if the API key is not found
        """
        client = OrcaClient._resolve_client()
        client.DELETE("/auth/api_key/{name_or_id}", params={"name_or_id": name})

    # TODO: remove deprecated methods after 2026-01-01

    @deprecated("Use `OrcaClient.api_key` instead")
    @staticmethod
    def set_api_key(api_key: str, check_validity: bool = True):
        """
        Set the API key to use for authenticating with the Orca API

        Note:
            The API key can also be provided by setting the `ORCA_API_KEY` environment variable

        Params:
            api_key: The API key to set
            check_validity: Whether to check if the API key is valid and raise an error otherwise

        Raises:
            ValueError: if the API key is invalid and `check_validity` is True
        """
        sync_client = OrcaClient._resolve_client()
        sync_client.api_key = api_key
        if check_validity:
            sync_client.GET("/auth")

        async_client = OrcaAsyncClient._resolve_client()
        async_client.api_key = api_key

    @deprecated("Use `OrcaClient.base_url` instead")
    @staticmethod
    def get_api_url() -> str:
        """
        Get the base URL of the Orca API that is currently being used
        """
        client = OrcaClient._resolve_client()
        return str(client.base_url)

    @deprecated("Use `OrcaClient.base_url` instead")
    @staticmethod
    def set_api_url(url: str, check_validity: bool = True):
        """
        Set the base URL for the Orca API

        Args:
            url: The base URL to set
            check_validity: Whether to check if there is an API running at the given base URL

        Raises:
            ValueError: if there is no healthy API running at the given base URL and `check_validity` is True
        """
        # check if the base url is reachable before setting it
        if check_validity:
            try:
                httpx.get(url, timeout=1)
            except ConnectError as e:
                raise ValueError(f"No API found at {url}") from e

        sync_client = OrcaClient._resolve_client()
        sync_client.base_url = url

        async_client = OrcaAsyncClient._resolve_client()
        async_client.base_url = url

        # check if the api passes the health check
        if check_validity:
            OrcaCredentials.is_healthy()

    @deprecated("Use `OrcaClient.headers` instead")
    @staticmethod
    def set_api_headers(headers: dict[str, str]):
        """
        Add or override default HTTP headers for all Orca API requests.

        Params:
            headers: Mapping of header names to their string values

        Notes:
            New keys are merged into the existing headers, this will overwrite headers with the
            same name, but leave other headers untouched.
        """
        sync_client = OrcaClient._resolve_client()
        sync_client.headers.update(Headers(headers))

        async_client = OrcaAsyncClient._resolve_client()
        async_client.headers.update(Headers(headers))
