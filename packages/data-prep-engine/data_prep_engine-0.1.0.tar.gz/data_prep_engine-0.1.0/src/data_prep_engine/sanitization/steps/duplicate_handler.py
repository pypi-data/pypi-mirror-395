from __future__ import annotations

from typing import List, Tuple

import pandas as pd

from ..pipeline import SanitizationStep
from ...core.standard_table import StandardTable


class DuplicateHandler(SanitizationStep):
    """
    Drop duplicate rows, keeping the first occurrence.

    This is a simple but commonly needed optimization for ML preprocessing.
    """

    @property
    def name(self) -> str:
        return "DuplicateHandler"

    def sanitize(self, table: StandardTable) -> Tuple[StandardTable, List[str]]:
        df = table.to_pandas()
        logs: List[str] = []

        before = len(df)
        df_dedup = df.drop_duplicates(keep="first")
        after = len(df_dedup)
        removed = before - after

        if removed > 0:
            logs.append(f"Removed {removed} duplicate rows (from {before} to {after}).")
        else:
            logs.append("No duplicate rows found.")

        new_table = StandardTable(data=df_dedup, metadata=dict(table.metadata))
        return new_table, logs
