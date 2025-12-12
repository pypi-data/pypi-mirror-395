from __future__ import annotations

from typing import TYPE_CHECKING, Self

import polars as pl

from kabukit.domain.base import Base

if TYPE_CHECKING:
    from datetime import timedelta

    from .statements import Statements


class Prices(Base):
    """日次株価データを保持し、各種指標を計算するためのメソッドを提供する。

    このクラスは、Polars DataFrameを内部で利用して、J-Quants APIなどから
    取得した株価の時系列データを格納する。
    株式分割などを考慮した調整や、財務情報と連携した各種利回り指標の計算、
    時価総額の算出といった、分析に不可欠なデータ加工機能を提供する。

    Attributes:
        data (pl.DataFrame): 株価の時系列データ。
    """

    def truncate(self, every: str | timedelta | pl.Expr) -> Self:
        """時系列データを指定された頻度で集計し、切り詰める。

        日次などの時系列データを指定された頻度（例: 月次、週次）で集計し、
        新しい時間軸に切り詰める。集計方法は以下の通りである。

        - `Open`: 各期間の最初の`Open`値
        - `High`: 各期間の最大`High`値
        - `Low`: 各期間の最小`Low`値
        - `Close`: 各期間の最後の`Close`値
        - `Volume`: 各期間の`Volume`の合計
        - `TurnoverValue`: 各期間の`TurnoverValue`の合計

        Args:
            every (str | timedelta | Expr):
                切り詰める頻度。"1d" (日次), "1mo" (月次),
                `timedelta`オブジェクト, または Polars の `Expr` オブジェクト。

        Returns:
            Self: 指定された頻度で切り詰められた新しいPricesオブジェクト。
        """
        data = (
            self.data.group_by(pl.col("Date").dt.truncate(every), "Code")
            .agg(
                pl.col("Open").drop_nulls().first(),
                pl.col("High").max(),
                pl.col("Low").min(),
                pl.col("Close").drop_nulls().last(),
                pl.col("Volume").sum(),
                pl.col("TurnoverValue").sum(),
            )
            .sort("Code", "Date")
        )

        return self.__class__(data)

    def with_adjusted_shares(self, statements: Statements) -> Self:
        """日次の調整済み株式数を計算し、列として追加する。

        決算短信で報告される株式数は四半期ごとのデータだが、株式分割や併合は
        日々発生する。このメソッドは、直近の決算で報告された株式数を、
        日々の調整係数 (`AdjustmentFactor`) を用いて補正し、日次ベースの
        時系列データとして提供する。

        `statements`から`IssuedShares`と`TreasuryShares`を取得し、
        `AdjustedIssuedShares`, `AdjustedTreasuryShares`列として追加する。

        Note:
            計算は、決算発表間の株式数変動が株式分割・併合にのみ起因すると
            仮定する。期中の増資や自己株式取得などは考慮されない。

        Args:
            statements (Statements): 財務情報を提供する`Statements`オブジェクト。

        Returns:
            Self: 調整済み株式数列が追加された、新しいPricesオブジェクト。
        """
        if "AdjustedIssuedShares" in self.data.columns:
            return self

        shares = statements.shares().rename({"Date": "ReportDate"})

        adjusted = (
            self.data.join_asof(
                shares,
                left_on="Date",
                right_on="ReportDate",
                by="Code",
                check_sortedness=False,
            )
            .with_columns(
                (1.0 / pl.col("AdjustmentFactor"))
                .cum_prod()
                .over("Code", "ReportDate")
                .alias("CumulativeRatio"),
            )
            .with_columns(
                (pl.col("IssuedShares", "TreasuryShares") * pl.col("CumulativeRatio"))
                .round(0)
                .cast(pl.Int64)
                .name.prefix("Adjusted"),
            )
            .select(
                "Date",
                "Code",
                "ReportDate",
                "AdjustedIssuedShares",
                "AdjustedTreasuryShares",
            )
        )

        data = self.data.join(adjusted, on=["Date", "Code"], how="left")

        return self.__class__(data)

    def _shares_expr(self, *, include_treasury_shares: bool = False) -> pl.Expr:
        """調整済み発行済株式数を計算する Polars 式を返す。

        Args:
            include_treasury_shares (bool): True の場合、
                自己株式を時価総額の計算に含める（発行済株式数を使用）。 False の場合、
                自己株式を計算から除外する（発行済株式数 - 自己株式数 を使用）。
                デフォルトは False。

        Returns:
            pl.Expr: 調整済み発行済株式数を計算する Polars 式。

        Raises:
            KeyError: 必要な列が存在しない場合に送出される。
        """
        required_cols = {"AdjustedIssuedShares"}
        if not include_treasury_shares:
            required_cols.add("AdjustedTreasuryShares")

        if not required_cols.issubset(self.data.columns):
            missing = required_cols - set(self.data.columns)
            msg = f"必要な列が存在しません: {missing}。"
            msg += "事前に .with_adjusted_shares() を呼び出す必要があります。"
            raise KeyError(msg)

        return (
            pl.col("AdjustedIssuedShares")
            if include_treasury_shares
            else (pl.col("AdjustedIssuedShares") - pl.col("AdjustedTreasuryShares"))
        )

    def with_market_cap(self, *, include_treasury_shares: bool = False) -> Self:
        """時価総額を計算し、列として追加する。

        日々の調整前終値 (`RawClose`) と、調整済みの発行済株式数を基に、
        日次ベースの時価総額を計算する。

        計算式:
            時価総額 = 調整前終値 * 発行済株式数

        Note:
            `include_treasury_shares` が False (デフォルト) の場合、
            発行済株式数は自己株式数を差し引いた数（発行済株式数 - 自己株式数）
            になります。True の場合は、発行済株式数全体が使用されます。

        Args:
            include_treasury_shares (bool): True の場合、
                自己株式を時価総額の計算に含める（発行済株式数を使用）。 False の場合、
                自己株式を計算から除外する（発行済株式数 - 自己株式数 を使用）。
                デフォルトは False。

        Returns:
            Self: `MarketCap` 列が追加された、新しいPricesオブジェクト。

        Raises:
            KeyError:
                調整済み株式数列が存在しない場合。
                事前に `with_adjusted_shares()` を呼び出す必要がある。
        """
        shares_expr = self._shares_expr(
            include_treasury_shares=include_treasury_shares,
        )

        data = self.data.with_columns(
            (pl.col("RawClose") * shares_expr).alias("MarketCap"),
        )

        return self.__class__(data)

    def with_equity(self, statements: Statements) -> Self:
        """時系列の純資産を列として追加する。

        Args:
            statements (Statements): 財務情報を提供する`Statements`オブジェクト。

        Returns:
            Self: `Equity` 列が追加された、新しいPricesオブジェクト。
        """
        if "Equity" in self.data.columns:
            return self

        data = self.data.join_asof(
            statements.equity(),
            on="Date",
            by="Code",
            check_sortedness=False,
        )

        return self.__class__(data)

    def with_book_value_yield(self) -> Self:
        """時系列の一株あたり純資産と純資産利回りを列として追加する。

        計算式:
            BPS = 純資産 / (調整済み発行済株式数 - 調整済み自己株式数)
            純資産利回り = BPS / 調整前終値

        Returns:
            Self: `BookValuePerShare`, `BookValueYield` 列が追加された、
            新しいPricesオブジェクト。

        Raises:
            KeyError:
                純資産または調整済み株式数列が存在しない場合。
                事前に `with_equity()` と `with_adjusted_shares()` を
                呼び出す必要がある。
        """
        data = self.data.with_columns(
            (pl.col("Equity") / self._shares_expr()).alias(
                "BookValuePerShare",
            ),
        ).with_columns(
            (pl.col("BookValuePerShare") / pl.col("RawClose")).alias(
                "BookValueYield",
            ),
        )

        return self.__class__(data)

    def with_forecast_profit(self, statements: Statements) -> Self:
        """時系列の予想純利益を列として追加する。

        Args:
            statements (Statements): 財務情報を提供する`Statements`オブジェクト。

        Returns:
            Self: `ForecastProfit` 列が追加された、新しいPricesオブジェクト。
        """
        if "ForecastProfit" in self.data.columns:
            return self

        data = self.data.join_asof(
            statements.forecast_profit(),
            on="Date",
            by="Code",
            check_sortedness=False,
        )

        return self.__class__(data)

    def with_earnings_yield(self) -> Self:
        """時系列の一株あたり純利益と収益利回りを列として追加する。

        計算式:
            EPS = 予想純利益 / (調整済み発行済株式数 - 調整済み自己株式数)
            収益利回り = EPS / 調整前終値

        Returns:
            Self: `EarningsPerShare`, `EarningsYield` 列が追加された、
            新しいPricesオブジェクト。

        Raises:
            KeyError:
                予想純利益または調整済み株式数列が存在しない場合。
                事前に `with_forecast_profit()` と `with_adjusted_shares()`
                を呼び出す必要がある。
        """
        data = self.data.with_columns(
            (pl.col("ForecastProfit") / self._shares_expr()).alias(
                "EarningsPerShare",
            ),
        ).with_columns(
            (pl.col("EarningsPerShare") / pl.col("RawClose")).alias("EarningsYield"),
        )

        return self.__class__(data)

    def with_forecast_dividend(self, statements: Statements) -> Self:
        """時系列の予想年間配当総額を列として追加する。

        Args:
            statements (Statements): 財務情報を提供する`Statements`オブジェクト。

        Returns:
            Self: `ForecastDividend` 列が追加された、新しいPricesオブジェクト。
        """
        if "ForecastDividend" in self.data.columns:
            return self

        data = self.data.join_asof(
            statements.forecast_dividend(),
            on="Date",
            by="Code",
            check_sortedness=False,
        )

        return self.__class__(data)

    def with_dividend_yield(self) -> Self:
        """時系列の一株あたり配当金と配当利回りを列として追加する。

        計算式:
            DPS = 予想年間配当総額 / (調整済み発行済株式数 - 調整済み自己株式数)
            配当利回り = DPS / 調整前終値

        Returns:
            Self: `DividendPerShare`, `DividendYield` 列が追加された、
            新しいPricesオブジェクト。

        Raises:
            KeyError:
                予想配当または調整済み株式数列が存在しない場合。
                事前に `with_forecast_dividend()` と `with_adjusted_shares()`
                を呼び出す必要がある。
        """
        data = self.data.with_columns(
            (pl.col("ForecastDividend") / self._shares_expr()).alias(
                "DividendPerShare",
            ),
        ).with_columns(
            (pl.col("DividendPerShare") / pl.col("RawClose")).alias("DividendYield"),
        )

        return self.__class__(data)

    def with_yields(self, statements: Statements) -> Self:
        """すべての利回り関連指標を計算し、列として追加する。

        以下の利回り関連指標をまとめて計算するコンビニエンスメソッドである。
        - 純資産利回り (`BookValueYield`)
        - 収益利回り (`EarningsYield`)
        - 配当利回り (`DividendYield`)

        内部で `with_adjusted_shares()` や `with_equity()` などを呼び出す。
        これらのメソッドはべき等であるため、重複して呼び出されても
        無駄な計算は行われない。

        Args:
            statements (Statements): 財務情報を提供する`Statements`オブジェクト。

        Returns:
            Self: 各種利回り指標の列が追加された、新しいPricesオブジェクト。
        """
        return (
            self.with_adjusted_shares(statements)
            .with_equity(statements)
            .with_book_value_yield()
            .with_forecast_profit(statements)
            .with_earnings_yield()
            .with_forecast_dividend(statements)
            .with_dividend_yield()
        )

    def period_stats(self) -> pl.DataFrame:
        """各期ごとの各種利回りおよび調整済み終値の統計量を計算する。

        `Code`と`ReportDate`で定義される各期（決算期間）ごとに、
        各種指標の統計量（始値, 高値, 安値, 終値, 平均値）を計算する。

        対象指標:
        - `BookValueYield` (純資産利回り)
        - `EarningsYield` (収益利回り)
        - `DividendYield` (配当利回り)
        - `Close` (調整済み終値)

        Returns:
            DataFrame: 各期ごとの統計量を持つ新しいDataFrameオブジェクト。

        Raises:
            KeyError:
                計算に必要な列が存在しない場合。
                事前に `with_yields()` を呼び出す必要がある。
        """
        # 必要なカラムが存在するかチェック
        required_cols = {
            "BookValueYield",
            "EarningsYield",
            "DividendYield",
            "Close",
            "ReportDate",
        }
        if not required_cols.issubset(self.data.columns):
            missing = required_cols - set(self.data.columns)
            msg = f"必要な列が存在しません: {missing}。"
            msg += "事前に `with_yields()` メソッドなどを呼び出してください。"
            raise KeyError(msg)

        # 統計量を計算するカラムのリスト
        target_cols = ["BookValueYield", "EarningsYield", "DividendYield", "Close"]

        # 各カラムに対して統計量を計算する式を生成
        aggs: list[pl.Expr] = []
        for col in target_cols:
            aggs.extend(
                [
                    pl.col(col).drop_nulls().first().alias(f"{col}_PeriodOpen"),
                    pl.col(col).max().alias(f"{col}_PeriodHigh"),
                    pl.col(col).min().alias(f"{col}_PeriodLow"),
                    pl.col(col).drop_nulls().last().alias(f"{col}_PeriodClose"),
                    pl.col(col).mean().alias(f"{col}_PeriodMean"),
                ],
            )

        # CodeとReportDateでグループ化し、統計量を計算
        return self.data.group_by("Code", "ReportDate", maintain_order=True).agg(aggs)

    def with_period_stats(self) -> Self:
        """各期ごとの各種利回りおよび調整済み終値の統計量を列として追加する。

        `period_stats()` メソッドで計算された各期の統計量を、元のDataFrameの
        各行に対応させて追加する。

        Returns:
            Self: 各期の統計量カラムが追加された、新しいPricesオブジェクト。

        Raises:
            KeyError:
                計算に必要な列が存在しない場合。
                事前に `with_yields()` を呼び出す必要がある。
        """
        stats = self.period_stats()
        data = self.data.join(stats, on=["Code", "ReportDate"], how="left")

        return self.__class__(data)
