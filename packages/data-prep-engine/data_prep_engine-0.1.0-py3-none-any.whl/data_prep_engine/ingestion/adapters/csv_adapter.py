from __future__ import annotations

from typing import Any, Dict, Optional

import pandas as pd

from .base import ReaderAdapter
from ..datasource import DataSource
from ...core.standard_table import StandardTable


class CSVAdapter(ReaderAdapter):
    """Adapter that reads CSV sources into a StandardTable."""

    def __init__(self, read_kwargs: Optional[Dict[str, Any]] = None) -> None:
        # allow users to override pandas.read_csv kwargs such as delimiter, dtype, etc.
        self._read_kwargs = read_kwargs or {}

    def supports(self, source: DataSource) -> bool:
        fmt = (source.format_hint or source.suffix()).lower()
        return fmt == "csv"

    def read(self, source: DataSource) -> StandardTable:
        df = pd.read_csv(source.uri, **self._read_kwargs)
        metadata = {"source": source.uri, "format": "csv"}
        return StandardTable(data=df, metadata=metadata)
