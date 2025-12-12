# purerouter-sdk/src/purerouter/client.py
from __future__ import annotations
import time
from typing import Any, Dict, Iterable, Optional

import httpx

from .errors import APIError
from .types import Json, StreamEvent
from .resources.router import RouterResource
from .resources.deployments import DeploymentsResource

DEFAULT_BASE_URL = "https://api.purerouter-api.com"


class _Base:
    def __init__(
        self,
        *,
        router_key: Optional[str] = None,
        base_url: str = DEFAULT_BASE_URL,
        timeout: float = 30.0,
        headers: Optional[Dict[str, str]] = None,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.default_headers = {
            "User-Agent": "purerouter-python/0.1",
        }
        if headers:
            self.default_headers.update(headers)
        if router_key:
            self.default_headers.setdefault("x-router-key", router_key)

    def _retry_send(self, client: httpx.Client, req: httpx.Request) -> httpx.Response:
        backoff = 0.25
        for attempt in range(5):
            try:
                resp = client.send(req)
                if resp.status_code >= 500:
                    raise APIError(resp.status_code, "Server error", body=resp.text)
                return resp
            except (httpx.TransportError, APIError):
                if attempt == 4:
                    raise
                time.sleep(backoff)
                backoff *= 2
        raise RuntimeError("unreachable")

    @staticmethod
    def _iter_stream(resp: httpx.Response) -> Iterable[StreamEvent]:
        ct = (resp.headers.get("content-type") or "").lower()
        if "text/event-stream" in ct:
            for line in resp.iter_lines():
                if not line:
                    continue
                if isinstance(line, (bytes, bytearray)):
                    line = line.decode("utf-8", "ignore")
                if line.startswith(":"):
                    continue
                if line.lower().startswith("data:"):
                    line = line[5:].lstrip()
                yield StreamEvent(data=line)
        else:
            for chunk in resp.iter_bytes():
                if not chunk:
                    continue
                if isinstance(chunk, (bytes, bytearray)):
                    yield StreamEvent(data=chunk.decode("utf-8", "ignore"))
                else:
                    yield StreamEvent(data=str(chunk))

    @staticmethod
    async def _aiter_stream(resp: httpx.Response):
        ct = (resp.headers.get("content-type") or "").lower()
        if "text/event-stream" in ct:
            async for line in resp.aiter_lines():
                if not line:
                    continue
                if line.startswith(":"):
                    continue
                if line.lower().startswith("data:"):
                    line = line[5:].lstrip()
                yield StreamEvent(data=line)
        else:
            async for chunk in resp.aiter_bytes():
                if not chunk:
                    continue
                if isinstance(chunk, (bytes, bytearray)):
                    yield StreamEvent(data=chunk.decode("utf-8", "ignore"))
                else:
                    yield StreamEvent(data=str(chunk))


class PureRouter(_Base):

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.router = RouterResource(self)
        self.deployments = DeploymentsResource(self)

    def _client(self) -> httpx.Client:
        return httpx.Client(timeout=self.timeout, headers=self.default_headers)

    def health(self) -> Json:
        url = f"{self.base_url}/v1/health"
        with self._client() as c:
            r = self._retry_send(c, c.build_request("GET", url))
            if r.status_code >= 400:
                raise APIError(r.status_code, r.text, body=r.text)
            return r.json()


class AsyncPureRouter(_Base):

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.router = RouterResource(self)
        self.deployments = DeploymentsResource(self)

    def _client(self) -> httpx.AsyncClient:
        return httpx.AsyncClient(timeout=self.timeout, headers=self.default_headers)

    async def health(self) -> Json:
        url = f"{self.base_url}/v1/health"
        async with self._client() as c:
            r = await c.get(url)
            if r.status_code >= 400:
                raise APIError(r.status_code, r.text, body=r.text)
            return r.json()
