from __future__ import annotations

from kabukit.sources.columns import BaseColumns


class ListColumns(BaseColumns):
    Date = "日付"
    Code = "銘柄コード"
    DisclosedDate = "開示日"
    DisclosedTime = "開示時刻"
    Company = "会社名"
    Title = "表題"
    PdfUrl = "PDF URL"
    XbrlUrl = "XBRL URL"
    UpdateStatus = "更新履歴"
