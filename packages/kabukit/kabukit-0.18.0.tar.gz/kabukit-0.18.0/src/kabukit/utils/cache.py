from __future__ import annotations

import shutil
from typing import TYPE_CHECKING

import polars as pl

from .config import get_cache_dir
from .datetime import today

if TYPE_CHECKING:
    from collections.abc import Iterator
    from pathlib import Path


def glob(source: str | None = None, group: str | None = None) -> Iterator[Path]:
    """Glob parquet files in the cache directory.

    Args:
        source: The name of the cache subdirectory (e.g., "jquants", "edinet").
        group: The name of the cache subdirectory (e.g., "info", "statements").
              If None, it globs all `*.parquet` files recursively.

    Returns:
        An iterator of Path objects for the matched parquet files.
    """
    paths: Iterator[Path] = iter([])  # Initialize paths

    if source is None and group is None:
        paths = get_cache_dir().glob("**/*.parquet")
    elif source and group is None:
        paths = get_cache_dir().joinpath(source).glob("**/*.parquet")
    elif source and group:
        paths = get_cache_dir().joinpath(source, group).glob("*.parquet")
    elif source is None and group:
        paths = get_cache_dir().glob(f"*/{group}/*.parquet")

    yield from sorted(paths, key=lambda path: path.stat().st_mtime)


def _get_latest_filepath(source: str, group: str) -> Path:
    filenames = list(glob(source, group))

    if not filenames:
        msg = f"No data found for {source}/{group}"
        raise FileNotFoundError(msg)

    return filenames[-1]


def _get_cache_filepath(source: str, group: str, name: str | None = None) -> Path:
    if name is None:
        return _get_latest_filepath(source, group)

    filename = get_cache_dir() / source / group / f"{name}.parquet"

    if not filename.exists():
        msg = f"File not found: {filename}"
        raise FileNotFoundError(msg)

    return filename


def read(source: str, group: str, name: str | None = None) -> pl.DataFrame:
    """Read a polars.DataFrame directly from the cache.

    Args:
        source: The name of the cache subdirectory (e.g., "jquants", "edinet").
        group: The name of the cache subdirectory (e.g., "info", "statements").
        name: Optional. A specific filename (without extension) within the cache group.
              If None, the latest file in the subdirectory is read.

    Returns:
        polars.DataFrame: The DataFrame read from the cache.

    Raises:
        FileNotFoundError: If no data is found in the cache.
    """
    filepath = _get_cache_filepath(source, group, name)
    return pl.read_parquet(filepath)


def write(source: str, group: str, df: pl.DataFrame, name: str | None = None) -> Path:
    """Write a polars.DataFrame directly to the cache.

    Args:
        source: The name of the cache subdirectory (e.g., "jquants", "edinet").
        group: The name of the cache subdirectory (e.g., "info", "statements").
        df: The polars.DataFrame to write.
        name: Optional. The filename (without extension) for the parquet file.
              If None, a timestamp is used as the filename.

    Returns:
        Path: The path to the written Parquet file.
    """
    data_dir = get_cache_dir() / source / group
    data_dir.mkdir(parents=True, exist_ok=True)

    if name is None:
        name = today().strftime("%Y%m%d")

    filename = data_dir / f"{name}.parquet"
    df.write_parquet(filename)
    return filename


def clean(source: str | None = None, group: str | None = None) -> None:
    """Remove the entire cache directory or a specified cache group.

    Args:
        source (str | None, optional): The name of the cache
            subdirectory (e.g., "jquants", "edinet") to remove.
        group (str | None, optional): The name of the cache
            subdirectory (e.g., "info", "statements") to remove.
            If None, the entire cache directory is removed.
    """
    if source is None and group is None:
        target_dir = get_cache_dir()
    elif source and group is None:
        target_dir = get_cache_dir() / source
    elif source and group:
        target_dir = get_cache_dir() / source / group
    else:
        # This specific combination (group without source) is not supported.
        # The function returns early.
        return

    if target_dir.exists():
        shutil.rmtree(target_dir)
