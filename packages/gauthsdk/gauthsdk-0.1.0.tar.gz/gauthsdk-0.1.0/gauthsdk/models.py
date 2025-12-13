"""Data models for GAuth SDK."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Generic, List, Optional, TypeVar

T = TypeVar("T")


@dataclass
class Paging:
    """Pagination information."""

    page: int = 1
    limit: int = 20
    total: int = 0
    total_pages: int = 0

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional["Paging"]:
        if not data:
            return None
        return cls(
            page=data.get("page", 1),
            limit=data.get("limit", 20),
            total=data.get("total", 0),
            total_pages=data.get("totalPages", 0),
        )


@dataclass
class User:
    """Represents a user in the system."""

    id: str
    first_name: str
    last_name: str
    role: str
    status: str
    email_verified: bool = False
    phone_verified: bool = False
    tenant_id: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    username: Optional[str] = None
    avatar: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def full_name(self) -> str:
        """Returns the user's full name."""
        return f"{self.first_name} {self.last_name}"

    @classmethod
    def from_dict(cls, data: dict) -> "User":
        return cls(
            id=data.get("id", ""),
            first_name=data.get("firstName", ""),
            last_name=data.get("lastName", ""),
            role=data.get("role", ""),
            status=data.get("status", ""),
            email_verified=data.get("emailVerified", False),
            phone_verified=data.get("phoneVerified", False),
            tenant_id=data.get("tenantId"),
            email=data.get("email"),
            phone=data.get("phone"),
            username=data.get("username"),
            avatar=data.get("avatar"),
            created_at=_parse_datetime(data.get("createdAt")),
            updated_at=_parse_datetime(data.get("updatedAt")),
        )


@dataclass
class Session:
    """Represents a user session."""

    id: str
    user_id: str
    identity_id: str
    type: str
    tenant_id: str
    exp_at: datetime
    user_agent: Optional[str] = None
    created_at: Optional[datetime] = None

    @classmethod
    def from_dict(cls, data: dict) -> "Session":
        return cls(
            id=data.get("id", ""),
            user_id=data.get("userId", ""),
            identity_id=data.get("identityId", ""),
            type=data.get("type", ""),
            tenant_id=data.get("tenantId", ""),
            exp_at=_parse_datetime(data.get("expAt")) or datetime.now(),
            user_agent=data.get("userAgent"),
            created_at=_parse_datetime(data.get("createdAt")),
        )


@dataclass
class TokenResponse:
    """Response from a login operation."""

    access_token: str
    refresh_token: str
    token_type: str
    expires_at: Optional[datetime] = None

    @classmethod
    def from_dict(cls, data: dict) -> "TokenResponse":
        return cls(
            access_token=data.get("accessToken", ""),
            refresh_token=data.get("refreshToken", ""),
            token_type=data.get("tokenType", "Bearer"),
            expires_at=_parse_datetime(data.get("expiresAt")),
        )


@dataclass
class TokenClaims:
    """JWT token claims."""

    sub: str
    tenant_id: str
    role: str
    email_verified: bool
    exp: int
    iat: int

    @classmethod
    def from_dict(cls, data: dict) -> "TokenClaims":
        return cls(
            sub=data.get("sub", ""),
            tenant_id=data.get("tenantId", ""),
            role=data.get("role", ""),
            email_verified=data.get("emailVerified", False),
            exp=data.get("exp", 0),
            iat=data.get("iat", 0),
        )


@dataclass
class ListUsersResponse:
    """Response containing a paginated list of users."""

    users: List[User] = field(default_factory=list)
    paging: Optional[Paging] = None


def _parse_datetime(value: Optional[str]) -> Optional[datetime]:
    """Parse an ISO datetime string."""
    if not value:
        return None
    try:
        # Handle various ISO formats
        if value.endswith("Z"):
            value = value[:-1] + "+00:00"
        return datetime.fromisoformat(value)
    except (ValueError, TypeError):
        return None
