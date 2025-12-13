from __future__ import annotations

from typing import Any, Dict, Optional

import pandas as pd

from .base import ReaderAdapter
from ..datasource import DataSource
from ...core.standard_table import StandardTable


class ParquetAdapter(ReaderAdapter):
    """
    Adapter for Parquet files using pandas.read_parquet.

    Requires a Parquet engine such as pyarrow (already in pyproject deps).
    """

    def __init__(self, read_kwargs: Optional[Dict[str, Any]] = None) -> None:
        self._read_kwargs = read_kwargs or {}

    def supports(self, source: DataSource) -> bool:
        fmt = (source.format_hint or source.suffix()).lower()
        return fmt == "parquet"

    def read(self, source: DataSource) -> StandardTable:
        df = pd.read_parquet(source.uri, **self._read_kwargs)
        metadata = {"source": source.uri, "format": "parquet"}
        return StandardTable(data=df, metadata=metadata)
