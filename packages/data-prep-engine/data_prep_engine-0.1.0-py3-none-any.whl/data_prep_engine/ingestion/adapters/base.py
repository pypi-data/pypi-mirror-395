from __future__ import annotations

from abc import ABC, abstractmethod

from ..datasource import DataSource
from ...core.standard_table import StandardTable


class ReaderAdapter(ABC):
    """
    Base interface for all ingestion adapters.

    Each adapter decides if it supports a given DataSource and, if so,
    knows how to read it into a StandardTable.
    """

    @abstractmethod
    def supports(self, source: DataSource) -> bool:
        """Return True if this adapter can handle the given source."""
        raise NotImplementedError

    @abstractmethod
    def read(self, source: DataSource) -> StandardTable:
        """Read the data source into a StandardTable."""
        raise NotImplementedError
