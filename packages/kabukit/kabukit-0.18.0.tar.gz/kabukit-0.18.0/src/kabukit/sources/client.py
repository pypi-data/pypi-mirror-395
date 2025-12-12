from __future__ import annotations

import asyncio
import functools
from typing import TYPE_CHECKING, ClassVar, Self

import httpx
import tenacity
from httpx import AsyncClient

if TYPE_CHECKING:
    from collections.abc import Callable
    from concurrent.futures import Executor

    from httpx import Response
    from httpx._types import QueryParamTypes


def is_retryable(e: BaseException) -> bool:
    """例外がリトライ可能なネットワークエラーであるかを判定する。"""
    return isinstance(e, (httpx.ConnectTimeout, httpx.ReadTimeout, httpx.ConnectError))


class Client:
    client: AsyncClient
    base_url: ClassVar[str]
    executor: Executor | None = None

    def __init__(self, executor: Executor | None = None) -> None:
        self.client = AsyncClient(base_url=self.__class__.base_url, timeout=20)
        self.executor = executor

    async def aclose(self) -> None:
        """HTTPクライアントを閉じる。"""
        await self.client.aclose()

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:  # pyright: ignore[reportMissingParameterType, reportUnknownParameterType]  # noqa: ANN001
        await self.aclose()

    @tenacity.retry(
        reraise=True,
        stop=tenacity.stop_after_attempt(3),
        wait=tenacity.wait_exponential(multiplier=1, min=2, max=10),
        retry=tenacity.retry_if_exception(is_retryable),
    )
    async def get(self, url: str, /, params: QueryParamTypes | None = None) -> Response:
        """リトライ処理を伴うGETリクエストを送信する。

        ネットワークエラーが発生した場合、指数関数的バックオフを用いて
        最大3回までリトライする。

        Args:
            url: GETリクエストのURLパス。
            params: リクエストのクエリパラメータ。

        Returns:
            httpx.Response: APIからのレスポンスオブジェクト。

        Raises:
            httpx.HTTPStatusError: APIリクエストがHTTPエラーステータスを返した場合。
        """
        response = await self.client.get(url, params=params)
        response.raise_for_status()
        return response

    async def run_in_executor[**P, R](
        self,
        func: Callable[P, R],
        /,
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> R:
        """指定された関数をエグゼキューター内で非同期に実行する。"""
        if self.executor is None:
            return func(*args, **kwargs)

        loop = asyncio.get_running_loop()
        pfunc = functools.partial(func, *args, **kwargs)
        return await loop.run_in_executor(self.executor, pfunc)
