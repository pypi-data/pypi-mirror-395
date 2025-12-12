from __future__ import annotations

import io
import zipfile
from functools import cache
from typing import TYPE_CHECKING, Literal, overload

from bs4 import BeautifulSoup

if TYPE_CHECKING:
    import re
    from collections.abc import Iterator


@cache
def get_soup(html: str) -> BeautifulSoup:
    return BeautifulSoup(html, "lxml")


@overload
def iter_contents(
    content: bytes,
    pattern: re.Pattern[str],
    *,
    include_filename: Literal[False] = False,
) -> Iterator[bytes]: ...


@overload
def iter_contents(
    content: bytes,
    pattern: re.Pattern[str],
    *,
    include_filename: Literal[True],
) -> Iterator[tuple[str, bytes]]: ...


def iter_contents(
    content: bytes,
    pattern: re.Pattern[str],
    *,
    include_filename: bool = False,
) -> Iterator[bytes] | Iterator[tuple[str, bytes]]:
    buffer = io.BytesIO(content)

    with zipfile.ZipFile(buffer) as zf:
        for info in zf.infolist():
            if pattern.match(info.filename):
                with zf.open(info) as f:
                    if include_filename:
                        yield info.filename, f.read()
                    else:
                        yield f.read()
