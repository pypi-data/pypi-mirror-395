# purerouter-sdk/src/purerouter/resources/deployments.py
from __future__ import annotations
from typing import Any, Dict, Generator, AsyncGenerator

import httpx

from ..errors import APIError
from ..types import InvokeRequest, StreamEvent


class DeploymentsResource:
    def __init__(self, client: Any) -> None:
        self._client = client

    def _to_payload(self, request: InvokeRequest) -> Dict[str, Any]:
        if hasattr(request, "to_payload") and callable(getattr(request, "to_payload")):
            return request.to_payload()  # type: ignore[attr-defined]
        return {k: v for k, v in request.__dict__.items() if v is not None}

    def invoke(self, deployment_id: str, request: InvokeRequest) -> Dict[str, Any]:
        """
        Synchronous call without streaming.        
        """
        url = f"{self._client.base_url}/v1/deployments/{deployment_id}/invoke"
        payload = self._to_payload(request)
        with self._client._client() as c:  # pylint: disable=protected-access
            req = c.build_request("POST", url, json=payload)
            resp = self._client._retry_send(c, req)  # pylint: disable=protected-access
            if resp.status_code >= 400:
                raise APIError(resp.status_code, resp.text, body=resp.text)
            return resp.json()

    def stream(
        self,
        deployment_id: str,
        request: InvokeRequest,
    ) -> Generator[StreamEvent, None, None]:
        """
        Synchronous streaming call (SSE)..
        """
        url = f"{self._client.base_url}/v1/deployments/{deployment_id}/invoke"
        payload = self._to_payload(request)
        payload["stream"] = True

        headers = {"Accept": "text/event-stream"}
        with self._client._client() as c:  # pylint: disable=protected-access
            with c.stream("POST", url, json=payload, headers=headers) as resp:
                if resp.status_code >= 400:
                    body = resp.read().decode("utf-8", "ignore")
                    raise APIError(resp.status_code, body, body=body)
                yield from self._client._iter_stream(resp)  

    # Async
    async def ainvoke(self, deployment_id: str, request: InvokeRequest) -> Dict[str, Any]:
        """
        Asynchronous call without streaming.
        """
        url = f"{self._client.base_url}/v1/deployments/{deployment_id}/invoke"
        payload = self._to_payload(request)
        async with self._client._client() as c:  # pylint: disable=protected-access
            resp = await c.post(url, json=payload)
            if resp.status_code >= 400:
                raise APIError(resp.status_code, resp.text, body=await resp.aread())
            return resp.json()

    async def astream(
        self,
        deployment_id: str,
        request: InvokeRequest,
    ) -> AsyncGenerator[StreamEvent, None]:
        """
        Streaming asynchronous invocation (SSE).
        """
        url = f"{self._client.base_url}/v1/deployments/{deployment_id}/invoke"
        payload = self._to_payload(request)
        payload["stream"] = True

        headers = {"Accept": "text/event-stream"}
        async with self._client._client() as c:  
            async with c.stream("POST", url, json=payload, headers=headers) as resp:
                if resp.status_code >= 400:
                    body = await resp.aread()
                    raise APIError(resp.status_code, body.decode("utf-8", "ignore"), body=body)
                async for ev in self._client._aiter_stream(resp):  
                    yield ev
