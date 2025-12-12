from __future__ import annotations

import re
from dataclasses import dataclass
from typing import TYPE_CHECKING

from kabukit.sources.utils import get_soup
from kabukit.utils.datetime import parse_date, parse_time

if TYPE_CHECKING:
    import datetime
    from collections.abc import Iterator

    from bs4.element import Tag


DATE_PATTERN = re.compile(r"I_list_001_(\d{8})\.html")


def iter_dates(html: str, /) -> Iterator[datetime.date]:
    soup = get_soup(html)
    daylist = soup.find("select", attrs={"name": "daylist"})

    if not daylist:
        return

    for option in daylist.find_all("option"):
        value = option.get("value", "")
        if isinstance(value, str) and (m := DATE_PATTERN.search(value)):
            yield parse_date(m.group(1))


PAGER_PATTERN = re.compile(r"pagerLink\('I_list_(\d+)_\d+\.html'\)")


def iter_page_numbers(html: str, /) -> Iterator[int]:
    soup = get_soup(html)
    div = soup.find("div", attrs={"id": "pager-box-top"})

    if div is None:
        return

    for m in PAGER_PATTERN.finditer(str(div)):
        yield int(m.group(1))


@dataclass
class Item:
    """TDnet開示情報一覧の各項目を保持するデータクラス。"""

    code: str
    """銘柄コード"""
    disclosed_date: datetime.date | None
    """開示日時"""
    disclosed_time: datetime.time
    """開示時刻"""
    company: str
    """会社名"""
    title: str
    """表題"""
    pdf_url: str | None
    """PDFのURL"""
    xbrl_url: str | None
    """XBRLのURL"""
    update_status: str | None
    """更新履歴"""

    def to_dict(self) -> dict[str, str | datetime.date | datetime.time | None]:
        """Itemオブジェクトを辞書形式に変換する。

        Returns:
            dict[str, str | datetime.date | None]: Polars DataFrameの行として
                適した辞書。
        """
        return {
            "Code": self.code,
            "DisclosedDate": self.disclosed_date,
            "DisclosedTime": self.disclosed_time,
            "Company": self.company,
            "Title": self.title,
            "PdfUrl": self.pdf_url,
            "XbrlUrl": self.xbrl_url,
            "UpdateStatus": self.update_status,
        }


def iter_items(html: str, /) -> Iterator[Item]:
    soup = get_soup(html)
    if table := soup.find("table", attrs={"id": "main-list-table"}):
        yield from (parse_item(tr) for tr in table.find_all("tr"))


def parse_item(tag: Tag, /) -> Item:
    tds = tag.find_all("td")

    return Item(
        code=tds[1].get_text(strip=True),
        disclosed_date=None,
        disclosed_time=parse_time(tds[0].get_text(strip=True)),
        company=tds[2].get_text(strip=True),
        title=tds[3].get_text(strip=True),
        pdf_url=get_url(tds[3]),
        xbrl_url=get_url(tds[4]),
        update_status=tds[6].get_text(strip=True) or None,
    )


def get_url(tag: Tag, /) -> str | None:
    if a := tag.find("a"):
        href = a.get("href")
        if isinstance(href, str):
            return href

    return None
