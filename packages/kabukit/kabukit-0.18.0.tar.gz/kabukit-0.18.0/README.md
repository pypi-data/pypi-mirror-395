<p align="center">
  <img src="https://raw.githubusercontent.com/daizutabi/kabukit/main/docs/assets/images/logo.svg" alt="Kabukit Logo"">
</p>

<p align="center">
  <img src="https://raw.githubusercontent.com/daizutabi/kabukit/main/docs/assets/images/kabukit.svg" alt="Kabukit">
</p>

<p align="center">
  <em>日本の株式分析を、もっと手軽に、もっと速く</em>
</p>

<p align="center">
  <a href="https://pypi.org/project/kabukit/"><img src="https://img.shields.io/pypi/v/kabukit.svg"/></a>
  <a href="https://pypi.org/project/kabukit/"><img src="https://img.shields.io/pypi/pyversions/kabukit.svg"/></a>
  <a href="https://github.com/daizutabi/kabukit/actions?query=event%3Apush+branch%3Amain"><img src="https://img.shields.io/github/actions/workflow/status/daizutabi/kabukit/code-quality-tests.yaml?branch=main&label=ci&logo=github"/></a>
  <a href="https://codecov.io/github/daizutabi/kabukit?branch=main"><img src="https://codecov.io/github/daizutabi/kabukit/graph/badge.svg?token=Yu6lAdVVnd"/></a>
  <a href="https://daizutabi.github.io/kabukit/"><img src="https://img.shields.io/badge/docs-latest-blue.svg"/></a>
</p>

---

kabukit は、J-Quants と EDINET のデータを、コマンドラインや Python コードから快適に扱うためのモダンなツールキットです。

## なぜ kabukit なのか？

日本株の投資分析には、様々なデータソースへのアクセスが必要です。しかし、それぞれの API は仕様が異なり、データ取得だけで多くの時間を費やしてしまいます。kabukit は、こうした課題を解決します。

### ターミナルから即座にデータ取得

API の認証設定が対話形式で簡単に完了。`kabu get prices --all` の一行で、全上場銘柄の 10 年分<sup>1</sup> の株価データが手に入り、すぐに分析を始められます。

### ノートブックで快適な分析体験

`await get_statements()` と書くだけで、全上場銘柄の財務情報を非同期で並列取得。[Polars](https://pola.rs/) によるデータフレーム操作で、数千銘柄のデータも瞬時に処理できます。

### 賢いキャッシュで高速アクセス

一度取得したデータはローカルに保存され、次回からは瞬時にアクセス可能。ネットワークアクセスを待つことなく、何度でも試行錯誤できます。

### モダンな技術スタックで高速処理

[httpx](https://www.python-httpx.org/) の非同期処理により、複数銘柄のデータを並列取得。従来の同期的なアプローチと比べ、データ取得時間を大幅に短縮します。

<sup>1</sup> J-Quants API スタンダードプラン利用時。詳しくは [J-Quants API](https://jpx-jquants.com/) のプラン表を参照してください。

## クイックスタート

### インストール

Python 3.12 以上が必要です。

```bash
pip install kabukit
```

または

```bash
uv add kabukit
```

### CLI で使う

インストールしたら、まずは認証設定から始めましょう。

```bash
# J-Quants API の認証（対話形式）
kabu auth jquants

# 全銘柄情報を取得
kabu get info

# トヨタ自動車の財務情報を取得
kabu get statements 7203
```

### Python で使う

つぎに、[Jupyter](https://jupyter.org/) や [marimo](https://marimo.io/) などのノートブックで使ってみましょう。

```python
from kabukit import get_info, get_prices

# 全銘柄情報を取得
df_info = await get_info()

# トヨタ自動車の株価を取得
df_prices = await get_prices("7203")
```

## 主な機能

### 2つの API を統一的に扱える

- **[J-Quants API](https://jpx-jquants.com/)**: 上場銘柄情報、財務情報、株価四本値など
- **[EDINET API](https://disclosure2dl.edinet-fsa.go.jp/guide/static/disclosure/WZEK0110.html)**: 有価証券報告書などの開示書類

異なる API の仕様差を吸収し、同じインターフェースで利用できます。

### 高速なデータ処理

- **[Polars](https://pola.rs/)**: Rust ベースの高速データフレームライブラリ
- **[httpx](https://www.python-httpx.org/)**: 非同期 HTTP クライアントによる並列データ取得
- **キャッシュ機構**: 取得済みデータの再利用で、分析の試行錯誤を高速化

### 柔軟な利用方法

- **CLI**: スクリプト不要で、ターミナルから直接データ取得
- **Python API**: ノートブック環境での対話的な分析に最適
- **キャッシュ活用**: CLI で取得したデータを Python から読み込み可能

## ドキュメント

詳しい使い方は、公式ドキュメントを参照してください。

**[kabukit ドキュメント](https://daizutabi.github.io/kabukit/)**

- [CLI の使い方](https://daizutabi.github.io/kabukit/guides/cli/) - 認証設定、データ取得、キャッシュ管理
- [Python API の使い方](https://daizutabi.github.io/kabukit/guides/api/) - 各種情報を Python から取得する方法。モジュール関数と Client クラスの使い分け

## ライセンス

MIT License
