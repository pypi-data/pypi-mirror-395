from __future__ import annotations

import datetime
import json
import re
from typing import TYPE_CHECKING, Any

import polars as pl
from bs4 import Tag

from kabukit.sources.utils import get_soup
from kabukit.utils.datetime import parse_month_day, parse_time, parse_year_month, today

if TYPE_CHECKING:
    from collections.abc import Iterator


def _get(text: str, pattern: re.Pattern[str]) -> re.Match[str] | None:
    soup = get_soup(text)
    script = soup.find("script", string=pattern)  # pyright: ignore[reportCallIssue, reportArgumentType, reportUnknownVariableType], # ty: ignore[no-matching-overload]

    if not isinstance(script, Tag):
        return None

    return pattern.search(script.text)


PRELOADED_STATE_PATTERN = re.compile(r"window\.__PRELOADED_STATE__\s*=\s*(\{.*\})")


def get_preloaded_state(text: str, /) -> dict[str, Any]:
    """HTMLテキストから `__PRELOADED_STATE__` を抽出して辞書として返す。

    Args:
        text: HTMLテキスト。

    Returns:
        抽出した状態辞書。見つからなかった場合は空の辞書。
    """
    if match := _get(text, PRELOADED_STATE_PATTERN):
        return json.loads(match.group(1))

    return {}


def parse_quote(text: str) -> pl.DataFrame:
    state = get_preloaded_state(text)

    if not state:
        return pl.DataFrame()

    return pl.DataFrame(dict(iter_quote(state)))


def iter_quote(state: dict[str, Any], /) -> Iterator[tuple[str, Any]]:
    yield from iter_price(state)
    yield from iter_previous_price(state)
    yield from iter_index(state)
    yield from iter_press_release(state)
    yield from iter_performance(state)


def iter_price(state: dict[str, Any], /) -> Iterator[tuple[str, Any]]:
    """状態辞書から現在の株価を生成する。

    Args:
        state (dict[str, Any]): 状態辞書。

    Yields:
        tuple[str, Any]: 現在の株価と日時。
    """
    detail: dict[str, Any] = state["mainStocksPriceBoard"]["priceBoard"]

    yield "Price", _float_or_none(detail["price"])

    date_str = detail["priceDateTime"]
    date, time = _parse_datetime(date_str)

    yield "PriceDate", date
    yield "PriceTime", time


def iter_previous_price(state: dict[str, Any], /) -> Iterator[tuple[str, Any]]:
    """状態辞書から前日の株価を生成する。

    Args:
        state (dict[str, Any]): 状態辞書。

    Yields:
        tuple[str, Any]: 前日の株価と日時。
    """
    detail: dict[str, Any] = state["mainStocksDetail"]["detail"]

    yield "PreviousPrice", _float_or_none(detail["previousPrice"])

    date_str = detail["previousPriceDate"]
    date, time = _parse_datetime(date_str)

    yield "PreviousPriceDate", date
    yield "PreviousPriceTime", time


def iter_index(state: dict[str, Any], /) -> Iterator[tuple[str, Any]]:
    """状態辞書の mainStocksDetail セクションの指標値を生成する。

    Args:
        state (dict[str, Any]): 状態辞書。

    Yields:
        tuple[str, Any]: mainStocksDetail セクション内の主な指標値。
    """
    index: dict[str, Any] = state["mainStocksDetail"]["referenceIndex"]

    yield "IssuedShares", int(index["sharesIssued"].replace(",", ""))
    date_str = index["sharesIssuedDate"]
    date, _ = _parse_datetime(date_str)
    yield "IssuedSharesDate", date

    for p, name in [("b", "BookValue"), ("e", "Earnings"), ("d", "Dividend")]:
        yield f"{name}PerShare", _float_or_none(index[f"{p}ps"])
        date, _ = _parse_datetime(index[f"{p}psDate"])
        yield f"{name}PerShareDate", date


