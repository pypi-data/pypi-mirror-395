"""Cache management commands."""

from __future__ import annotations

import datetime
import shutil
from typing import TYPE_CHECKING, Annotated
from zoneinfo import ZoneInfo

import typer
from rich.console import Console
from rich.tree import Tree
from typer import Argument, Option

if TYPE_CHECKING:
    from pathlib import Path

app = typer.Typer(add_completion=False, help="キャッシュを管理します。")


@app.command()
def tree() -> None:
    """キャッシュディレクトリのツリー構造を表示します。"""
    from kabukit.utils.config import get_cache_dir

    cache_dir = get_cache_dir()

    if not cache_dir.exists():
        typer.echo(f"キャッシュディレクトリ '{cache_dir}' は存在しません。")
        return

    console = Console()

    label = f"[bold blue]{cache_dir}[/bold blue]"
    tree_view = Tree(label)
    add_to_tree(tree_view, cache_dir)
    console.print(tree_view)


def add_to_tree(tree: Tree, path: Path) -> None:
    for p in sorted(path.iterdir(), key=lambda x: x.stat().st_mtime):
        if p.is_dir():
            label = f"[bold blue]{p.name}[/bold blue]"
            branch = tree.add(label)
            add_to_tree(branch, p)
        else:
            info = format_info(p)
            label = f"{p.name} [dim]{info}[/dim]"
            tree.add(label)


def format_info(path: Path) -> str:
    size = path.stat().st_size
    formatted_size = format_size(size)

    timestamp = path.stat().st_mtime
    formatted_timestamp = format_timestamp(timestamp)

    return f"{formatted_timestamp} {formatted_size}"


def format_timestamp(timestamp: float) -> str:
    dt = datetime.datetime.fromtimestamp(timestamp, tz=ZoneInfo("Asia/Tokyo"))
    return dt.strftime("%Y-%m-%d %H:%M")


def format_size(size: int) -> str:
    if size < 1024:
        return f"{size}B"

    if size < 1024 * 1024:
        return f"{size / 1024:.1f}KiB"

    return f"{size / (1024 * 1024):.1f}MiB"


SubDir = Annotated[str | None, Argument(help="サブディレクトリ。")]
All = Annotated[bool, Option("--all", help="全てのキャッシュを消去します。")]


@app.command()
def clean(sub_dir: SubDir = None, *, all_: All = False) -> None:
    """キャッシュディレクトリを削除します。"""
    from kabukit.utils.config import get_cache_dir

    cache_dir = get_cache_dir()

    if sub_dir is None:
        if all_:
            clean_cache_dir(cache_dir)
            return

        typer.echo("サブディレクトリか --all オプションを指定してください。")
        raise typer.Exit(1)

    clean_cache_dir(cache_dir / sub_dir)


def clean_cache_dir(cache_dir: Path) -> None:
    if not cache_dir.exists():
        typer.echo(f"キャッシュディレクトリ '{cache_dir}' は存在しません。")
        return

    try:
        shutil.rmtree(cache_dir)
        msg = f"キャッシュディレクトリ '{cache_dir}' を正常にクリーンアップしました。"
        typer.echo(msg)
    except OSError:
        msg = f"キャッシュディレクトリ '{cache_dir}' のクリーンアップ中に"
        msg += "エラーが発生しました。"
        typer.secho(msg, fg=typer.colors.RED, bold=True)
        raise typer.Exit(1) from None
