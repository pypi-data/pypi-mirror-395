# luna-sdk

Official Python SDK for the Eclipse Softworks Platform API.

## Installation

```bash
pip install luna-sdk
```

## Quick Start

```python
import asyncio
from luna import LunaClient

async def main():
    # API Key authentication
    async with LunaClient(api_key="lk_live_xxxx") as client:
        # List users
        users = await client.users.list(limit=10)
        
        # Get a specific user
        user = await client.users.get("usr_123")
        
        # Create a new user
        from luna import UserCreate
        new_user = await client.users.create(
            UserCreate(email="john@example.com", name="John Doe")
        )

asyncio.run(main())
```

## Authentication

### API Key

```python
client = LunaClient(api_key="lk_live_xxxx")
```

### OAuth Token

```python
async def save_tokens(tokens):
    # Save tokens to database
    pass

client = LunaClient(
    access_token=session.access_token,
    refresh_token=session.refresh_token,
    on_token_refresh=save_tokens,
)
```

## Error Handling

```python
from luna import LunaClient, NotFoundError, RateLimitError

try:
    await client.users.get("usr_nonexistent")
except NotFoundError as e:
    print(f"User not found: {e.message}")
except RateLimitError as e:
    print(f"Rate limited, retry after: {e.retry_after}")
```

## Configuration

```python
client = LunaClient(
    api_key="lk_live_xxxx",
    base_url="https://api.staging.eclipse.dev",
    timeout=60.0,
    max_retries=5,
    log_level="debug",
)
```

## License

MIT © Eclipse Softworks
