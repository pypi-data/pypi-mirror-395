import asyncio
import json
from typing import Literal

from .types import (
    Response,
    Proxy,
    Action,
    Cookie,
    BrowserEndpoint,
    EngineType,
    ProxyStrategy,
)
from .pool import ProxyPool
from .engines import CurlEngine, CDPEngine, BaaSEngine
from .cache import Cache
from .telemetry import get_tracer

tracer = get_tracer()


class Fetcher:
    """
    Unified fetcher with explicit engine selection, proxy rotation,
    and anti-detection.

    Usage:
        async with Fetcher(proxies=[...], baas_endpoints=[...]) as f:
            # Default: curl
            resp = await f.fetch("https://example.com")

            # Explicit browser
            resp = await f.fetch("https://example.com", engine="browser")

            # Browser with actions
            resp = await f.fetch(
                "https://example.com",
                actions=[{"action": "wait", "selector": "#price"}],
            )
    """

    def __init__(
        self,
        # Proxy config
        proxies: list[Proxy | str] | ProxyPool | None = None,
        proxy_strategy: ProxyStrategy = "round_robin",
        # Browser engine selection
        browser_engine: Literal["cdp", "baas"] = "cdp",
        # CDP options
        cdp_endpoint: str | None = None,
        headless: bool = True,
        # BaaS options
        baas_endpoints: list[BrowserEndpoint] | None = None,
        # General options
        timeout: float = 30.0,
        browser_timeout: float = 60.0,
        max_retries: int = 3,
        max_concurrent: int = 50,
        max_concurrent_browser: int = 10,
        # Cache
        cache: Cache | bool | None = None,
    ):
        """
        Initialize the Fetcher.

        Args:
            proxies: List of proxy URLs or Proxy objects
            proxy_strategy: Strategy for proxy selection
            browser_engine: "cdp" (local/remote Playwright) or "baas" (HTTP API)
            cdp_endpoint: Optional CDP WebSocket URL (e.g. ws://localhost:3000)
            headless: Run browser in headless mode (CDP only)
            baas_endpoints: List of BaaS endpoints
            timeout: Default timeout for curl requests
            browser_timeout: Default timeout for browser requests
            max_retries: Max retries for curl requests
            max_concurrent: Max concurrent curl requests
            max_concurrent_browser: Max concurrent browser requests
            cache: Cache implementation (e.g. FileSystemCache)
        """
        # Cache
        self.cache: Cache | None = None
        if cache is True:
            from .cache import FileSystemCache

            self.cache = FileSystemCache()
        elif cache is False:
            self.cache = None
        else:
            self.cache = cache

        # Proxy pool
        if isinstance(proxies, ProxyPool):
            self.proxy_pool = proxies
        else:
            self.proxy_pool = ProxyPool(proxies or [], strategy=proxy_strategy)

        # Curl engine
        self._curl = CurlEngine(
            timeout=timeout,
            max_retries=max_retries,
        )

        # Browser engine
        self._browser_engine_type = browser_engine
        self._browser: CDPEngine | BaaSEngine
        if browser_engine == "cdp":
            self._browser = CDPEngine(
                cdp_endpoint=cdp_endpoint,
                headless=headless,
                timeout=browser_timeout,
                cache=self.cache,
            )
        else:
            self._browser = BaaSEngine(
                endpoints=baas_endpoints,
                timeout=browser_timeout,
            )

        # Concurrency control
        self._semaphore = asyncio.Semaphore(max_concurrent)
        self._browser_semaphore = asyncio.Semaphore(max_concurrent_browser)

        # Defaults
        self.timeout = timeout
        self.browser_timeout = browser_timeout
        self.max_retries = max_retries

    async def __aenter__(self) -> "Fetcher":
        await self._browser.connect()
        return self

    async def __aexit__(self, *args) -> None:
        await self._browser.disconnect()

    async def fetch(
        self,
        url: str,
        *,
        engine: EngineType = "curl",
        location: str | None = None,
        actions: list[Action | dict | str] | None = None,
        cookies: dict[str, str] | list[Cookie] | None = None,
        headers: dict[str, str] | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
        retry_on: set[int] | None = None,
        retry_backoff: float | None = None,
        referer: str | None = None,
        allow_redirects: bool = True,
        wait_until: str = "domcontentloaded",
    ) -> Response:
        """
        Fetch a URL.

        Args:
            url: Target URL
            engine: "curl" (default) or "browser"
            location: Geo location for proxy selection
            actions: List of `Action` objects or dicts (implies engine="browser")
            cookies: Dict of name/value pairs or list of `Cookie` objects
            headers: Custom headers
            timeout: Request timeout in seconds
            max_retries: Number of retries for failed requests (curl only)
            retry_on: Set of HTTP status codes to retry on (curl only, default: {429, 500, 502, 503, 504})
            retry_backoff: Base for exponential backoff in seconds (curl only, default: 2.0)
            referer: Referer header
            allow_redirects: Follow HTTP redirects
            wait_until: Browser load state ("domcontentloaded", "load", "networkidle")

        Returns:
            `Response` object containing status, body, cookies, etc. - check .ok or .error
        """
        # Normalize actions - implies browser
        normalized_actions: list[Action] | None = None
        if actions:
            normalized_actions = []
            for a in actions:
                if isinstance(a, Action):
                    normalized_actions.append(a)
                elif isinstance(a, dict):
                    normalized_actions.append(Action(**a))
                elif isinstance(a, str):
                    # Parse string shorthand
                    # "wait_for_load"
                    # "click:#selector"
                    # "wait:2000"
                    # "screenshot"
                    # "screenshot:filename.png"
                    if ":" in a:
                        action_type, value = a.split(":", 1)
                        if action_type == "click":
                            normalized_actions.append(
                                Action(action="click", selector=value)
                            )
                        elif action_type == "wait":
                            # Check if value is number (timeout) or selector
                            if value.isdigit():
                                normalized_actions.append(
                                    Action(action="wait", timeout=int(value))
                                )
                            else:
                                normalized_actions.append(
                                    Action(action="wait", selector=value)
                                )
                        elif action_type == "input":
                            # input:#selector:value - might be too complex for simple split
                            # Let's support simple input:#selector=value
                            if "=" in value:
                                sel, val = value.split("=", 1)
                                normalized_actions.append(
                                    Action(action="input", selector=sel, value=val)
                                )
                            else:
                                # Fallback or error? Let's assume just selector focus? No, input needs value.
                                # Maybe just don't support complex input in shorthand.
                                pass
                        elif action_type == "screenshot":
                            normalized_actions.append(
                                Action(action="screenshot", value=value)
                            )
                        elif action_type == "scroll":
                            normalized_actions.append(
                                Action(action="scroll", selector=value)
                            )
                        elif action_type == "hover":
                            normalized_actions.append(
                                Action(action="hover", selector=value)
                            )
                    else:
                        # No arguments
                        if a == "wait_for_load":
                            normalized_actions.append(Action(action="wait_for_load"))
                        elif a == "screenshot":
                            normalized_actions.append(Action(action="screenshot"))

            engine = "browser"

        # Start OTel span
        with tracer.start_as_current_span("phantomfetch.fetch") as span:
            span.set_attribute("url.full", url)
            span.set_attribute("phantomfetch.engine", engine)
            span.set_attribute("phantomfetch.cache.enabled", bool(self.cache))

            # Enhanced OTel attributes
            if timeout:
                span.set_attribute("phantomfetch.config.timeout", float(timeout))
            if wait_until:
                span.set_attribute("phantomfetch.config.wait_until", wait_until)

            if normalized_actions:
                span.set_attribute(
                    "phantomfetch.actions.count", len(normalized_actions)
                )
                try:
                    # Serialize actions to JSON for debugging
                    # We only serialize the 'action' and 'selector' to keep it concise
                    actions_summary = [
                        {"action": a.action, "selector": a.selector, "value": a.value}
                        for a in normalized_actions
                    ]
                    span.set_attribute(
                        "phantomfetch.actions.json", json.dumps(actions_summary)
                    )
                except Exception:
                    pass

            # Check cache
            if self.cache and self.cache.should_cache_request("document"):
                # Simple cache key generation
                # TODO: Include actions/headers in key if needed
                cache_key = f"{engine}:{url}"
                cached_resp = await self.cache.get(cache_key)
                if cached_resp:
                    cached_resp.from_cache = True
                    span.set_attribute("phantomfetch.cache.hit", True)
                    return cached_resp

            span.set_attribute("phantomfetch.cache.hit", False)

            # Get proxy
            proxy = self.proxy_pool.get(url=url, location=location)
            if proxy:
                span.set_attribute("phantomfetch.proxy", proxy.url)

            # Route to engine
            if engine == "browser":
                resp = await self._fetch_browser(
                    url=url,
                    proxy=proxy,
                    headers=headers,
                    cookies=cookies,
                    actions=normalized_actions,
                    timeout=timeout or self.browser_timeout,
                    location=location,
                    wait_until=wait_until,
                )
            else:
                resp = await self._fetch_curl(
                    url=url,
                    proxy=proxy,
                    headers=headers,
                    cookies=cookies,
                    timeout=timeout or self.timeout,
                    max_retries=max_retries or self.max_retries,
                    retry_on=retry_on,
                    retry_backoff=retry_backoff,
                    referer=referer,
                    allow_redirects=allow_redirects,
                )

            # Update proxy stats
            if proxy:
                if resp.ok:
                    self.proxy_pool.mark_success(proxy)
                elif resp.error:
                    self.proxy_pool.mark_failed(proxy)

            # Cache response
            if self.cache and resp.ok and self.cache.should_cache_request("document"):
                # Simple cache key generation
                cache_key = f"{engine}:{url}"
                await self.cache.set(cache_key, resp)

            return resp

    async def fetch_many(
        self,
        urls: list[str],
        *,
        engine: EngineType = "curl",
        location: str | None = None,
        actions: list[Action | dict | str] | None = None,
        headers: dict[str, str] | None = None,
        timeout: float | None = None,
    ) -> list[Response]:
        """
        Fetch multiple URLs concurrently.

        Args:
            urls: List of URLs
            engine: Engine selection (applied to all)
            location: Geo location for proxy selection
            actions: Browser actions (applied to all)
            headers: Custom headers (applied to all)
            timeout: Request timeout

        Returns:
            List of Response objects in same order as urls
        """
        tasks = [
            self.fetch(
                url,
                engine=engine,
                location=location,
                actions=actions,
                headers=headers,
                timeout=timeout,
            )
            for url in urls
        ]

        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Convert exceptions to Response objects
        responses = []
        for url, result in zip(urls, results):
            if isinstance(result, Exception):
                responses.append(
                    Response(
                        url=url,
                        status=0,
                        body=b"",
                        engine=engine if engine != "browser" else "curl",
                        error=str(result),
                    )
                )
            else:
                # result is definitely Response here because return_exceptions=True returns Union[T, BaseException]
                # and we handled Exception branch
                from typing import cast

                responses.append(cast(Response, result))

        return responses

    async def _fetch_curl(
        self,
        url: str,
        proxy: Proxy | None,
        headers: dict[str, str] | None,
        timeout: float,
        max_retries: int,
        referer: str | None,
        allow_redirects: bool,
        cookies: dict[str, str] | list[Cookie] | None = None,
        retry_on: set[int] | None = None,
        retry_backoff: float | None = None,
    ) -> Response:
        async with self._semaphore:
            return await self._curl.fetch(
                url=url,
                proxy=proxy,
                headers=headers,
                cookies=cookies,
                timeout=timeout,
                max_retries=max_retries,
                retry_on=retry_on,
                retry_backoff=retry_backoff,
                referer=referer,
                allow_redirects=allow_redirects,
            )

    async def _fetch_browser(
        self,
        url: str,
        proxy: Proxy | None,
        headers: dict[str, str] | None,
        actions: list[Action] | None,
        timeout: float,
        location: str | None,
        wait_until: str,
        cookies: dict[str, str] | list[Cookie] | None = None,
    ) -> Response:
        async with self._semaphore:
            async with self._browser_semaphore:
                if self._browser_engine_type == "cdp":
                    from .engines import CDPEngine
                    from typing import cast

                    browser = cast(CDPEngine, self._browser)
                    return await browser.fetch(
                        url=url,
                        proxy=proxy,
                        headers=headers,
                        cookies=cookies,
                        actions=actions,
                        timeout=timeout,
                        location=location,
                        wait_until=wait_until,
                    )
                else:
                    from .engines import BaaSEngine
                    from typing import cast

                    browser = cast(BaaSEngine, self._browser)
                    return await browser.fetch(
                        url=url,
                        proxy=proxy,
                        headers=headers,
                        actions=actions,
                        timeout=timeout,
                        location=location,
                    )
