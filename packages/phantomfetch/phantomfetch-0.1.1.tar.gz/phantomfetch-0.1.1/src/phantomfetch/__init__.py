from .types import (
    Response,
    Proxy,
    Action,
    BrowserEndpoint,
    EngineType,
    ProxyStrategy,
    ActionType,
    NetworkExchange,
    Cookie,
)
from .pool import ProxyPool
from .fetch import Fetcher
from .engines import CurlEngine, CDPEngine, BaaSEngine
from .cache import FileSystemCache

# Try to install uvloop if available
try:
    import uvloop

    uvloop.install()
except ImportError:
    pass


async def fetch(
    url: str,
    *,
    engine: EngineType = "curl",
    actions: list[Action | dict | str] | None = None,
    headers: dict[str, str] | None = None,
    timeout: float | None = None,
    wait_until: str = "domcontentloaded",
    cache: bool = False,
) -> Response:
    """
    One-liner fetch function.

    Args:
        url: Target URL
        engine: "curl" or "browser"
        actions: List of actions
        headers: Custom headers
        timeout: Timeout in seconds
        wait_until: Browser load state
        cache: If True, use default FileSystemCache
    """
    async with Fetcher(cache=cache) as f:
        return await f.fetch(
            url,
            engine=engine,
            actions=actions,
            headers=headers,
            timeout=timeout,
            wait_until=wait_until,
        )


# Alias for requests/httpx users
get = fetch

__all__ = [
    # Main API
    "Fetcher",
    "fetch",
    "get",
    "Response",
    "Proxy",
    "ProxyPool",
    "Action",
    "BrowserEndpoint",
    "FileSystemCache",
    "NetworkExchange",
    "Cookie",
    # Types
    "EngineType",
    "ProxyStrategy",
    "ActionType",
    # Engines (advanced)
    "CurlEngine",
    "CDPEngine",
    "BaaSEngine",
]
