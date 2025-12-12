from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import polars as pl


class BaseColumns(Enum):
    @classmethod
    def rename(cls, df: pl.DataFrame, *, strict: bool = False) -> pl.DataFrame:
        """DataFrameの列名を日本語から英語に変換する。"""
        return df.rename({x.name: x.value for x in cls}, strict=strict)
