from __future__ import annotations

import asyncio
import contextlib
import functools
from itertools import islice
from typing import TYPE_CHECKING, Any, Protocol

import polars as pl

if TYPE_CHECKING:
    from collections.abc import (
        AsyncIterable,
        AsyncIterator,
        Awaitable,
        Callable,
        Iterable,
    )

    from marimo._plugins.stateless.status import progress_bar
    from tqdm.asyncio import tqdm

    from kabukit.sources.client import Client

    class _Progress(Protocol):
        def __call__(
            self,
            aiterable: AsyncIterable[Any],
            /,
            total: int | None = None,
            *args: Any,
            **kwargs: Any,
        ) -> AsyncIterator[Any]: ...


MAX_CONCURRENCY = 12


async def collect[T, R](
    function: Callable[[T], Awaitable[R]],
    args: Iterable[T],
    /,
    max_concurrency: int | None = None,
) -> AsyncIterator[R]:
    semaphore = asyncio.Semaphore(max_concurrency or MAX_CONCURRENCY)

    async def func(arg: T) -> R:
        async with semaphore:
            return await function(arg)

    tasks = {asyncio.create_task(func(arg)) for arg in args}

    try:
        for future in asyncio.as_completed(tasks):  # async for (python 3.13+)
            with contextlib.suppress(asyncio.CancelledError):
                yield await future
    finally:
        for task in tasks:
            task.cancel()
        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)


type Progress = type[progress_bar[Any] | tqdm[Any]] | _Progress


async def get[T, C: Client](
    client_factory: Callable[[], C],
    get: Callable[[C, T], Awaitable[pl.DataFrame]],
    args: Iterable[T],
    /,
    max_items: int | None = None,
    max_concurrency: int | None = None,
    progress: Progress | None = None,
) -> pl.DataFrame:
    """各種データを取得し、単一のDataFrameにまとめて返す。

    Args:
        client_factory (Callable[[], Client]): Clientインスタンスを生成する
            呼び出し可能オブジェクト。
            JQuantsClientやEdinetClientなど、Clientを継承したクラスを指定できる。
        get (Callable[[Client, T], Awaitable[pl.DataFrame]]): 取得するClientクラスの
            メソッドデータ。
        args (Iterable[T]): 取得対象の引数のリスト。
        max_items (int | None, optional): 取得数する上限。
        max_concurrency (int | None, optional): 同時に実行するリクエストの最大数。
            指定しないときはデフォルト値が使用される。
        progress (Progress | None, optional): 進捗表示のための関数。
            tqdm, marimoなどのライブラリを使用できる。
            指定しないときは進捗表示は行われない。

    Returns:
        DataFrame:
            すべての情報を含む単一のDataFrame。
    """
    args = list(islice(args, max_items))

    async with client_factory() as client:
        function = functools.partial(get, client)
        ait = collect(function, args, max_concurrency=max_concurrency)

        if progress:
            ait = progress(ait, total=len(args))

        dfs = [df async for df in ait if not df.is_empty()]
        return pl.concat(dfs, how="vertical_relaxed") if dfs else pl.DataFrame()
