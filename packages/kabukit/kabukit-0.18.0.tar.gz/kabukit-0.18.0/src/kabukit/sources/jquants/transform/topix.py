from __future__ import annotations

import polars as pl


def transform(df: pl.DataFrame) -> pl.DataFrame:
    return df.select(
        pl.col("Date").str.to_date("%Y-%m-%d"),
        pl.lit("TOPIX").alias("Code"),
        pl.exclude("Date"),
    )
