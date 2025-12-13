"""Users API for GAuth SDK."""

from typing import TYPE_CHECKING, List, Optional

from .endpoints import (
    ENDPOINT_API_USER_SESSION_BY_ID,
    ENDPOINT_API_USER_SESSIONS,
    ENDPOINT_API_USERS,
)
from .models import ListUsersResponse, Paging, Session, User

if TYPE_CHECKING:
    from .client import Client


class UsersAPI:
    """Provides methods for interacting with user endpoints."""

    def __init__(self, client: "Client"):
        self._client = client

    def get(self, user_id: str) -> User:
        """
        Get a user by ID.

        Args:
            user_id: The user's UUID

        Returns:
            User object
        """
        path = f"{ENDPOINT_API_USERS}/{user_id}"
        response = self._client._request(method="GET", path=path)
        data = self._client._parse_response(response)
        return User.from_dict(data)

    def list(
        self,
        page: int = 1,
        limit: int = 20,
        status: Optional[str] = None,
        role: Optional[str] = None,
        search: Optional[str] = None,
    ) -> ListUsersResponse:
        """
        List users with pagination.

        Args:
            page: Page number (default: 1)
            limit: Items per page (default: 20)
            status: Filter by status (e.g., "active", "inactive")
            role: Filter by role
            search: Search query

        Returns:
            ListUsersResponse with users and paging info
        """
        params = {}
        if page > 0:
            params["page"] = page
        if limit > 0:
            params["limit"] = limit
        if status:
            params["status"] = status
        if role:
            params["role"] = role
        if search:
            params["search"] = search

        response = self._client._request(
            method="GET",
            path=ENDPOINT_API_USERS,
            params=params if params else None,
        )
        data, paging = self._client._parse_list_response(response)

        users = [User.from_dict(u) for u in (data or [])]
        return ListUsersResponse(users=users, paging=paging)

    def list_sessions(self, user_id: str) -> List[Session]:
        """
        List all active sessions for a user.

        Args:
            user_id: The user's UUID

        Returns:
            List of Session objects
        """
        path = ENDPOINT_API_USER_SESSIONS.format(user_id=user_id)
        response = self._client._request(method="GET", path=path)
        data = self._client._parse_response(response)
        return [Session.from_dict(s) for s in (data or [])]

    def revoke_session(self, user_id: str, session_id: str) -> None:
        """
        Revoke/delete a specific session for a user.

        Args:
            user_id: The user's UUID
            session_id: The session's UUID
        """
        path = ENDPOINT_API_USER_SESSION_BY_ID.format(
            user_id=user_id, session_id=session_id
        )
        response = self._client._request(method="DELETE", path=path)
        self._client._parse_response(response)
