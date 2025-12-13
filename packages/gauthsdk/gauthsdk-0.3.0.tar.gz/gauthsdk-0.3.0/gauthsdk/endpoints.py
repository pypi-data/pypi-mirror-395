"""API endpoint constants for GAuth SDK."""

# Auth endpoints (public, requires X-Tenant-ID)
ENDPOINT_AUTH_LOGIN = "/v1/auth/login"
ENDPOINT_AUTH_LOGIN_USERNAME = "/v1/auth/login/username"
ENDPOINT_AUTH_LOGIN_PHONE = "/v1/auth/login/phone"
ENDPOINT_AUTH_REFRESH = "/v1/auth/refresh"
ENDPOINT_AUTH_LOGOUT = "/v1/auth/logout"
ENDPOINT_AUTH_REGISTER = "/v1/auth/register"
ENDPOINT_AUTH_FORGOT_PWD = "/v1/auth/forgot-password"
ENDPOINT_AUTH_RESET_PWD = "/v1/auth/reset-password"
ENDPOINT_AUTH_VERIFY_EMAIL = "/v1/auth/verify-email"

# Me endpoints (requires JWT auth)
ENDPOINT_ME = "/v1/me"
ENDPOINT_ME_PASSWORD = "/v1/me/password"
ENDPOINT_ME_SESSIONS = "/v1/me/sessions"

# Public API endpoints (S2S - requires API Key)
ENDPOINT_API_USERS = "/v1/api/users"
ENDPOINT_API_USER_SESSIONS = "/v1/api/users/{user_id}/sessions"
ENDPOINT_API_USER_SESSION_BY_ID = "/v1/api/users/{user_id}/sessions/{session_id}"
ENDPOINT_API_AUTH_VALIDATE = "/v1/api/auth/validate"

# Admin endpoints (requires JWT + admin role)
ENDPOINT_ADMIN_USERS = "/v1/admin/users"
ENDPOINT_ADMIN_TENANTS = "/v1/admin/tenants"
ENDPOINT_ADMIN_API_KEYS = "/v1/admin/api-keys"

# Headers
HEADER_CONTENT_TYPE = "Content-Type"
HEADER_ACCEPT = "Accept"
HEADER_AUTHORIZATION = "Authorization"
HEADER_API_KEY = "X-API-Key"
HEADER_TENANT_ID = "X-Tenant-ID"

CONTENT_TYPE_JSON = "application/json"
