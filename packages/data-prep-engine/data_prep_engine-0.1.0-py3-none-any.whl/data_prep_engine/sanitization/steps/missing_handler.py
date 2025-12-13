from __future__ import annotations

from typing import List, Tuple

import pandas as pd

from ..pipeline import SanitizationStep
from ...core.standard_table import StandardTable


class MissingValueHandler(SanitizationStep):
    """
    Handle missing values with a simple, deterministic strategy:

    - For numeric columns: impute with median.
    - For non-numeric columns: impute with mode (most frequent) if available,
      otherwise leave as-is.
    """

    @property
    def name(self) -> str:
        return "MissingValueHandler"

    def sanitize(self, table: StandardTable) -> Tuple[StandardTable, List[str]]:
        df = table.to_pandas()
        logs: List[str] = []

        for col in df.columns:
            series = df[col]
            missing_before = int(series.isna().sum())
            if missing_before == 0:
                continue

            if pd.api.types.is_numeric_dtype(series):
                median = float(series.median())
                df[col] = series.fillna(median)
                logs.append(
                    f"Filled {missing_before} missing values in numeric column '{col}' "
                    f"with median={median}."
                )
            else:
                mode_series = series.mode(dropna=True)
                if not mode_series.empty:
                    mode = mode_series.iloc[0]
                    df[col] = series.fillna(mode)
                    logs.append(
                        f"Filled {missing_before} missing values in non-numeric column "
                        f"'{col}' with mode={mode!r}."
                    )
                else:
                    logs.append(
                        f"Column '{col}' has only missing values; left as-is."
                    )

        new_table = StandardTable(data=df, metadata=dict(table.metadata))
        return new_table, logs
