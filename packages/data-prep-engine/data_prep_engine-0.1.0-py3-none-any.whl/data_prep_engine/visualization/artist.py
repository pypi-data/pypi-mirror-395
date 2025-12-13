from __future__ import annotations

import io
from typing import Optional

import matplotlib.pyplot as plt
import pandas as pd

from ..core.standard_table import StandardTable
from ..diagnostics.report import DiagnosticsReport, ColumnSummary


class Artist:
    """
    Lightweight visualization engine that produces smart plots
    based on column types and diagnostics.

    Usage:
        fig = Artist.plot(table, diagnostics_report, column="age")
        fig.show()
    """

    @staticmethod
    def plot(
        table: StandardTable,
        report: DiagnosticsReport,
        column: Optional[str] = None,
    ):
        df = table.to_pandas()

        # Auto-select column if not provided
        col_to_plot = column or Artist._choose_column(report)

        if col_to_plot not in df.columns:
            raise ValueError(f"Column '{col_to_plot}' not found in table.")

        summary = report.column_summaries[col_to_plot]
        series = df[col_to_plot]

        if pd.api.types.is_numeric_dtype(series):
            return Artist._plot_numeric(series, summary)
        else:
            return Artist._plot_categorical(series, summary)

    @staticmethod
    def _choose_column(report: DiagnosticsReport) -> str:
        """
        Automatically pick a column to plot using priority:
        1. Columns with warnings
        2. First numeric column
        3. First column
        """
        if report.warnings:
            for col in report.column_summaries.keys():
                if any(col in w for w in report.warnings):
                    return col

        for col, summary in report.column_summaries.items():
            if summary.numeric_stats is not None:
                return col

        return next(iter(report.column_summaries))

    @staticmethod
    def _plot_numeric(series: pd.Series, summary: ColumnSummary):
        fig, ax = plt.subplots(figsize=(6, 4))
        series.plot(kind="hist", bins=20, ax=ax, alpha=0.7, color="#4a90e2")

        ax.set_title(f"Distribution of {summary.name}")
        ax.set_xlabel(summary.name)
        ax.set_ylabel("Frequency")

        # Add outlier lines if numeric_stats exist
        if summary.numeric_stats:
            ns = summary.numeric_stats
            ax.axvline(ns.q1, color="green", linestyle="--", label="Q1")
            ax.axvline(ns.q3, color="red", linestyle="--", label="Q3")
            ax.legend()

        return fig

    @staticmethod
    def _plot_categorical(series: pd.Series, summary: ColumnSummary):
        counts = series.value_counts(dropna=False)

        fig, ax = plt.subplots(figsize=(6, 4))
        counts.plot(kind="bar", ax=ax, color="#50e3c2")

        ax.set_title(f"Value Counts: {summary.name}")
        ax.set_xlabel(summary.name)
        ax.set_ylabel("Count")

        return fig

    @staticmethod
    def to_png(fig, path: str):
        fig.savefig(path, format="png")

    @staticmethod
    def to_bytes(fig) -> bytes:
        buf = io.BytesIO()
        fig.savefig(buf, format="png")
        return buf.getvalue()
