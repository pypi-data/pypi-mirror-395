from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List, Optional

import pandas as pd

from ..core.standard_table import StandardTable


@dataclass
class NumericStats:
    min: float
    max: float
    mean: float
    q1: float
    q3: float
    iqr: float
    outlier_count: int


@dataclass
class ColumnSummary:
    name: str
    dtype: str
    non_nulls: int
    missing_count: int
    missing_ratio: float
    unique_count: int
    is_constant: bool
    is_high_cardinality: bool
    numeric_stats: Optional[NumericStats] = None


@dataclass
class DiagnosticsReport:
    """
    Container for all diagnostic information about a StandardTable.
    """
    row_count: int
    duplicate_row_count: int
    column_summaries: Dict[str, ColumnSummary]
    inferred_primary_keys: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the report to a JSON-serializable dictionary.
        """
        cols: Dict[str, Any] = {}
        for name, summary in self.column_summaries.items():
            col_dict = asdict(summary)
            if summary.numeric_stats is not None:
                col_dict["numeric_stats"] = asdict(summary.numeric_stats)
            cols[name] = col_dict

        return {
            "row_count": self.row_count,
            "duplicate_row_count": self.duplicate_row_count,
            "inferred_primary_keys": list(self.inferred_primary_keys),
            "warnings": list(self.warnings),
            "column_summaries": cols,
        }

    def to_markdown(self) -> str:
        """
        Render a concise markdown table of column-level diagnostics.
        """
        lines: List[str] = []
        lines.append(
            "| column | dtype | non_nulls | missing% | unique | constant | high_card | outliers |"
        )
        lines.append("|--------|-------|-----------|----------|--------|----------|-----------|----------|")

        for name, summary in self.column_summaries.items():
            ns = summary.numeric_stats
            outliers = ns.outlier_count if ns is not None else 0
            lines.append(
                f"| {name} | {summary.dtype} | {summary.non_nulls} | "
                f"{summary.missing_ratio:.2%} | {summary.unique_count} | "
                f"{summary.is_constant} | {summary.is_high_cardinality} | {outliers} |"
            )

        header = f"# Diagnostics Report\n\n"
        meta = (
            f"- Rows: **{self.row_count}**  \n"
            f"- Duplicate rows: **{self.duplicate_row_count}**  \n"
            f"- Inferred primary keys: `{', '.join(self.inferred_primary_keys) or 'None'}`  \n"
        )
        warn_block = ""
        if self.warnings:
            warn_block = "\n**Warnings:**\n" + "\n".join(f"- {w}" for w in self.warnings) + "\n"

        return header + meta + "\n".join(lines) + "\n" + warn_block


class DataDoctor:
    """
    The 'Doctor' for our data: runs diagnostics on a StandardTable.
    """

    def __init__(
        self,
        high_cardinality_threshold: float = 0.5,
        high_cardinality_min_unique: int = 50,
    ) -> None:
        self.high_cardinality_threshold = high_cardinality_threshold
        self.high_cardinality_min_unique = high_cardinality_min_unique

    def diagnose(self, table: StandardTable) -> DiagnosticsReport:
        df = table.to_pandas()
        row_count = len(df)
        duplicate_row_count = int(df.duplicated().sum())

        column_summaries: Dict[str, ColumnSummary] = {}
        warnings: List[str] = []

        for col_name in df.columns:
            summary, col_warnings = self._profile_column(df[col_name], row_count)
            column_summaries[col_name] = summary
            warnings.extend(col_warnings)

        inferred_primary_keys = self._infer_primary_keys(
            row_count=row_count, summaries=column_summaries
        )
        if not inferred_primary_keys:
            warnings.append("No primary key column inferred (no column is unique and non-null).")

        return DiagnosticsReport(
            row_count=row_count,
            duplicate_row_count=duplicate_row_count,
            column_summaries=column_summaries,
            inferred_primary_keys=inferred_primary_keys,
            warnings=warnings,
        )

    def _profile_column(
        self, series: pd.Series, row_count: int
    ) -> tuple[ColumnSummary, List[str]]:
        col_name = series.name
        dtype = str(series.dtype)
        missing_count = int(series.isna().sum())
        non_nulls = row_count - missing_count
        missing_ratio = missing_count / row_count if row_count > 0 else 0.0
        unique_count = int(series.nunique(dropna=True))

        is_constant = unique_count <= 1
        is_numeric = pd.api.types.is_numeric_dtype(series)
        numeric_stats: Optional[NumericStats] = None
        warnings: List[str] = []

        if is_constant:
            warnings.append(f"Column '{col_name}' is constant and may be dropped.")

        is_high_card = False
        if non_nulls > 0:
            ratio = unique_count / non_nulls
            is_high_card = (
                unique_count >= self.high_cardinality_min_unique
                and ratio >= self.high_cardinality_threshold
            )
            if is_high_card:
                warnings.append(
                    f"Column '{col_name}' has high cardinality "
                    f"({unique_count} unique out of {non_nulls} non-null)."
                )

        if is_numeric and non_nulls > 0:
            numeric_stats = self._compute_numeric_stats(series)
            if numeric_stats.outlier_count > 0:
                warnings.append(
                    f"Column '{col_name}' contains {numeric_stats.outlier_count} IQR outliers."
                )

        summary = ColumnSummary(
            name=col_name,
            dtype=dtype,
            non_nulls=non_nulls,
            missing_count=missing_count,
            missing_ratio=missing_ratio,
            unique_count=unique_count,
            is_constant=is_constant,
            is_high_cardinality=is_high_card,
            numeric_stats=numeric_stats,
        )
        return summary, warnings

    @staticmethod
    def _compute_numeric_stats(series: pd.Series) -> NumericStats:
        clean = series.dropna()
        q1 = float(clean.quantile(0.25))
        q3 = float(clean.quantile(0.75))
        iqr = q3 - q1
        if iqr <= 0:
            outlier_count = 0
        else:
            lower = q1 - 1.5 * iqr
            upper = q3 + 1.5 * iqr
            outlier_mask = (clean < lower) | (clean > upper)
            outlier_count = int(outlier_mask.sum())

        return NumericStats(
            min=float(clean.min()),
            max=float(clean.max()),
            mean=float(clean.mean()),
            q1=q1,
            q3=q3,
            iqr=float(iqr),
            outlier_count=outlier_count,
        )

    @staticmethod
    def _infer_primary_keys(
        row_count: int, summaries: Dict[str, ColumnSummary]
    ) -> List[str]:
        """
        Infer primary key columns.
        
        Criteria:
        - Must be unique and non-null
        - Prefer integer/string types over float types
        - Prefer columns with key-like names (id, pk, key, etc.)
        - Exclude numeric columns with outliers (likely value columns, not keys)
        """
        candidates: List[tuple[str, ColumnSummary, int]] = []
        
        for name, summary in summaries.items():
            if row_count == 0:
                continue
            if summary.missing_count == 0 and summary.unique_count == row_count:
                # Score: higher is better
                score = 0
                
                # Prefer integer or string types (not float)
                if "int" in summary.dtype or "object" in summary.dtype or "string" in summary.dtype:
                    score += 10
                elif "float" in summary.dtype:
                    # Float types are less likely to be primary keys
                    score -= 5
                
                # Prefer columns with key-like names
                name_lower = name.lower()
                if any(keyword in name_lower for keyword in ["id", "pk", "key", "_id", "_pk"]):
                    score += 20
                
                # Penalize numeric columns with outliers (likely value columns)
                if summary.numeric_stats and summary.numeric_stats.outlier_count > 0:
                    score -= 15
                
                candidates.append((name, summary, score))
        
        # Sort by score (descending), then by name
        candidates.sort(key=lambda x: (-x[2], x[0]))
        
        # Return only the highest-scoring candidates (those with score > 0 or top candidate)
        if not candidates:
            return []
        
        # If top candidate has positive score, return all with same or higher score
        # Otherwise, return only the top candidate if it's the only one
        top_score = candidates[0][2]
        if top_score > 0:
            return [name for name, _, score in candidates if score == top_score]
        elif len(candidates) == 1:
            return [candidates[0][0]]
        else:
            # Multiple candidates but all have non-positive scores
            # Return only the top one
            return [candidates[0][0]]
