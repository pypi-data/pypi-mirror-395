"""GAuth SDK - Python client for GAuth API."""

from .auth import AuthAPI
from .client import Client
from .errors import APIError
from .models import (
    ListUsersResponse,
    Paging,
    Session,
    TokenClaims,
    TokenResponse,
    User,
)
from .users import UsersAPI

__version__ = "0.3.0"

__all__ = [
    # Main client
    "Client",
    # API services
    "UsersAPI",
    "AuthAPI",
    # Models
    "User",
    "Session",
    "Paging",
    "TokenResponse",
    "TokenClaims",
    "ListUsersResponse",
    # Errors
    "APIError",
]
