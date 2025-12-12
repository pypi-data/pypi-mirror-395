from __future__ import annotations

import polars as pl


def transform(df: pl.DataFrame) -> pl.DataFrame:
    return df.select(
        pl.col("Date").str.to_date("%Y-%m-%d"),
        "Code",
        Open=pl.col("AdjustmentOpen"),
        High=pl.col("AdjustmentHigh"),
        Low=pl.col("AdjustmentLow"),
        Close=pl.col("AdjustmentClose"),
        UpperLimit=pl.col("UpperLimit").cast(pl.Int8).cast(pl.Boolean),
        LowerLimit=pl.col("LowerLimit").cast(pl.Int8).cast(pl.Boolean),
        Volume=pl.col("AdjustmentVolume"),
        TurnoverValue=pl.col("TurnoverValue"),
        AdjustmentFactor=pl.col("AdjustmentFactor"),
        RawOpen=pl.col("Open"),
        RawHigh=pl.col("High"),
        RawLow=pl.col("Low"),
        RawClose=pl.col("Close"),
        RawVolume=pl.col("Volume"),
    )
