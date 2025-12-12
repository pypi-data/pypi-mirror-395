from __future__ import annotations

from typing import TYPE_CHECKING, Any

import polars as pl
import tqdm.asyncio
import typer
from rich import box
from rich.console import Console
from rich.table import Table

from kabukit.utils.cache import write
from kabukit.utils.params import get_code_date as _get_code_date

if TYPE_CHECKING:
    import datetime

# pyright: reportUnknownMemberType=false


class CustomTqdm(tqdm.asyncio.tqdm):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        kwargs.setdefault("ncols", 80)
        super().__init__(*args, **kwargs)


def get_code_date(
    arg: str | None,
) -> tuple[None, None] | tuple[str, None] | tuple[None, datetime.date]:
    try:
        return _get_code_date(arg)
    except ValueError:
        typer.echo("無効な銘柄コード・日付の形式です。", err=True)
        raise typer.Exit(1) from None


def write_cache(
    df: pl.DataFrame,
    source: str,
    group: str,
    name: str,
    /,
    *,
    quiet: bool = False,
) -> None:
    path = write(source, group, df)
    if not quiet:
        typer.echo(f"{name}を '{path}' に保存しました。")


def display_dataframe(
    df: pl.DataFrame,
    *,
    first: bool = False,
    last: bool = False,
    quiet: bool = False,
) -> None:
    """データフレームを表示します。"""
    if quiet:
        return

    pl.Config.set_tbl_rows(5)
    pl.Config.set_tbl_cols(6)
    pl.Config.set_tbl_hide_dtype_separator()

    if df.is_empty():
        typer.echo("取得したデータはありません。")
    elif df.height == 1:
        display_single_row_dataframe(df)
    elif first:
        display_single_row_dataframe(df.head(1))
    elif last:
        display_single_row_dataframe(df.tail(1))
    else:
        typer.echo(df)


def display_single_row_dataframe(df: pl.DataFrame) -> None:
    """DataFrameが単一行の場合、rich Tableで整形して表示します。"""
    typer.echo(f"width: {df.width}")

    table = Table(show_header=True, header_style=None, box=box.SQUARE_DOUBLE_HEAD)

    table.add_column("Column Name", no_wrap=True)
    table.add_column("Data Type")
    table.add_column("Value")

    for col_name, dtype in df.schema.items():
        value = df[0, col_name]
        table.add_row(col_name, str(dtype), display_value(value))

    console = Console()
    console.print(table)


def display_value(value: Any) -> str:
    if isinstance(value, int):
        return f"{value:,d}"
    if isinstance(value, float):
        return format_float_with_commas(value)
    return str(value)


def format_float_with_commas(number: float) -> str:
    str_num = str(number)
    integer_part, decimal_part = str_num.split(".")
    formatted_integer_part = f"{int(integer_part):,d}"
    return f"{formatted_integer_part}.{decimal_part}"
