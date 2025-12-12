"""Main client for SEE URL SDK."""

from dataclasses import asdict
from typing import Any

from .exceptions import ValidationError
from .http_client import HttpClient
from .models import (
    CreateShortUrlRequest,
    CreateShortUrlResponse,
    UpdateShortUrlRequest,
    UpdateShortUrlResponse,
    DeleteShortUrlRequest,
    DeleteShortUrlResponse,
    DomainResponse,
    TagResponse,
)


class SeeClient:
    """
    Main client for interacting with the URL shortening service.

    This client provides methods to create, update, and delete short URLs,
    as well as retrieve available domains and tags.

    Example:
        import os
        
        api_key = os.getenv("SEE_API_KEY")
        async with SeeClient(api_key=api_key) as client:
            request = CreateShortUrlRequest(
                domain="s.ee",
                target_url="https://example.com/long/url"
            )
            response = await client.create_short_url(request)
            print(response.data)
    """

    def __init__(
        self,
        api_key: str,
        base_url: str = "https://s.ee/api",
        timeout: float = 30.0,
        max_retries: int = 3,
        proxy: str | None = None,
    ) -> None:
        """
        Initialize the SEE URL client.

        Args:
            api_key: Your API key for authentication
            base_url: Base URL of the API (default: https://s.ee/api)
            timeout: Request timeout in seconds (default: 30.0)
            max_retries: Maximum number of retries for failed requests (default: 3)
            proxy: Optional HTTP proxy URL (e.g., http://localhost:8080)

        Raises:
            ValidationError: If API key is empty or invalid
        """
        if not api_key:
            raise ValidationError("API key is required")

        self._http_client = HttpClient(
            base_url=base_url,
            api_key=api_key,
            timeout=timeout,
            max_retries=max_retries,
            proxy=proxy,
        )

    async def __aenter__(self) -> "SeeClient":
        """Async context manager entry."""
        await self._http_client.__aenter__()
        return self

    async def __aexit__(self, *args: Any) -> None:
        """Async context manager exit."""
        await self._http_client.__aexit__(*args)

    async def create_short_url(
        self, request: CreateShortUrlRequest
    ) -> CreateShortUrlResponse:
        """
        Create a new short URL.

        Args:
            request: The create short URL request containing domain, target URL, and optional parameters

        Returns:
            CreateShortUrlResponse: Response containing the created short URL details

        Raises:
            ValidationError: If target URL is invalid or domain is missing
            APIError: If the API request fails
        """
        # Validate target URL format
        if not request.target_url or not request.target_url.startswith(
            ("http://", "https://")
        ):
            raise ValidationError("Invalid URL: must start with http:// or https://")

        # Validate domain is provided
        if not request.domain:
            raise ValidationError("Domain is required")

        response = await self._http_client.post("/v1/shorten", json=asdict(request))
        return CreateShortUrlResponse.from_dict(response)

    async def update_short_url(
        self, request: UpdateShortUrlRequest
    ) -> UpdateShortUrlResponse:
        """
        Update an existing short URL.

        Args:
            request: The update short URL request containing domain, slug, and fields to update

        Returns:
            UpdateShortUrlResponse: Response indicating the update status

        Raises:
            NotFoundError: If the short URL is not found
            APIError: If the API request fails
        """
        response = await self._http_client.put(
            "/v1/shorten",
            json=asdict(request),
        )
        return UpdateShortUrlResponse.from_dict(response)

    async def delete_short_url(
        self, request: DeleteShortUrlRequest
    ) -> DeleteShortUrlResponse:
        """
        Delete a short URL.

        Args:
            request: The delete short URL request containing domain and slug

        Returns:
            DeleteShortUrlResponse: Response indicating the deletion status

        Raises:
            NotFoundError: If the short URL is not found
            APIError: If the API request fails
        """
        response = await self._http_client.delete("/v1/shorten", json=asdict(request))
        return DeleteShortUrlResponse.from_dict(response)

    async def get_domains(self) -> DomainResponse:
        """
        Get available domains for creating short URLs.

        Returns:
            DomainResponse: Response containing the list of available domains

        Raises:
            APIError: If the API request fails
        """
        response = await self._http_client.get("/v1/domains")
        return DomainResponse.from_dict(response)

    async def get_tags(self) -> TagResponse:
        """
        Get available tags for categorizing short URLs.

        Returns:
            TagResponse: Response containing the list of available tags

        Raises:
            APIError: If the API request fails
        """
        response = await self._http_client.get("/v1/tags")
        return TagResponse.from_dict(response)
