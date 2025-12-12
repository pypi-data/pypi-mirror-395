# engines/base.py
from typing import Protocol
from ..types import Response, Proxy, Action


class Engine(Protocol):
    async def fetch(
        self,
        url: str,
        proxy: Proxy | None = None,
        headers: dict[str, str] | None = None,
        timeout: float = 30.0,
        **kwargs,
    ) -> Response: ...


class BrowserEngine(Protocol):
    async def fetch(
        self,
        url: str,
        proxy: Proxy | None = None,
        headers: dict[str, str] | None = None,
        actions: list[Action] | None = None,
        timeout: float = 30.0,
        **kwargs,
    ) -> Response: ...

    async def connect(self) -> None: ...

    async def disconnect(self) -> None: ...
