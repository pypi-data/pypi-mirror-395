import asyncio
from enum import Enum
from typing import Any

from aiolimiter import AsyncLimiter
import httpx
from httpx import RequestError
from pydantic import BaseModel, Field

from moysklad_api.exceptions import DetailedMsApiError, MSApiError


class Method(str, Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"


class Request(BaseModel):
    method: str
    url: str
    params: dict[str, Any] | None = None
    json_data: Any | None = None
    data: str | bytes | None = None
    headers: dict[str, str] | None = None


class Response(BaseModel):
    status: int
    ok: bool
    data: Any = None
    error: str | None = None

    def __bool__(self):
        return self.ok


class Headers(BaseModel):
    token: str | None = Field(default=None, exclude=True)

    _accept: str = "application/json;charset=utf-8"
    _content_type: str = "application/json"

    @property
    def as_dict(self) -> dict[str, str]:
        headers = {
            "Accept": self._accept,
            "Content-Type": self._content_type,
        }
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        return headers


class BaseSession:
    """
    Base class for all requests using HTTPX.

    All requests follow Moysklad JSON API limitations:
    https://dev.moysklad.ru/doc/api/remap/1.2/#mojsklad-json-api-ogranicheniq
    """

    base: str
    """Base URL"""
    timeout: int
    """Base timeout"""
    headers: Headers
    """Base Headers"""

    _rate_limiter = AsyncLimiter(45, 3)
    _account_semaphore = asyncio.Semaphore(20)
    _user_semaphore = asyncio.Semaphore(5)
    _request_count = 0
    _lock = asyncio.Lock()

    def __init__(
        self,
        base: str,
        timeout: int = 30,
    ) -> None:
        self.base_url = base.rstrip("/")
        self.timeout = timeout

        self._client = httpx.AsyncClient(timeout=self.timeout)

    async def close(self):
        await self._client.aclose()

    async def make_request(self, request: Request) -> Response:
        async with self._rate_limiter:
            async with self._account_semaphore:
                async with self._user_semaphore:
                    async with self._lock:
                        BaseSession._request_count += 1
                        try:
                            response = await self._client.request(
                                method=request.method.upper(),
                                url=request.url,
                                params=request.params,
                                json=request.json_data,
                                content=request.data,
                                headers=self.headers.as_dict,
                            )
                        except RequestError as e:
                            raise DetailedMsApiError(str(e)) from e

                        if response.status_code >= 400:
                            try:
                                data = response.json()
                                if "errors" in data and isinstance(
                                    data["errors"], list
                                ):
                                    err = data["errors"][0]
                                    error_data = err.get("error", str(data))
                                    code = err.get("code")
                                    more_info = err.get("moreInfo")
                                else:
                                    error_data = str(data) or response.text
                                    code = more_info = None
                            except Exception:  # noqa: broad exception
                                error_data = response.text
                                code = more_info = None

                            raise MSApiError(
                                f"{error_data} (code: {code})", url=more_info
                            )

                        data = response.json() or response.text
                        return Response(status=response.status_code, ok=True, data=data)

    async def get(self, url: str, *, params: dict[str, Any] | None = None) -> Response:
        req = Request(method=Method.GET, url=url, params=params)
        return await self.make_request(req)

    async def post(
        self,
        url: str,
        *,
        json: Any | None = None,
        data: str | bytes | None = None,
    ) -> Response:
        req = Request(method=Method.POST, url=url, json_data=json, data=data)
        return await self.make_request(req)

    async def put(
        self,
        url: str,
        *,
        json: Any | None = None,
        data: str | bytes | None = None,
    ) -> Response:
        req = Request(method=Method.PUT, url=url, json_data=json, data=data)
        return await self.make_request(req)

    async def delete(
        self, url: str, *, params: dict[str, Any] | None = None
    ) -> Response:
        req = Request(method=Method.DELETE, url=url, params=params)
        return await self.make_request(req)
