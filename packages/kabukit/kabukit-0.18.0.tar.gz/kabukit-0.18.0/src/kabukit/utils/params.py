from __future__ import annotations

import datetime
from typing import TYPE_CHECKING, Any

from .datetime import parse_date

if TYPE_CHECKING:
    from collections.abc import Iterator


def iter_items(kwargs: dict[str, Any]) -> Iterator[tuple[str, Any]]:
    for key, value in kwargs.items():
        if value is None:
            continue

        if key == "from_":
            yield "from", value
        else:
            yield key, value


def get_params(**kwargs: Any) -> dict[str, Any]:
    params: dict[str, Any] = {}

    for key, value in iter_items(kwargs):
        if isinstance(value, datetime.date) or key == "date":
            params[key] = date_to_str(value)
        elif isinstance(value, str | int | float | bool):
            params[key] = value
        else:
            params[key] = str(value)

    return params


def date_to_str(date: str | datetime.date) -> str:
    """Convert a date object or string to a YYYY-MM-DD string.

    Args:
        date: The date to convert.

    Returns:
        The date as a YYYY-MM-DD string.
    """
    if isinstance(date, str):
        date = parse_date(date)

    return date.strftime("%Y-%m-%d")


def get_code_date(
    arg: str | None,
) -> tuple[None, None] | tuple[str, None] | tuple[None, datetime.date]:
    """銘柄コードまたは日付文字列を解析し、銘柄コードまたは日付オブジェクトを返す。

    Args:
        arg: 銘柄コードまたは日付文字列。

    Returns:
        銘柄コードまたは日付オブジェクトのタプル。
    """
    if arg is None:
        return None, None

    if len(arg) in [4, 5]:
        return arg, None

    return None, parse_date(arg)
