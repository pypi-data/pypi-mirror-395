from __future__ import annotations

from typing import TYPE_CHECKING, Any, Self

from kabukit.utils.cache import read, write
from kabukit.utils.config import get_cache_dir

if TYPE_CHECKING:
    from collections.abc import Iterable
    from pathlib import Path

    import polars as pl
    from polars._typing import IntoExprColumn


class Base:
    data: pl.DataFrame

    def __init__(
        self,
        data: pl.DataFrame | None = None,
        *,
        name: str | None = None,
    ) -> None:
        if data is not None:
            self.data = data
            return

        source, group = self._get_cache_path_parts()
        self.data = read(source, group, name)

    @classmethod
    def _get_cache_path_parts(cls) -> tuple[str, str]:
        parts = cls.__module__.split(".")
        # e.g. kabukit.domain.jquants.info -> jquants
        source = parts[-2]
        # e.g. kabukit.domain.jquants.info -> info
        group = parts[-1]
        return source, group

    @classmethod
    def data_dir(cls) -> Path:
        source, group = cls._get_cache_path_parts()
        return get_cache_dir() / source / group

    def write(self, name: str | None = None) -> Path:
        source, group = self._get_cache_path_parts()
        return write(source, group, self.data, name)

    def filter(
        self,
        *predicates: IntoExprColumn | Iterable[IntoExprColumn] | bool | list[bool],
        **constraints: Any,
    ) -> Self:
        """Filter the data with given predicates and constraints."""
        data = self.data.filter(*predicates, **constraints)
        return self.__class__(data)
