from __future__ import annotations

from typing import Any, Dict, Optional

import pandas as pd

from .base import ReaderAdapter
from ..datasource import DataSource
from ...core.standard_table import StandardTable


class JSONAdapter(ReaderAdapter):
    """
    Adapter for line-delimited or records-oriented JSON.

    We start with a simple implementation; we can later expand with
    'orient' / 'lines' options and nested normalization.
    """

    def __init__(self, read_kwargs: Optional[Dict[str, Any]] = None) -> None:
        # allow callers to override pandas.read_json options while keeping sane defaults
        self._read_kwargs = read_kwargs or {}

    def supports(self, source: DataSource) -> bool:
        fmt = (source.format_hint or source.suffix()).lower()
        return fmt == "json"

    def read(self, source: DataSource) -> StandardTable:
        read_kwargs: Dict[str, Any] = dict(self._read_kwargs)
        try:
            # pandas needs lines=True for JSONL. Retry automatically if not provided.
            df = pd.read_json(source.uri, **read_kwargs)
        except ValueError as exc:
            if "lines" in read_kwargs:
                raise
            read_kwargs["lines"] = True
            df = pd.read_json(source.uri, **read_kwargs)
        metadata = {"source": source.uri, "format": "json"}
        return StandardTable(data=df, metadata=metadata)
