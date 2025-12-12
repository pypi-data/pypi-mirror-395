"""Async Redis helper utilities."""

from __future__ import annotations

from typing import Any, Optional, TYPE_CHECKING

from urllib.parse import urlparse

try:
    import redis.asyncio as redis
except ImportError:  # pragma: no cover - Redis is optional
    redis = None


if TYPE_CHECKING:  # pragma: no cover - typing aid
    from redis.asyncio import Redis


def create_async_redis_client(
    url: Optional[str],
    *,
    decode_responses: bool = True,
    encoding: str = "utf-8",
    logger: Optional[Any] = None,
    **kwargs,
) -> Optional["Redis"]:
    """Return a configured async Redis client or None if unavailable.

    Args:
        url: Redis connection URL.
        decode_responses: Whether to decode responses to str.
        encoding: Character encoding to use with decoded responses.
        logger: Optional logger supporting .warning() for diagnostics.
        **kwargs: Additional keyword arguments forwarded to Redis.from_url.
    """
    if redis is None:
        return None

    if not url or url in {"redis_url", "REDIS_URL"}:
        return None

    parsed = urlparse(url)
    connection_kwargs = {
        "decode_responses": decode_responses,
        "encoding": encoding,
    }
    connection_kwargs.update(kwargs)

    if parsed.scheme == "rediss":
        connection_kwargs.setdefault("ssl_cert_reqs", "none")
        connection_kwargs.setdefault("ssl_check_hostname", False)

    try:
        return redis.Redis.from_url(url, **connection_kwargs)
    except Exception as exc:  # pragma: no cover - best effort logging
        if logger is not None:
            logger.warning(f"Failed to create Redis client: {exc}")
        return None
