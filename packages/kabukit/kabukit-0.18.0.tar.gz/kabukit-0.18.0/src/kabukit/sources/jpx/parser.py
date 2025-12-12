"""JPXから上場株式数データを解析するためのモジュール。

このモジュールは、JPXのウェブサイトから上場株式数に関するHTMLリンクを抽出し、
PDFファイルの内容を解析して、株式数データをPolars DataFrameとして提供します。
"""

from __future__ import annotations

import calendar
import datetime
import io
import re
from dataclasses import dataclass
from typing import TYPE_CHECKING

import polars as pl
from pypdf import PdfReader

from kabukit.sources.utils import get_soup

if TYPE_CHECKING:
    from collections.abc import Iterator


def iter_shares_html_urls(html: str, /) -> Iterator[str]:
    """HTMLコンテンツから、上場株式数のPDFリンクが掲載されたHTMLのURLを抽出する。

    Args:
        html (str): 解析対象のHTML文字列。

    Yields:
        str: 上場株式数のPDFリンクが掲載されたHTMLのURL。
    """
    soup = get_soup(html)
    select = soup.find("select", class_="backnumber")

    if select is None:
        return

    for option in select.find_all("option"):
        value = option.get("value")
        if isinstance(value, str):
            yield value


def iter_shares_pdf_urls(html: str, /) -> Iterator[str]:
    """HTMLコンテンツから、上場株式数のPDFコンテンツのURLを抽出する。

    Args:
        html (str): 解析対象のHTML文字列。

    Yields:
        str: 上場株式数のPDFコンテンツのURL。
    """
    soup = get_soup(html)

    pattern = re.compile(r"HP-\d{4}\.\d{1,2}\.pdf")

    for a in soup.find_all("a", href=pattern):
        href = a.get("href")
        if isinstance(href, str):
            yield href


@dataclass
class Shares:
    """上場株式数データを保持するデータクラス。"""

    company: str
    """会社名"""
    code: str
    """銘柄コード"""
    number: int
    """上場株式数"""
    year: int
    """データが所属する年"""
    month: int
    """データが所属する月"""

    def to_dict(self) -> dict[str, str | int | datetime.date]:
        """Sharesオブジェクトを辞書形式に変換する。

        Returns:
            dict[str, str | int | datetime.date]: Polars DataFrameの行として
                適した辞書。
        """
        day = calendar.monthrange(self.year, self.month)[1]
        date = datetime.date(self.year, self.month, day)

        return {
            "Date": date,
            "Code": self.code,
            "Company": self.company,
            "IssuedShares": self.number,
        }


def iter_shares_pages(content: bytes, /) -> Iterator[str]:
    """PDFコンテンツから上場株式数データを含むページテキストを抽出する。

    PDF内の特定のヘッダーを検出し、そのページ以降のテキストを抽出する。

    Args:
        content (bytes): PDFファイルのバイトコンテンツ。

    Yields:
        str: 上場株式数データを含むページのテキスト。
    """
    reader = PdfReader(io.BytesIO(content))

    header = r"^\s*\d{4}年\d{1,2}月分.+会社別\n会社名\s+（コード）\s+月末現在上場株式数"
    pattern = re.compile(header, re.DOTALL)
    in_shares = False

    for page in reader.pages:
        text = page.extract_text()
        if in_shares:
            yield text
        elif pattern.match(text):
            in_shares = True
            yield text


def iter_shares(page: str, /) -> Iterator[Shares]:
    """単一のページテキストから上場株式数データを抽出する。

    Args:
        page (str): 上場株式数データを含むページのテキスト。

    Yields:
        Shares: 解析された`Shares`オブジェクト。
    """
    m = re.match(r"^\s*(\d{4})年(\d{1,2})月分\n", page)
    if not m:
        return

    year, month = map(int, m.groups())

    pattern = re.compile(r"^(.+?)\s+\(([0-9A-Z]{4})\)\s+([\d,]+)\s*")

    for line in page.splitlines():
        m = pattern.match(line)
        if m:
            company, code, number = m.groups()
            number = int(number.replace(",", ""))
            yield Shares(company, code, number, year, month)


def parse_shares(content: bytes, /) -> pl.DataFrame:
    """PDFコンテンツを解析し、上場株式数データのPolars DataFrameを生成する。

    Args:
        content (bytes): PDFファイルのバイトコンテンツ。

    Returns:
        pl.DataFrame: 上場株式数データを含むPolars DataFrame。
    """
    pages = iter_shares_pages(content)
    shares = (share.to_dict() for page in pages for share in iter_shares(page))
    return pl.DataFrame(shares)
