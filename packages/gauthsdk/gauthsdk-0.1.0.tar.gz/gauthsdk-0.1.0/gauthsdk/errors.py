"""Error types for GAuth SDK."""

from typing import Optional


class APIError(Exception):
    """Represents an error response from the API."""

    def __init__(self, code: int, message: str, reason: Optional[str] = None):
        self.code = code
        self.message = message
        self.reason = reason
        super().__init__(self._format_message())

    def _format_message(self) -> str:
        if self.reason:
            return f"API error {self.code}: {self.message} ({self.reason})"
        return f"API error {self.code}: {self.message}"

    def is_not_found(self) -> bool:
        """Returns True if the error is a 404 Not Found error."""
        return self.code == 404

    def is_unauthorized(self) -> bool:
        """Returns True if the error is a 401 Unauthorized error."""
        return self.code == 401

    def is_forbidden(self) -> bool:
        """Returns True if the error is a 403 Forbidden error."""
        return self.code == 403

    def is_rate_limited(self) -> bool:
        """Returns True if the error is a 429 Too Many Requests error."""
        return self.code == 429

    @classmethod
    def from_response(cls, status_code: int, data: dict) -> "APIError":
        """Create an APIError from an API response."""
        error_data = data.get("error", data)
        return cls(
            code=error_data.get("code", status_code),
            message=error_data.get("message", "Unknown error"),
            reason=error_data.get("reason"),
        )