def iter_press_release(state: dict[str, Any], /) -> Iterator[tuple[str, Any]]:
    """状態辞書の mainStocksPressReleaseSummary セクションの主な値を生成する。

    Args:
        state (dict[str, Any]): 状態辞書。

    Yields:
        tuple[str, Any]: mainStocksPressReleaseSummary セクション内の主な値。
    """
    pr: dict[str, Any] = state["mainStocksPressReleaseSummary"]

    if "summary" not in pr:
        yield "PressReleaseSummary", None
        yield "PressReleaseDate", None
        yield "PressReleaseTime", None
        return

    yield "PressReleaseSummary", pr["summary"]
    disclosed_datetime = datetime.datetime.fromisoformat(pr["disclosedTime"])
    yield "PressReleaseDate", disclosed_datetime.date()
    yield "PressReleaseTime", disclosed_datetime.time()


def iter_performance(state: dict[str, Any]) -> Iterator[tuple[str, Any]]:
    """状態辞書の stockPerformance セクションの主な値を生成する。

    Args:
        state (dict[str, Any]): 状態辞書。

    Yields:
        tuple[str, Any]: stockPerformance セクション内の主な値。
    """
    info: dict[str, Any] | None = state["stockPerformance"].get("summaryInfo", None)

    columns = [
        "PerformanceSummary",
        "PerformancePotential",
        "PerformanceStability",
        "PerformanceProfitability",
        "PerformanceDate",
        "PerformanceTime",
    ]

    if info is None:
        for column in columns:
            yield column, None
        return

    for k, key in enumerate(["summary", "potential", "stability", "profitability"]):
        yield columns[k], info[key]

    update_datetime = datetime.datetime.fromisoformat(info["updateTime"])
    yield columns[4], update_datetime.date()
    yield columns[5], update_datetime.time()


PRELOADED_STORE_PATTERN = re.compile(r'\\"preloadedStore\\":(.*)')


def get_preloaded_store(text: str, /) -> dict[str, Any]:
    """HTMLテキストから `preloadedStore` を抽出して辞書として返す。

    Args:
        text: HTMLテキスト。

    Returns:
        抽出した状態辞書。見つからなかった場合は空の辞書。
    """
    if match := _get(text, PRELOADED_STORE_PATTERN):
        if store := _extract_content(match.group(1)):
            store = store.replace('\\"', '"')
            return json.loads(store)

    return {}


def parse_performance(text: str) -> pl.DataFrame:
    store = get_preloaded_store(text)

    if not store:
        return pl.DataFrame()

    performance = store["performance"]["performance"]

    return pl.DataFrame(performance)


def _float_or_none(value: str) -> float | None:
    """文字列を浮動小数点数に変換する。変換できない場合は None を返す。"""
    if value == "---":
        return None

    return float(value.replace(",", ""))


def _parse_datetime(
    date_str: str,
) -> tuple[datetime.date, datetime.time] | tuple[None, None]:
    """月日/日付/時刻文字列を解釈する。"""
    if "-" in date_str:
        return None, None

    if re.match(r"^\d{4}/\d{2}$", date_str):
        # "2023/10" のような年月形式の場合
        return parse_year_month(date_str), datetime.time(0, 0)

    if "/" in date_str:
        # "10/29" のような日付形式の場合
        return parse_month_day(date_str), datetime.time(15, 30)  # 取引終了時刻を想定

    # "14:45" のような時刻形式の場合
    return today(), parse_time(date_str)


def _extract_content(text: str) -> str:
    """波括弧で囲まれたJSONコンテンツを抽出する。"""
    start_index = text.find("{")
    if start_index == -1:
        return ""

    brace_count = 0
    end_index = -1
    for i, char in enumerate(text[start_index:]):
        if char == "{":
            brace_count += 1
        elif char == "}":
            brace_count -= 1
            if brace_count == 0:
                end_index = start_index + i
                break

    if end_index == -1:
        return ""
    return text[start_index : end_index + 1]
