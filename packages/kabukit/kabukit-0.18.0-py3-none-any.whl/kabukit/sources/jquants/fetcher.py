from __future__ import annotations

from typing import TYPE_CHECKING

from kabukit.utils import fetcher

from .client import JQuantsClient

if TYPE_CHECKING:
    import datetime
    from collections.abc import Iterable

    import polars as pl

    from kabukit.utils.fetcher import Progress


async def get_calendar() -> pl.DataFrame:
    """営業日カレンダーを取得する。

    Returns:
        pl.DataFrame: 営業日カレンダーを含むDataFrame。

    Raises:
        HTTPStatusError: APIリクエストが失敗した場合。
    """
    async with JQuantsClient() as client:
        return await client.get_calendar()


async def get_info(
    code: str | None = None,
    date: str | datetime.date | None = None,
    *,
    only_common_stocks: bool = True,
) -> pl.DataFrame:
    """上場銘柄一覧を取得する。

    Args:
        code (str, optional): 銘柄情報を取得する銘柄コード (例: "7203")。
            省略された場合、全銘柄が対象となる。
        date (str | datetime.date, optional): 銘柄情報を取得する日付
            (例: "2025-10-01")。
        only_common_stocks (bool, optional): 投資信託や優先株式を除く、
            普通株式のみを対象とするか。デフォルトはTrue。

    Returns:
        pl.DataFrame: 銘柄情報を含むDataFrame。

    Raises:
        HTTPStatusError: APIリクエストが失敗した場合。
    """
    async with JQuantsClient() as client:
        return await client.get_info(code, date, only_common_stocks=only_common_stocks)


async def get_target_codes() -> list[str]:
    """分析対象となる、普通株式の銘柄コードのリストを返す。

    Returns:
        list[str]: 分析対象となる銘柄コードのリスト。
    """
    info = await get_info(only_common_stocks=True)
    return info.get_column("Code").to_list()


async def get_statements(
    codes: Iterable[str] | str | None = None,
    /,
    date: str | datetime.date | None = None,
    max_items: int | None = None,
    max_concurrency: int = 12,
    progress: Progress | None = None,
) -> pl.DataFrame:
    """四半期毎の決算短信サマリーおよび業績・配当の修正に関する開示情報を取得する。

    Args:
        codes (Iterable[str] | str, optional): 財務情報を取得する銘柄のコード。
            省略された場合、全銘柄が対象となる。
        date (str | datetime.date, optional): 銘柄情報を取得する日付
            (例: "2025-10-01")。
        max_items (int | None, optional): 取得する銘柄数の上限。
            指定しないときはすべての銘柄が対象となる。
        max_concurrency (int | None, optional): 同時に実行するリクエストの最大数。
            デフォルトは12。
        progress (Progress | None, optional): 進捗表示のための関数。
            tqdm, marimoなどのライブラリを使用できる。
            指定しないときは進捗表示は行われない。

    Returns:
        pl.DataFrame: 財務情報を含むDataFrame。

    Raises:
        HTTPStatusError: APIリクエストが失敗した場合。
    """
    if isinstance(codes, str) or (codes is None and date):
        async with JQuantsClient() as client:
            return await client.get_statements(codes, date)

    if codes is None:
        codes = await get_target_codes()

    data = await fetcher.get(
        JQuantsClient,
        JQuantsClient.get_statements,
        codes,
        max_items=max_items,
        max_concurrency=max_concurrency,
        progress=progress,
    )
    return data.sort("Code", "Date")


async def get_prices(
    codes: Iterable[str] | str | None = None,
    /,
    date: str | datetime.date | None = None,
    max_items: int | None = None,
    max_concurrency: int = 8,
    progress: Progress | None = None,
) -> pl.DataFrame:
    """日々の株価四本値を取得する。

    株価は分割・併合を考慮した調整済み株価（小数点第２位四捨五入）と調整前の株価を取得できる。

    Args:
        codes (Iterable[str] | str, optional): 株価情報を取得する銘柄のコード。
            省略された場合、全銘柄が対象となる。
        date (str | datetime.date, optional): 株価情報を取得する日付
            (例: "2025-10-01")。
        max_items (int | None, optional): 取得する銘柄数の上限。
            指定しないときはすべての銘柄が対象となる。
        max_concurrency (int | None, optional): 同時に実行するリクエストの最大数。
            デフォルトは8。
        progress (Progress | None, optional): 進捗表示のための関数。
            tqdm, marimoなどのライブラリを使用できる。
            指定しないときは進捗表示は行われない。

    Returns:
        pl.DataFrame: 日々の株価四本値を含むDataFrame。

    Raises:
        HTTPStatusError: APIリクエストが失敗した場合。
    """
    if isinstance(codes, str) or (codes is None and date):
        async with JQuantsClient() as client:
            return await client.get_prices(codes, date)

    if codes is None:
        codes = await get_target_codes()

    data = await fetcher.get(
        JQuantsClient,
        JQuantsClient.get_prices,
        codes,
        max_items=max_items,
        max_concurrency=max_concurrency,
        progress=progress,
    )
    return data.sort("Code", "Date")
