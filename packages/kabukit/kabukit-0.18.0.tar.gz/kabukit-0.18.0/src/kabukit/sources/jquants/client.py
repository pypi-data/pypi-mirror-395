from __future__ import annotations

from enum import StrEnum
from typing import TYPE_CHECKING, Any, ClassVar

import polars as pl

from kabukit.sources.client import Client
from kabukit.sources.datetime import with_date
from kabukit.utils.config import get_config_value
from kabukit.utils.params import get_params

from .transform import calendar, info, prices, statements, topix

if TYPE_CHECKING:
    import datetime
    from collections.abc import AsyncIterator
    from concurrent.futures import Executor

    from httpx import HTTPStatusError  # noqa: F401


API_VERSION = "v1"
BASE_URL = f"https://api.jquants.com/{API_VERSION}"


class AuthKey(StrEnum):
    """J-Quants認証のための環境変数キー。"""

    MAILADDRESS = "J_QUANTS_MAILADDRESS"
    PASSWORD = "J_QUANTS_PASSWORD"  # noqa: S105
    ID_TOKEN = "J_QUANTS_ID_TOKEN"  # noqa: S105


class JQuantsClient(Client):
    """J-Quants APIと非同期に対話するためのクライアント。

    `httpx.AsyncClient` をラップし、認証トークンの管理、ページネーションの
    自動処理、APIレスポンスの `polars.DataFrame` への変換などを行う。

    Attributes:
        client (httpx.AsyncClient): APIリクエストを行うための非同期HTTPクライアント。
    """

    base_url: ClassVar[str] = BASE_URL

    def __init__(
        self,
        id_token: str | None = None,
        executor: Executor | None = None,
    ) -> None:
        super().__init__(executor=executor)
        self.set_id_token(id_token)

    def set_id_token(self, id_token: str | None = None) -> None:
        """HTTPヘッダーにIDトークンを設定する。

        Args:
            id_token: 設定するIDトークン。Noneの場合、設定ファイルまたは
                環境変数から読み込む。
        """
        if id_token is None:
            id_token = get_config_value(AuthKey.ID_TOKEN)

        if id_token:
            self.client.headers["Authorization"] = f"Bearer {id_token}"

    async def post(self, url: str, json: Any | None = None) -> Any:
        """指定されたURLにPOSTリクエストを送信する。

        Args:
            url: POSTリクエストのURLパス。
            json: リクエストボディのJSONペイロード。

        Returns:
            APIからのJSONレスポンス。

        Raises:
            HTTPStatusError: APIリクエストがHTTPエラーステータスを返した場合。
        """
        response = await self.client.post(url, json=json)
        response.raise_for_status()
        return response.json()

    async def auth(
        self,
        mailaddress: str | None = None,
        password: str | None = None,
    ) -> str:
        """メールアドレスとパスワードで認証し、IDトークンを返す。

        Args:
            mailaddress (str | None): J-Quantsに登録したメールアドレス。
                Noneの場合、設定ファイルまたは環境変数から読み込む。
            password (str | None): J-Quantsのパスワード。
                Noneの場合、設定ファイルまたは環境変数から読み込む。

        Returns:
            str: 認証によって取得されたIDトークン。

        Raises:
            ValueError: メールアドレスまたはパスワードが指定されていない場合。
            HTTPStatusError: 認証APIリクエストが失敗した場合。
        """
        mailaddress = mailaddress or get_config_value(AuthKey.MAILADDRESS)
        password = password or get_config_value(AuthKey.PASSWORD)

        if not mailaddress or not password:
            msg = "メールアドレスとパスワードを指定するか、"
            msg += "環境変数に設定する必要がある。"
            raise ValueError(msg)

        json = {"mailaddress": mailaddress, "password": password}
        data = await self.post("/token/auth_user", json)
        refresh_token = data["refreshToken"]

        url = f"/token/auth_refresh?refreshtoken={refresh_token}"
        data = await self.post(url)
        id_token = data["idToken"]
        self.set_id_token(id_token)
        return id_token

    async def iter_pages(
        self,
        url: str,
        params: dict[str, Any] | None,
        name: str,
    ) -> AsyncIterator[pl.DataFrame]:
        """ページ分割されたAPIレスポンスを非同期に反復処理する。

        J-Quants APIのページネーション仕様（`pagination_key`）に対応し、
        複数ページにまたがるデータを自動的に取得する。

        Args:
            url: APIエンドポイントのURLパス。
            params: クエリパラメータの辞書。
            name: アイテムのリストを含むJSONレスポンスのキー。

        Yields:
            pl.DataFrame: データの各ページに対応するDataFrame。

        Raises:
            HTTPStatusError: APIリクエストが失敗した場合。
        """
        params = params or {}

        while True:
            response = await self.get(url, params)
            data = response.json()

            yield pl.DataFrame(data[name])

            if "pagination_key" in data:
                params["pagination_key"] = data["pagination_key"]
            else:
                break

    async def get_info(
        self,
        code: str | None = None,
        date: str | datetime.date | None = None,
        *,
        transform: bool = True,
        only_common_stocks: bool = True,
    ) -> pl.DataFrame:
        """上場銘柄一覧を取得する。

        Args:
            code (str, optional): 銘柄情報を取得する銘柄コード (例: "7203")。
            date (str | datetime.date, optional): 銘柄情報を取得する日付
                (例: "2025-10-01")。
            transform (bool, optional): 取得したデータを整形するかどうか。
                デフォルトはTrue。
            only_common_stocks (bool, optional): 投資信託や優先株式を除く、
                普通株式のみを対象とするか。デフォルトはTrue。

        Returns:
            pl.DataFrame: 銘柄情報を含むDataFrame。

        Raises:
            HTTPStatusError: APIリクエストが失敗した場合。
        """
        params = get_params(code=code, date=date)
        url = "/listed/info"
        response = await self.get(url, params)
        data = response.json()

        df = pl.DataFrame(data["info"])

        if not transform:
            return df

        if df.is_empty():
            return pl.DataFrame()

        return info.transform(df, only_common_stocks=only_common_stocks)

    async def get_statements(
        self,
        code: str | None = None,
        date: str | datetime.date | None = None,
        *,
        transform: bool = True,
    ) -> pl.DataFrame:
        """四半期毎の決算短信サマリーおよび業績・配当の修正に関する開示情報を取得する。

        Args:
            code (str, optional): 財務情報を取得する銘柄コード (例: "7203")。
            date (str | datetime.date, optional): 財務情報を取得する日付
                (例: "2025-10-01")。
            transform (bool, optional): 取得したデータを整形するかどうか。
                デフォルトはTrue。

        Returns:
            pl.DataFrame: 財務情報を含むDataFrame。

        Raises:
            ValueError: `code`と`date`が両方とも指定されない場合。
            HTTPStatusError: APIリクエストが失敗した場合。
        """
        if not code and not date:
            msg = "codeまたはdateのどちらかを指定する必要がある。"
            raise ValueError(msg)

        params = get_params(code=code, date=date)
        url = "/fins/statements"
        name = "statements"

        dfs = [df async for df in self.iter_pages(url, params, name)]
        df = pl.concat(dfs)

        if not transform:
            return df

        if df.is_empty():
            return pl.DataFrame()

        df = statements.transform(df)
        return await with_date(df)

    async def get_prices(
        self,
        code: str | None = None,
        date: str | datetime.date | None = None,
        from_: str | datetime.date | None = None,
        to: str | datetime.date | None = None,
        *,
        transform: bool = True,
    ) -> pl.DataFrame:
        """日々の株価四本値を取得する (prices/daily_quotes)。

        Args:
            code (str, optional): 株価を取得する銘柄コード (例: "7203")。
            date (str | datetime.date, optional): 株価を取得する日付
                (例: "2025-10-01")。`from_`または`to`とは併用不可。
            from_ (str | datetime.date, optional): 取得期間の開始日。
                `date`とは併用不可。
            to (str | datetime.date, optional): 取得期間の終了日。
                `date`とは併用不可。
            transform (bool, optional): 取得したデータを整形するかどうか。
                デフォルトはTrue。

        Returns:
            pl.DataFrame: 日々の株価四本値を含むDataFrame。

        Raises:
            ValueError: `date`と`from_`/`to`が同時に指定された場合。
            HTTPStatusError: APIリクエストが失敗した場合。
        """
        if not code and not date:
            msg = "codeまたはdateのどちらかを指定する必要がある。"
            raise ValueError(msg)

        if date and (from_ or to):
            msg = "dateとfrom/toを同時に指定することはできない。"
            raise ValueError(msg)

        params = get_params(code=code, date=date, from_=from_, to=to)

        url = "/prices/daily_quotes"
        name = "daily_quotes"

        dfs = [df async for df in self.iter_pages(url, params, name)]
        df = pl.concat(dfs)

        if not transform:
            return df

        if df.is_empty():
            return pl.DataFrame()

        return prices.transform(df)

    async def get_announcement(self) -> pl.DataFrame:
        """翌日発表予定の決算情報を取得する (fins/announcement)。

        Returns:
            pl.DataFrame: 翌日発表予定の決算開示情報を含むDataFrame。

        Raises:
            HTTPStatusError: APIリクエストが失敗した場合。
        """
        url = "fins/announcement"
        name = "announcement"

        dfs = [df async for df in self.iter_pages(url, {}, name)]
        df = pl.concat(dfs)

        if df.is_empty():
            return pl.DataFrame()

        return df.with_columns(pl.col("Date").str.to_date("%Y-%m-%d"))

    async def get_trades_spec(
        self,
        section: str | None = None,
        from_: str | datetime.date | None = None,
        to: str | datetime.date | None = None,
    ) -> pl.DataFrame:
        """投資部門別売買状況を取得する (markets/trades_spec)。

        Args:
            section (str, optional): 絞り込み対象のセクション (例: "TSE")。
            from_ (str | datetime.date, optional): 取得期間の開始日。
            to (str | datetime.date, optional): 取得期間の終了日。

        Returns:
            pl.DataFrame: 投資部門別売買状況を含むDataFrame。

        Raises:
            HTTPStatusError: APIリクエストが失敗した場合。
        """
        params = get_params(section=section, from_=from_, to=to)

        url = "/markets/trades_spec"
        name = "trades_spec"

        dfs = [df async for df in self.iter_pages(url, params, name)]
        df = pl.concat(dfs)

        if df.is_empty():
            return pl.DataFrame()

        return df.with_columns(pl.col("^.*Date$").str.to_date("%Y-%m-%d"))

    async def get_topix(
        self,
        from_: str | datetime.date | None = None,
        to: str | datetime.date | None = None,
    ) -> pl.DataFrame:
        """TOPIXの時系列データを取得する (indices/topix)。

        Args:
            from_ (str | datetime.date, optional): 取得期間の開始日。
            to (str | datetime.date, optional): 取得期間の終了日。

        Returns:
            pl.DataFrame: 日次のTOPIX指数データを含むDataFrame。

        Raises:
            HTTPStatusError: APIリクエストが失敗した場合。
        """
        params = get_params(from_=from_, to=to)

        url = "/indices/topix"
        name = "topix"

        dfs = [df async for df in self.iter_pages(url, params, name)]
        df = pl.concat(dfs)

        if df.is_empty():
            return pl.DataFrame()

        return topix.transform(df)

    async def get_calendar(
        self,
        holidaydivision: str | None = None,
        from_: str | datetime.date | None = None,
        to: str | datetime.date | None = None,
    ) -> pl.DataFrame:
        """市場の営業日カレンダーを取得する (markets/trading_calendar)。

        Args:
            holidaydivision (str, optional): 祝日区分
                ("0":非営業日, "1":営業日など)。
            from_ (str | datetime.date, optional): 取得期間の開始日。
            to (str | datetime.date, optional): 取得期間の終了日。

        Returns:
            pl.DataFrame: 市場の営業日・休業日データを含むDataFrame。

        Raises:
            HTTPStatusError: APIリクエストが失敗した場合。
        """
        params = get_params(holidaydivision=holidaydivision, from_=from_, to=to)

        url = "/markets/trading_calendar"
        name = "trading_calendar"

        dfs = [df async for df in self.iter_pages(url, params, name)]
        df = pl.concat(dfs)

        if df.is_empty():
            return pl.DataFrame()

        return calendar.transform(df)
