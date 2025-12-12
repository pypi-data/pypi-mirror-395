from __future__ import annotations

from typing import Annotated

import typer
from async_typer import AsyncTyper  # pyright: ignore[reportMissingTypeStubs]
from httpx import HTTPStatusError
from typer import Exit, Option

# pyright: reportUnknownMemberType=false

app = AsyncTyper(
    add_completion=False,
    help="J-QuantsまたはEDINETの認証トークンを保存します。",
)


Mailaddress = Annotated[
    str | None,
    Option(
        "--mailaddress",
        help="J-Quantsに登録したメールアドレス。",
    ),
]
Password = Annotated[
    str | None,
    Option(
        "--password",
        hide_input=True,
        help="J-Quantsのパスワード。",
    ),
]


@app.async_command()
async def jquants(mailaddress: Mailaddress = None, password: Password = None) -> None:
    """J-Quants APIの認証を行い、トークンを設定ファイルに保存します。"""
    from kabukit.sources.jquants.client import AuthKey, JQuantsClient
    from kabukit.utils.config import get_config_value, save_config_key

    mailaddress = mailaddress or get_config_value(AuthKey.MAILADDRESS)

    if mailaddress is None:
        mailaddress = typer.prompt("J-Quantsに登録したメールアドレス")
        if not mailaddress or mailaddress.strip() == "":
            typer.echo("メールアドレスが入力されていません。")
            raise Exit(1)

    password = password or get_config_value(AuthKey.PASSWORD)

    if password is None:
        password = typer.prompt("J-Quantsのパスワード", hide_input=True)
        if not password or password.strip() == "":
            typer.echo("パスワードが入力されていません。")
            raise Exit(1)

    async with JQuantsClient() as client:
        try:
            id_token = await client.auth(mailaddress, password)
        except HTTPStatusError:
            typer.echo("認証に失敗しました。")
            raise Exit(1) from None

    save_config_key(AuthKey.ID_TOKEN, id_token)
    typer.echo("J-QuantsのIDトークンを保存しました。")


ApiKey = Annotated[
    str | None,
    Option(
        "--api-key",
        help="EDINET APIキー。",
    ),
]


@app.command()
def edinet(api_key: ApiKey = None) -> None:
    """EDINET APIのAPIキーを設定ファイルに保存します。"""
    from kabukit.sources.edinet.client import AuthKey
    from kabukit.utils.config import save_config_key

    if api_key is None:
        api_key = typer.prompt("EDINETで取得したAPIキー")

    if not api_key or api_key.strip() == "":
        typer.echo("APIキーが入力されていません。")
        raise Exit(1)

    save_config_key(AuthKey.API_KEY, api_key)
    typer.echo("EDINETのAPIキーを保存しました。")


@app.command()
def show() -> None:
    """設定ファイルに保存したJ-Quants IDトークンおよびEDINET APIキーを表示します。"""
    from kabukit.utils.config import get_config_path

    path = get_config_path()
    typer.echo(f"設定ファイル: {path}")

    if path.exists():
        typer.echo("----")
        text = path.read_text(encoding="utf-8")
        typer.echo(text.rstrip())
        typer.echo("----")
