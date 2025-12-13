from __future__ import annotations

from typing import Iterable, List, Optional, Sequence

from .datasource import DataSource
from .adapters.base import ReaderAdapter
from .adapters.csv_adapter import CSVAdapter
from .adapters.json_adapter import JSONAdapter
from .adapters.parquet_adapter import ParquetAdapter
from ..core.standard_table import StandardTable


class IngestionError(Exception):
    """Raised when no adapter can handle the given source."""


class Loader:
    """
    Unified entrypoint for data ingestion.

    Example
    -------
    loader = Loader()
    table = loader.load("data/myfile.csv")
    """

    def __init__(self, adapters: Optional[Sequence[ReaderAdapter]] = None) -> None:
        if adapters is None:
            adapters = [CSVAdapter(), JSONAdapter(), ParquetAdapter()]
        self._adapters: List[ReaderAdapter] = list(adapters)

    @property
    def adapters(self) -> Iterable[ReaderAdapter]:
        """Return the configured adapters."""
        return tuple(self._adapters)

    def load(self, uri: str, format_hint: Optional[str] = None) -> StandardTable:
        """
        Load a URI using the first adapter that supports it.

        Parameters
        ----------
        uri:
            Path or URL to the data.
        format_hint:
            Optional explicit format (e.g. 'csv', 'json', 'parquet').
            If not provided, we infer from file suffix.

        Returns
        -------
        StandardTable

        Raises
        ------
        IngestionError
            If no adapter can handle the source.
        """
        source = DataSource(uri=uri, format_hint=format_hint.lower() if format_hint else None)

        for adapter in self._adapters:
            if adapter.supports(source):
                return adapter.read(source)

        raise IngestionError(
            f"No adapter found for uri={uri!r} with format_hint={format_hint!r}"
        )
