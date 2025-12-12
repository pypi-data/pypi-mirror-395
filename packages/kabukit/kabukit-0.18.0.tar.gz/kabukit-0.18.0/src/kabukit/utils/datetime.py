from __future__ import annotations

import calendar
import datetime
from typing import Literal, overload
from zoneinfo import ZoneInfo


def parse_date(date_string: str, fmt: str | None = None, /) -> datetime.date:
    """文字列を日付オブジェクトに変換する。

    Args:
        date_string (str): 変換する日付文字列。
        fmt (str | None, optional): 日付文字列のフォーマット。

    Returns:
        datetime.date: 変換された日付オブジェクト。
    """
    if fmt is None:
        fmt = "%Y-%m-%d" if "-" in date_string else "%Y%m%d"

    return (
        datetime.datetime.strptime(date_string, fmt)
        .replace(tzinfo=ZoneInfo("Asia/Tokyo"))
        .date()
    )


def parse_year_month(year_month_string: str, /) -> datetime.date:
    """'年/月'の文字列を日付オブジェクトに変換する。

    月末日を日付として扱う。

     Args:
         year_month_string (str): 変換する日付文字列。

     Returns:
         datetime.date: 変換された日付オブジェクト。
    """
    year, month = map(int, year_month_string.split("/"))
    day = calendar.monthrange(year, month)[1]
    return datetime.date(year, month, day)


def parse_month_day(month_day_string: str, /) -> datetime.date:
    """'月/日'の文字列を日付オブジェクトに変換する。

    当日より未来の日付の場合、前年の日付として扱う。

    Args:
        month_day_string (str): 変換する日付文字列。

    Returns:
        datetime.date: 変換された日付オブジェクト。
    """
    ref = today()
    date = parse_date(f"{ref.year}/{month_day_string}", "%Y/%m/%d")

    if date > ref:
        return date.replace(year=ref.year - 1)

    return date


def parse_time(time_string: str, fmt: str | None = None, /) -> datetime.time:
    """文字列を時刻オブジェクトに変換する。

    Args:
        time_string (str): 変換する日時文字列。
        fmt (str | None, optional): 日時文字列のフォーマット。

    Returns:
        datetime.time: 変換された時刻オブジェクト。
    """
    if fmt is None:
        fmt = "%H:%M"

    return (
        datetime.datetime.strptime(time_string, fmt)
        .replace(tzinfo=ZoneInfo("Asia/Tokyo"))
        .time()
    )


@overload
def today(*, as_str: Literal[True]) -> str: ...


@overload
def today(*, as_str: Literal[False] = False) -> datetime.date: ...


def today(*, as_str: Literal[True, False] = False) -> datetime.date | str:
    """今日の日付を取得する。

    Returns:
        datetime.date: 今日の日付。
    """
    date = datetime.datetime.now(ZoneInfo("Asia/Tokyo")).date()

    if as_str:
        return date.strftime("%Y-%m-%d")

    return date


def get_past_dates(
    days: int | None = None,
    years: int | None = None,
) -> list[datetime.date]:
    """過去days日またはyears年の日付リストを返す。

    Args:
        days (int | None): 過去days日の日付リストを取得する。
        years (int | None): 過去years年の日付リストを取得する。
            daysが指定されている場合は無視される。
    """
    end_date = today()

    if days is not None:
        start_date = end_date - datetime.timedelta(days=days)
    elif years is not None:
        start_date = end_date.replace(year=end_date.year - years)
    else:
        msg = "daysまたはyearsのいずれかを指定してください。"
        raise ValueError(msg)

    return [
        start_date + datetime.timedelta(days=i)
        for i in range(1, (end_date - start_date).days + 1)
    ]
