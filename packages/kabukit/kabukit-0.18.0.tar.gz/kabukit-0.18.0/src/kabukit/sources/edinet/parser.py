from __future__ import annotations

import re

import polars as pl

from kabukit.sources.utils import iter_contents


def parse_pdf(content: bytes, doc_id: str) -> pl.DataFrame:
    return pl.DataFrame({"DocumentId": [doc_id], "PdfContent": [content]})


def parse_csv(content: bytes, doc_id: str) -> pl.DataFrame:
    pattern = re.compile(r"^.+\.csv$")

    for csv in iter_contents(content, pattern):
        return read_csv(csv).select(
            pl.lit(doc_id).alias("DocumentId"),
            pl.all(),
        )

    return pl.DataFrame()


def read_csv(content: bytes) -> pl.DataFrame:
    return pl.read_csv(
        content,
        separator="\t",
        encoding="utf-16-le",
        infer_schema_length=None,
    )


def parse_xbrl(content: bytes) -> str | None:
    pattern = re.compile(r"^XBRL/PublicDoc/.+\.xbrl$")

    for xbrl in iter_contents(content, pattern):
        return xbrl.decode("utf-8")

    return None
