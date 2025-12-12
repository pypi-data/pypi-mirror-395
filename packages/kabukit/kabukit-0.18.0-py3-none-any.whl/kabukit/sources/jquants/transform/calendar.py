from __future__ import annotations

import polars as pl


def transform(df: pl.DataFrame) -> pl.DataFrame:
    return df.with_columns(
        pl.col("Date").str.to_date("%Y-%m-%d"),
        pl.col("HolidayDivision").cast(pl.Categorical),
        pl.col("HolidayDivision").eq("1").not_().alias("IsHoliday"),
    )
