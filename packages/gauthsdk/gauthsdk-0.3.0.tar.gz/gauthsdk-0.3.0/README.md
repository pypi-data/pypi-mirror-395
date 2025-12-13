# GAuth SDK for Python

Python SDK for GAuth API - GearVN Authentication Service.

## Installation

```bash
pip install gauthsdk
```

Or install from source:

```bash
pip install -e .
```

## Quick Start

```python
from gauthsdk import Client

# Initialize client with API Key (for S2S operations)
client = Client(
    api_key="gvn_sk_your_api_key_here",
    base_url="http://localhost:3000",
)

# Get user by ID
user = client.users.get("user-uuid")
print(f"User: {user.full_name()}")
print(f"Email: {user.email}")
print(f"Role: {user.role}")

# List users with pagination
result = client.users.list(page=1, limit=20)
for user in result.users:
    print(f"- {user.email}: {user.status}")
print(f"Total users: {result.paging.total}")

# Validate JWT token
claims = client.validate_token("user_jwt_token")
print(f"User ID: {claims.sub}")
print(f"Tenant ID: {claims.tenant_id}")
print(f"Role: {claims.role}")
```

## Features

### Users API

```python
# Get user by ID
user = client.users.get("user-uuid")

# List users with filters
result = client.users.list(
    page=1,
    limit=20,
    status="active",
    role="user",
    search="john",
)

# List user sessions
sessions = client.users.list_sessions("user-uuid")
for session in sessions:
    print(f"Session: {session.id}, Created: {session.created_at}")

# Revoke a session
client.users.revoke_session("user-uuid", "session-uuid")
```

### Auth API

For auth operations (login, register, etc.), you need to set `tenant_id`:

```python
client = Client(
    api_key="gvn_sk_...",
    tenant_id="tenant-uuid",
    base_url="http://localhost:3000",
)

# Login
tokens = client.auth.login("user@example.com", "password")
print(f"Access Token: {tokens.access_token}")
print(f"Refresh Token: {tokens.refresh_token}")

# Refresh token
new_tokens = client.auth.refresh_token(tokens.refresh_token)
print(f"New Access Token: {new_tokens.access_token}")

# Validate token
claims = client.auth.validate_token(tokens.access_token)
print(f"User: {claims.sub}")
```

## Error Handling

```python
from gauthsdk import Client, APIError

client = Client(api_key="gvn_sk_...")

try:
    user = client.users.get("invalid-uuid")
except APIError as e:
    print(f"Error {e.code}: {e.message}")

    if e.is_not_found():
        print("User not found")
    elif e.is_unauthorized():
        print("Invalid API key")
    elif e.is_forbidden():
        print("Insufficient permissions")
    elif e.is_rate_limited():
        print("Too many requests, please slow down")
```

## Configuration

| Parameter | Description | Default |
|-----------|-------------|---------|
| `api_key` | API Key for authentication (`X-API-Key` header) | None |
| `base_url` | Base URL for the API | `http://localhost:3000` |
| `tenant_id` | Tenant ID for multi-tenant operations | None |
| `timeout` | Request timeout in seconds | 30 |

## Requirements

- Python 3.8+
- `requests` library

## License

MIT
