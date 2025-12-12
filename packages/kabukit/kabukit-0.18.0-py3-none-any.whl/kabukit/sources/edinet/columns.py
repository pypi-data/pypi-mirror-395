from __future__ import annotations

from kabukit.sources.columns import BaseColumns


class ListColumns(BaseColumns):
    Date = "日付"
    Code = "銘柄コード"  # secCode
    SubmittedDate = "提出日"  # submitDateTime (date part)
    SubmittedTime = "提出時刻"  # submitDateTime (time part)
    Company = "会社名"  # filerName
    DocumentId = "書類管理番号"  # docID
    DocumentTypeCode = "書類種別コード"  # docTypeCode
    DocumentDescription = "提出書類概要"  # docDescription
    CurrentReportReason = "臨報提出事由"  # currentReportReason
    PeriodStart = "期間(自)"  # periodStart
    PeriodEnd = "期間(至)"  # periodEnd
    EdinetCode = "提出者EDINETコード"  # edinetCode
    IssuerEdinetCode = "発行会社EDINETコード"  # issuerEdinetCode
    SubjectEdinetCode = "対象EDINETコード"  # subjectEdinetCode
    SubsidiaryEdinetCode = "子会社EDINETコード"  # subsidiaryEdinetCode
    ParentDocumentId = "親書類管理番号"  # parentDocID
    DisclosureStatus = "開示不開示区分"  # disclosureStatus
    DocumentInfoEditStatus = "書類情報修正区分"  # docInfoEditStatus
    LegalStatus = "縦覧区分"  # legalStatus
    WithdrawalStatus = "取下区分"  # withdrawalStatus
    AttachDocumentFlag = "代替書面・添付文書有無フラグ"  # attachDocFlag
    CsvFlag = "CSV有無フラグ"  # csvFlag
    PdfFlag = "PDF有無フラグ"  # pdfFlag
    XbrlFlag = "XBRL有無フラグ"  # xbrlFlag
    FileDate = "ファイル日付"  # EDINET APIリクエスト時のdateパラメータ
