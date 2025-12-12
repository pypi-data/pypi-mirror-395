from __future__ import annotations

from enum import StrEnum
from typing import TYPE_CHECKING, ClassVar

import polars as pl

from kabukit.sources.client import Client
from kabukit.sources.datetime import with_date
from kabukit.utils.config import get_config_value
from kabukit.utils.params import get_params

from .parser import parse_csv, parse_pdf, parse_xbrl
from .transform import transform_list

if TYPE_CHECKING:
    import datetime
    from concurrent.futures import Executor


API_VERSION = "v2"
BASE_URL = f"https://api.edinet-fsa.go.jp/api/{API_VERSION}"


class AuthKey(StrEnum):
    """EDINET認証のための環境変数キー。"""

    API_KEY = "EDINET_API_KEY"


class EdinetClient(Client):
    """EDINET API v2と非同期に対話するためのクライアント。

    `httpx.AsyncClient` をラップし、APIキー認証、指数関数的バックオフを
    用いたリトライ処理、APIレスポンスの `polars.DataFrame` への変換などを行う。

    Attributes:
        client (httpx.AsyncClient): APIリクエストを行うための非同期HTTPクライアント。
    """

    base_url: ClassVar[str] = BASE_URL

    def __init__(
        self,
        api_key: str | None = None,
        executor: Executor | None = None,
    ) -> None:
        super().__init__(executor=executor)
        self.set_api_key(api_key)

    def set_api_key(self, api_key: str | None = None) -> None:
        """HTTPクエリパラメータにAPIキーを設定する。

        Args:
            api_key: 設定するAPIキー。Noneの場合、設定ファイルまたは
                環境変数から読み込む。
        """
        if api_key is None:
            api_key = get_config_value(AuthKey.API_KEY)

        if api_key:
            self.client.params = {"Subscription-Key": api_key}

    async def get_count(self, date: str | datetime.date) -> int:
        """指定したファイル日付の提出書類の数を取得する。

        Args:
            date (str | datetime.date): 取得するファイル日付。

        Returns:
            int: 指定日の提出書類数。
        """
        params = get_params(date=date, type=1)
        response = await self.get("/documents.json", params)
        data = response.json()
        metadata = data["metadata"]

        if metadata["status"] != "200":
            return 0

        return metadata["resultset"]["count"]

    async def get_list(
        self,
        date: str | datetime.date,
        *,
        transform: bool = True,
    ) -> pl.DataFrame:
        """指定したファイル日付の提出書類一覧を取得する。

        Args:
            date (str | datetime.date): 取得するファイル日付。
            transform (bool, optional): Trueのとき、取得したデータを整形・加工する。
                デフォルトはTrue。

        Returns:
            pl.DataFrame: 提出書類一覧を格納したDataFrame。
        """
        params = get_params(date=date, type=2)
        response = await self.get("/documents.json", params)
        data = response.json()

        if "results" not in data:
            return pl.DataFrame()

        df = pl.DataFrame(data["results"], infer_schema_length=None)

        if not transform:
            return df

        df = transform_list(df, date)

        if df.is_empty():
            return pl.DataFrame()

        return await with_date(df)

    async def get_pdf(self, doc_id: str) -> pl.DataFrame:
        """PDF形式の書類を取得し、テキストを抽出する。

        Args:
            doc_id: EDINETの書類ID。

        Returns:
            pl.DataFrame: 抽出したテキストデータを含むDataFrame。
        """
        response = await self.get(f"/documents/{doc_id}", {"type": 2})

        if response.headers["content-type"] != "application/pdf":
            return pl.DataFrame()

        return parse_pdf(response.content, doc_id)

    async def get_zip(self, doc_id: str, doc_type: int) -> bytes | None:
        """ZIP形式の書類を取得する。

        doc_typeの値:

            1 提出本文書及び監査報告書 ZIP 形式
            2 PDF PDF 形式
            3 代替書面・添付文書 ZIP 形式
            4 英文ファイル ZIP 形式
            5 CSV ZIP 形式

        Args:
            doc_id: EDINETの書類ID。
            doc_type: 書類タイプ (通常は5:CSV)。

        Returns:
            bytes | None: ZIPファイルのバイナリデータ。
                Noneの場合、ZIPが存在しない。
        """
        response = await self.get(f"/documents/{doc_id}", {"type": doc_type})

        if response.headers["content-type"] == "application/octet-stream":
            return response.content

        return None

    async def get_xbrl(self, doc_id: str) -> str | None:
        """XBRL形式の書類を取得する。

        Args:
            doc_id: EDINETの書類ID。

        Returns:
            str | None: XBRL形式のテキストデータ。
                Noneの場合、XBRLが存在しない。
        """

        content = await self.get_zip(doc_id, doc_type=1)

        if content is None:
            return None

        return parse_xbrl(content)

    async def get_csv(self, doc_id: str) -> pl.DataFrame:
        """CSV形式の書類(XBRL)を取得し、DataFrameに変換する。

        書類取得API (`type=5`) で取得したZIPファイルの中からCSVファイルを
        探し出し、DataFrameとして読み込む。

        Args:
            doc_id: EDINETの書類ID。

        Returns:
            pl.DataFrame: CSVデータを含むDataFrame。
        """
        content = await self.get_zip(doc_id, doc_type=5)

        if content is None:
            return pl.DataFrame()

        return parse_csv(content, doc_id)

    async def get_document(self, doc_id: str, *, pdf: bool = False) -> pl.DataFrame:
        """指定したIDの書類を取得する。

        Args:
            doc_id: EDINETの書類ID。
            pdf: Trueの場合PDF形式、Falseの場合CSV形式の書類を取得する。

        Returns:
            pl.DataFrame: 書類データを含むDataFrame。
        """
        if pdf:
            return await self.get_pdf(doc_id)

        return await self.get_csv(doc_id)
