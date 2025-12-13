"""
Access to request headers and context properties for UDFs.
"""

from fused.core._context import get_global_context

__all__ = [
    "get_header",
    "get_headers",
    "get_realtime_client_id",
    "get_recursion_factor",
    "get_user_email",
    "in_realtime",
    "in_batch",
]


def get_headers() -> dict[str, str]:
    """Get the request headers that were passed to the UDF."""
    context = get_global_context()
    if context and hasattr(context, "headers"):
        return context.headers
    return {}


def get_header(name: str) -> str | None:
    """Get a specific request header by name (case-insensitive)."""
    headers = get_headers()
    # Case-insensitive lookup
    for header_name, value in headers.items():
        if header_name.lower() == name.lower():
            return value
    return None


def get_user_email() -> str | None:
    """Get the user email from the current context."""
    context = get_global_context()
    if context and hasattr(context, "user_email"):
        return context.user_email
    return None


def get_realtime_client_id() -> str | None:
    """Get the realtime client ID from the current context."""
    context = get_global_context()
    if context and hasattr(context, "realtime_client_id"):
        return context.realtime_client_id
    return None


def get_recursion_factor() -> int | None:
    """Get the recursion factor from the current context."""
    context = get_global_context()
    if context and hasattr(context, "recursion_factor"):
        return context.recursion_factor
    return None


def in_realtime() -> bool:
    """Return True if the context is in a realtime job."""
    context = get_global_context()
    return context.in_realtime


def in_batch() -> bool:
    """Return True if the context is in a batch job."""
    context = get_global_context()
    return context.in_batch


async def _get_user_email_async() -> str:
    context = get_global_context()
    return await context.user_email_async()


def _get_auth_header(*, missing_ok: bool = False) -> dict[str, str]:
    context = get_global_context()
    return context.auth_header(missing_ok=missing_ok)


def _get_auth_scheme_and_token() -> tuple[str, str] | None:
    context = get_global_context()

    if context.auth_scheme and context.auth_token:
        return (context.auth_scheme, context.auth_token)
    return None
