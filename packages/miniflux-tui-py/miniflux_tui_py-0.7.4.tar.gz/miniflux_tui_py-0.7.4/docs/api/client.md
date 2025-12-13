# API Client Reference

## MinifluxClient

`MinifluxClient` is the async wrapper around the official Miniflux API library.

::: miniflux_tui.api.client.MinifluxClient
    options:
      docstring_style: google
      members:
        - __init__
        - change_entry_status
        - toggle_starred
        - save_entry
        - get_entries
        - get_unread_count
        - get_starred_count

## Connection

The client connects to your Miniflux server using:

- __Base URL__: The server's URL (e.g., `https://miniflux.example.com`)
- __API Key__: Your personal API token (retrieved via the password command in `config.toml`)
- __Certificate Validation__: Configurable for self-signed certificates

## Async Operations

All API calls are asynchronous and use `asyncio` for non-blocking operations.

Example:

```python
client = MinifluxClient(
    base_url="https://miniflux.example.com",
    api_key="your-api-key"
)

# Fetch unread entries
entries = await client.get_entries("unread")

# Mark an entry as read
await client.change_entry_status(entry_id=123, status="read")
```

## Error Handling

The client may raise exceptions for:

- Network errors (connection failures)
- Invalid credentials (wrong API token)
- Server errors (5xx responses)
- Invalid requests (malformed parameters)

Always wrap API calls in try-except blocks when appropriate.
