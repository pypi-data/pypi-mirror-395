from __future__ import annotations

import polars as pl


def transform(df: pl.DataFrame) -> pl.DataFrame:
    return (
        df.select(pl.exclude(r"^.*\(REIT\)$"))
        .pipe(_rename)
        .pipe(_cast)
        .select(pl.col("Code"), pl.exclude("Code"))
    )


def _rename(df: pl.DataFrame) -> pl.DataFrame:
    return df.rename(
        {
            "LocalCode": "Code",
            "NumberOfIssuedAndOutstandingSharesAtTheEndOfFiscalYearIncludingTreasuryStock": "IssuedShares",  # noqa: E501
            "NumberOfTreasuryStockAtTheEndOfFiscalYear": "TreasuryShares",
            "AverageNumberOfShares": "AverageOutstandingShares",
        },
    )


def _cast(df: pl.DataFrame) -> pl.DataFrame:
    return (
        df.with_columns(
            pl.col("^.*Date$").str.to_date("%Y-%m-%d", strict=False),
            pl.col("DisclosedTime").str.to_time("%H:%M:%S", strict=False),
            pl.col("TypeOfCurrentPeriod").cast(pl.Categorical),
        )
        .pipe(_cast_float)
        .pipe(_cast_bool)
    )


def _cast_float(df: pl.DataFrame) -> pl.DataFrame:
    return df.with_columns(
        pl.col(f"^.*{name}.*$").cast(pl.Float64, strict=False)
        for name in [
            "Assets",
            "BookValue",
            "Cash",
            "Distributions",
            "Dividend",
            "Earnings",
            "Equity",
            "NetSales",
            "PayoutRatio",
            "Profit",
        ]
    ).with_columns(
        pl.col(
            "IssuedShares",
            "TreasuryShares",
        ).cast(pl.Int64, strict=False),
        pl.col(
            "AverageOutstandingShares",
        ).cast(pl.Float64, strict=False),
    )


def _cast_bool(df: pl.DataFrame) -> pl.DataFrame:
    columns = df.select(pl.col("^.*Changes.*$")).columns
    columns.append("RetrospectiveRestatement")

    return df.with_columns(
        pl.when(pl.col(col) == "true")
        .then(True)  # noqa: FBT003
        .when(pl.col(col) == "false")
        .then(False)  # noqa: FBT003
        .otherwise(None)
        .alias(col)
        for col in columns
    )
