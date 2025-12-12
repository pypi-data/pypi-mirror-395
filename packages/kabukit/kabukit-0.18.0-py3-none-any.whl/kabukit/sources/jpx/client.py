from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from kabukit.sources.client import Client

from .parser import iter_shares_html_urls, iter_shares_pdf_urls, parse_shares

if TYPE_CHECKING:
    from collections.abc import AsyncIterator

    import polars as pl

BASE_URL = "https://www.jpx.co.jp"
SHARES_URL = "/listing/co/01.html"


class JpxClient(Client):
    """JPXと非同期に対話するためのクライアント。

    `httpx.AsyncClient` をラップし、取得したHTMLのパース、
    `polars.DataFrame` への変換などを行う。

    Attributes:
        client (httpx.AsyncClient): APIリクエストを行うための非同期HTTPクライアント。
    """

    base_url: ClassVar[str] = BASE_URL

    async def iter_shares_html_urls(self) -> AsyncIterator[str]:
        """上場株式数データが掲載されたHTMLページのURLを取得する。

        Yields:
            str: 上場株式数データが掲載されたHTMLページのURL。
        """
        response = await self.get(SHARES_URL)

        for html_url in iter_shares_html_urls(response.text):
            yield html_url

    async def _iter_shares_pdf_urls(self, html_url: str) -> AsyncIterator[str]:
        """指定されたHTMLページから上場株式数PDFのURLを取得する。

        Args:
            html_url (str): PDFのURLを抽出する対象のHTMLページのURL。

        Yields:
            str: 上場株式数PDFのURL。
        """
        response = await self.get(html_url)

        for pdf_url in iter_shares_pdf_urls(response.text):
            yield pdf_url

    async def iter_shares_pdf_urls(
        self,
        html_url: str | None = None,
    ) -> AsyncIterator[str]:
        """上場株式数PDFのURLを取得する。

        引数 `html_url` が指定された場合はそのページからのみURLを取得する。
        指定されない場合は、利用可能な全てのバックナンバーページを巡回して
        PDFのURLを取得する。

        Args:
            html_url (str | None, optional): PDFのURLを抽出する対象の
                HTMLページのURL。 指定しない場合は全ページが対象となる。

        Yields:
            str: 上場株式数PDFのURL。
        """
        if html_url:
            async for pdf_url in self._iter_shares_pdf_urls(html_url):
                yield pdf_url

        else:
            async for url in self.iter_shares_html_urls():
                async for pdf_url in self._iter_shares_pdf_urls(url):
                    yield pdf_url

    async def get_shares(self, pdf_url: str) -> pl.DataFrame:
        """指定されたPDFのURLから上場株式数データを取得し、DataFrameとして返す。

        PDFのパース処理はCPUバウンドです。
        `executor`属性によって非同期実行の方法を指定できます。

        Args:
            pdf_url (str): 上場株式数データが記載されたPDFのURL。

        Returns:
            pl.DataFrame: 上場株式数データを含むPolars DataFrame。
        """
        response = await self.get(pdf_url)
        return await self.run_in_executor(parse_shares, response.content)
