from __future__ import annotations

from typing import List, Tuple

import pandas as pd

from ..pipeline import SanitizationStep
from ...core.standard_table import StandardTable


class OutlierHandler(SanitizationStep):
    """
    Cap numeric outliers using the IQR rule:

    For each numeric column:
    - Compute Q1, Q3, IQR.
    - Define [lower, upper] = [Q1 - 1.5*IQR, Q3 + 1.5*IQR].
    - Values below lower are set to lower, above upper set to upper.
    """

    @property
    def name(self) -> str:
        return "OutlierHandler"

    def sanitize(self, table: StandardTable) -> Tuple[StandardTable, List[str]]:
        df = table.to_pandas()
        logs: List[str] = []

        for col in df.columns:
            series = df[col]
            if not pd.api.types.is_numeric_dtype(series):
                continue

            clean = series.dropna()
            if clean.empty:
                continue

            q1 = float(clean.quantile(0.25))
            q3 = float(clean.quantile(0.75))
            iqr = q3 - q1
            if iqr <= 0:
                continue

            lower = q1 - 1.5 * iqr
            upper = q3 + 1.5 * iqr

            before_outliers = int(((clean < lower) | (clean > upper)).sum())
            if before_outliers == 0:
                continue

            capped = series.clip(lower=lower, upper=upper)
            df[col] = capped

            logs.append(
                f"Capped {before_outliers} outliers in column '{col}' "
                f"to range [{lower:.3f}, {upper:.3f}]."
            )

        new_table = StandardTable(data=df, metadata=dict(table.metadata))
        return new_table, logs
