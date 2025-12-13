from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict

import pandas as pd


@dataclass
class StandardTable:
    """
    Lightweight, library-owned abstraction over tabular data.

    We wrap a pandas DataFrame for now, but this class is the single place
    where we can later switch to Polars or Arrow without changing adapters.
    """
    data: pd.DataFrame
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_pandas(self) -> pd.DataFrame:
        """Return a defensive copy of the underlying DataFrame."""
        return self.data.copy()

    @property
    def shape(self) -> tuple[int, int]:
        return self.data.shape
