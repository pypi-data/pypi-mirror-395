"""Auth API for GAuth SDK."""

from typing import TYPE_CHECKING

from .endpoints import ENDPOINT_AUTH_LOGIN, ENDPOINT_AUTH_REFRESH
from .models import TokenClaims, TokenResponse

if TYPE_CHECKING:
    from .client import Client


class AuthAPI:
    """Provides methods for authentication operations."""

    def __init__(self, client: "Client"):
        self._client = client

    def login(self, email: str, password: str) -> TokenResponse:
        """
        Authenticate a user with email and password.

        Note: Requires tenant_id to be set on the client.

        Args:
            email: User's email address
            password: User's password

        Returns:
            TokenResponse with access_token and refresh_token
        """
        response = self._client._request(
            method="POST",
            path=ENDPOINT_AUTH_LOGIN,
            json={"email": email, "password": password},
        )
        data = self._client._parse_response(response)
        return TokenResponse.from_dict(data)

    def refresh_token(self, refresh_token: str) -> TokenResponse:
        """
        Refresh an access token using a refresh token.

        Note: Requires tenant_id to be set on the client.

        Args:
            refresh_token: The refresh token

        Returns:
            TokenResponse with new access_token and refresh_token
        """
        response = self._client._request(
            method="POST",
            path=ENDPOINT_AUTH_REFRESH,
            json={"refreshToken": refresh_token},
        )
        data = self._client._parse_response(response)
        return TokenResponse.from_dict(data)

    def validate_token(self, token: str) -> TokenClaims:
        """
        Validate a JWT token.

        Args:
            token: The JWT token to validate

        Returns:
            TokenClaims with the validated token information
        """
        return self._client.validate_token(token)
