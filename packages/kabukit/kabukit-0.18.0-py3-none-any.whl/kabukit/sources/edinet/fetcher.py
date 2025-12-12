from __future__ import annotations

import datetime
from typing import TYPE_CHECKING

import polars as pl

from kabukit.utils import fetcher
from kabukit.utils.datetime import get_past_dates

from .client import EdinetClient

if TYPE_CHECKING:
    from collections.abc import Iterable

    from kabukit.utils.fetcher import Progress


async def get_list(
    dates: Iterable[datetime.date | str] | datetime.date | str | None = None,
    /,
    days: int | None = None,
    years: int | None = None,
    max_items: int | None = None,
    max_concurrency: int = 12,
    progress: Progress | None = None,
) -> pl.DataFrame:
    """過去 days 日または years 年の文書一覧を取得し、単一の DataFrame にまとめて返す。

    Args:
        dates (Iterable[datetime.date | str] | datetime.date | str | None):
            取得対象の日付のリスト。None の場合は days または years に基づいて
            日付リストを生成する。
        days (int | None): 過去 days 日の日付リストを取得する。
        years (int | None): 過去 years 年の日付リストを取得する。
            daysが指定されている場合は無視される。
        max_items (int | None, optional): 取得数の上限。
        max_concurrency (int, optional): 同時に実行するリクエストの最大数。
            デフォルトは12。
        progress (Progress | None, optional): 進捗表示のための関数。
            tqdm, marimoなどのライブラリを使用できる。
            指定しないときは進捗表示は行われない。

    Returns:
        DataFrame:
            文書一覧を含む単一のDataFrame。
    """
    if isinstance(dates, (str, datetime.date)):
        async with EdinetClient() as client:
            return await client.get_list(dates)

    if dates is None:
        dates = get_past_dates(days=days, years=years)

    df = await fetcher.get(
        EdinetClient,
        EdinetClient.get_list,
        dates,
        max_items=max_items,
        max_concurrency=max_concurrency,
        progress=progress,
    )

    if df.is_empty():
        return pl.DataFrame()

    return df.sort("Code", "Date")


async def get_documents(
    doc_ids: Iterable[str] | str,
    /,
    max_items: int | None = None,
    max_concurrency: int = 12,
    progress: Progress | None = None,
    *,
    pdf: bool = False,
) -> pl.DataFrame:
    """文書をCSV形式またはPDF形式で取得し、単一のDataFrameにまとめて返す。

    Args:
        doc_ids (Iterable[str] | str): 取得対象の文書IDのリスト。
        max_items (int | None, optional): 取得数の上限。
        max_concurrency (int, optional): 同時に実行するリクエストの最大数。
            デフォルトは12。
        progress (Progress | None, optional): 進捗表示のための関数。
            tqdm, marimoなどのライブラリを使用できる。
            指定しないときは進捗表示は行われない。
        pdf (bool): PDF形式で取得する場合はTrue、CSV形式で取得する場合はFalse。

    Returns:
        DataFrame:
            文書含む単一のDataFrame。
    """
    if isinstance(doc_ids, str):
        async with EdinetClient() as client:
            return await client.get_document(doc_ids, pdf=pdf)

    df = await fetcher.get(
        EdinetClient,
        EdinetClient.get_pdf if pdf else EdinetClient.get_csv,
        doc_ids,
        max_items=max_items,
        max_concurrency=max_concurrency,
        progress=progress,
    )
    return df.sort("DocumentId")
