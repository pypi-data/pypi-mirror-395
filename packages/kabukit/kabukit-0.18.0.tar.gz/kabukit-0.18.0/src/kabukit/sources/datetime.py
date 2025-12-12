from __future__ import annotations

import asyncio
import datetime
from typing import final

import polars as pl

# pyright: reportImportCycles=false


@final
class _CalendarCacheManager:
    def __init__(self) -> None:
        self._holidays: list[datetime.date] | None = None
        self._lock = asyncio.Lock()

    async def get_holidays(self) -> list[datetime.date]:
        from kabukit.sources.jquants.client import JQuantsClient

        async with self._lock:
            if self._holidays is None:
                async with JQuantsClient() as client:
                    df = await client.get_calendar()

                holidays = df.filter(pl.col("IsHoliday"))["Date"]
                self._holidays = holidays.to_list()

            return self._holidays


_calendar_cache_manager = _CalendarCacheManager()


async def with_date(df: pl.DataFrame) -> pl.DataFrame:
    """`Date`列を追加する。

    日付が休日のとき、または、時刻が境界時刻以降の場合、Dateを日付の翌営業日に設定する。

    日付の境界時刻は、

    - DisclosedTime: 15時30分
    - SubmittedTime: 15時00分

    とする。
    """
    holidays = await _calendar_cache_manager.get_holidays()
    return _with_date(df, holidays)


def _with_date(df: pl.DataFrame, holidays: list[datetime.date]) -> pl.DataFrame:
    if "DisclosedDate" in df.columns and "DisclosedTime" in df.columns:
        prefix, limit = "Disclosed", datetime.time(15, 30)
    elif "SubmittedDate" in df.columns and "SubmittedTime" in df.columns:
        prefix, limit = "Submitted", datetime.time(15, 0)
    else:
        msg = "DataFrame must contain either DisclosedDate and DisclosedTime"
        msg += " or SubmittedDate and SubmittedTime columns."
        raise ValueError(msg)

    is_null = pl.col(f"{prefix}Time").is_null()
    is_late = pl.col(f"{prefix}Time") >= limit

    return df.select(
        pl.when(is_null | is_late)
        .then(pl.col(f"{prefix}Date") + datetime.timedelta(days=1))
        .otherwise(pl.col(f"{prefix}Date"))
        .dt.add_business_days(0, holidays=holidays, roll="forward")
        .alias("Date"),
        pl.all(),
    )
