"""Main client for GAuth SDK."""

from typing import Any, Dict, Optional, Tuple, TypeVar

import requests

from .endpoints import (
    CONTENT_TYPE_JSON,
    ENDPOINT_API_AUTH_VALIDATE,
    HEADER_ACCEPT,
    HEADER_API_KEY,
    HEADER_AUTHORIZATION,
    HEADER_CONTENT_TYPE,
    HEADER_TENANT_ID,
)
from .errors import APIError
from .models import Paging, TokenClaims

T = TypeVar("T")

DEFAULT_BASE_URL = "http://localhost:3000"
DEFAULT_TIMEOUT = 30


class Client:
    """Main GAuth SDK client."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: str = DEFAULT_BASE_URL,
        tenant_id: Optional[str] = None,
        timeout: int = DEFAULT_TIMEOUT,
    ):
        """
        Initialize the GAuth client.

        Args:
            api_key: API key for authentication (X-API-Key header)
            base_url: Base URL for the API
            tenant_id: Tenant ID for multi-tenant auth operations
            timeout: Request timeout in seconds
        """
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.tenant_id = tenant_id
        self.timeout = timeout
        self._session = requests.Session()

        # Initialize API services (lazy import to avoid circular imports)
        from .auth import AuthAPI
        from .users import UsersAPI

        self.users = UsersAPI(self)
        self.auth = AuthAPI(self)

    def _build_headers(self, include_auth_token: Optional[str] = None) -> Dict[str, str]:
        """Build request headers."""
        headers = {
            HEADER_CONTENT_TYPE: CONTENT_TYPE_JSON,
            HEADER_ACCEPT: CONTENT_TYPE_JSON,
        }

        if self.api_key:
            headers[HEADER_API_KEY] = self.api_key

        if self.tenant_id:
            headers[HEADER_TENANT_ID] = self.tenant_id

        if include_auth_token:
            headers[HEADER_AUTHORIZATION] = f"Bearer {include_auth_token}"

        return headers

    def _request(
        self,
        method: str,
        path: str,
        json: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
        auth_token: Optional[str] = None,
    ) -> requests.Response:
        """Make an HTTP request."""
        url = f"{self.base_url}{path}"
        headers = self._build_headers(include_auth_token=auth_token)

        response = self._session.request(
            method=method,
            url=url,
            headers=headers,
            json=json,
            params=params,
            timeout=self.timeout,
        )

        return response

    def _parse_response(self, response: requests.Response) -> Any:
        """Parse API response and handle errors."""
        try:
            data = response.json()
        except ValueError:
            if response.status_code >= 400:
                raise APIError(
                    code=response.status_code,
                    message=response.text or "Unknown error",
                )
            return None

        if response.status_code >= 400:
            raise APIError.from_response(response.status_code, data)

        return data.get("data")

    def _parse_list_response(self, response: requests.Response) -> Tuple[Any, Optional[Paging]]:
        """Parse API response that includes pagination."""
        try:
            data = response.json()
        except ValueError:
            if response.status_code >= 400:
                raise APIError(
                    code=response.status_code,
                    message=response.text or "Unknown error",
                )
            return None, None

        if response.status_code >= 400:
            raise APIError.from_response(response.status_code, data)

        return data.get("data"), Paging.from_dict(data.get("paging"))

    def validate_token(self, token: str) -> TokenClaims:
        """
        Validate a JWT token and return the claims.

        Args:
            token: The JWT token to validate

        Returns:
            TokenClaims with the validated token information
        """
        response = self._request(
            method="GET",
            path=ENDPOINT_API_AUTH_VALIDATE,
            auth_token=token,
        )
        data = self._parse_response(response)
        return TokenClaims.from_dict(data)
