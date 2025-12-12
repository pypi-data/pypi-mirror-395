# purerouter-sdk/src/purerouter/resources/router.py
from __future__ import annotations
from typing import Any, Generator

import httpx
from dataclasses import fields as dc_fields

from ..errors import APIError
from ..types import InferRequest, InferResponse, StreamEvent


class RouterResource:
    def __init__(self, client: Any) -> None:
        self._client = client

    def infer(self, request: InferRequest) -> InferResponse:
        url = f"{self._client.base_url}/v1/infer"
        payload = {k: v for k, v in request.__dict__.items() if v is not None}
        with self._client._client() as c:  # pylint: disable=protected-access
            req = c.build_request("POST", url, json=payload)
            resp = self._client._retry_send(c, req)  # pylint: disable=protected-access
            if resp.status_code >= 400:
                body = resp.text
                raise APIError(resp.status_code, body, body=body)
            data = resp.json()
            allowed = {f.name for f in dc_fields(InferResponse)}
            filtered = {k: v for k, v in data.items() if k in allowed}
            return InferResponse(**filtered)

    def stream(self, request: InferRequest) -> Generator[StreamEvent, None, None]:
        url = f"{self._client.base_url}/v1/infer"
        payload = {k: v for k, v in request.__dict__.items() if v is not None}
        payload["stream"] = True
        with self._client._client() as c:  
            with c.stream("POST", url, json=payload) as resp:
                if resp.status_code >= 400:
                    body = resp.read().decode("utf-8", "ignore")
                    raise APIError(resp.status_code, body, body=body)
                yield from self._client._iter_stream(resp)  # pylint: disable=protected-access


    async def ainfer(self, request: InferRequest) -> InferResponse:
        url = f"{self._client.base_url}/v1/infer"
        payload = {k: v for k, v in request.__dict__.items() if v is not None}
        async with self._client._client() as c:  # pylint: disable=protected-access
            resp = await c.post(url, json=payload)
            if resp.status_code >= 400:
                raise APIError(resp.status_code, resp.text, body=await resp.aread())
            data = resp.json()
            allowed = {f.name for f in dc_fields(InferResponse)}
            filtered = {k: v for k, v in data.items() if k in allowed}
            return InferResponse(**filtered)

    async def astream(self, request: InferRequest):
        url = f"{self._client.base_url}/v1/infer"
        payload = {k: v for k, v in request.__dict__.items() if v is not None}
        payload["stream"] = True
        async with self._client._client() as c:  
            async with c.stream("POST", url, json=payload) as resp:
                if resp.status_code >= 400:
                    body = await resp.aread()
                    raise APIError(resp.status_code, body.decode("utf-8", "ignore"), body=body)
                async for ev in self._client._aiter_stream(resp):  # pylint: disable=protected-access
                    yield ev
