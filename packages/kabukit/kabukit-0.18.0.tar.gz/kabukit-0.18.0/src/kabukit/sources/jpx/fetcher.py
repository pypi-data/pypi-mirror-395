from __future__ import annotations

import functools
from concurrent.futures import ProcessPoolExecutor
from typing import TYPE_CHECKING

import polars as pl

from kabukit.utils import fetcher

from .client import JpxClient

if TYPE_CHECKING:
    from kabukit.utils.fetcher import Progress


async def get_shares(
    max_items: int | None = None,
    max_concurrency: int = 12,
    max_workers: int | None = None,
    progress: Progress | None = None,
) -> pl.DataFrame:
    """上場株式数を取得する。

    Args:
        max_items (int | None, optional): 取得数の上限。
        max_concurrency (int | None, optional): 同時に実行するリクエストの最大数。
            デフォルトは8。
        max_workers (int | None, optional): PDFのパース処理を実行するための
            ワーカープロセスの最大数。指定しないときは`ProcessPoolExecutor`の
            デフォルト値が使用される。
        progress (Progress | None, optional): 進捗表示のための関数。
            tqdm, marimoなどのライブラリを使用できる。
            指定しないときは進捗表示は行われない。

    Returns:
        DataFrame:
            文書一覧を含む単一のDataFrame。
    """
    async with JpxClient() as client:
        pdf_urls = [url async for url in client.iter_shares_pdf_urls()]

    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        df = await fetcher.get(
            functools.partial(JpxClient, executor=executor),
            JpxClient.get_shares,
            pdf_urls,
            max_items=max_items,
            max_concurrency=max_concurrency,
            progress=progress,
        )

    if df.is_empty():
        return pl.DataFrame()

    return df.sort("Code", "Date")
