from __future__ import annotations

from pathlib import Path

import pandas as pd

from data_prep_engine.core.standard_table import StandardTable
from data_prep_engine.diagnostics.report import DataDoctor


def test_diagnostics_basic_profiles_and_pk() -> None:
    # Create a small dataset with:
    # - pk: true primary key
    # - value: numeric with an outlier
    # - category: constant column
    # - with_missing: has missing values
    df = pd.DataFrame(
        {
            "pk": [1, 2, 3, 4],
            "value": [10.0, 11.0, 12.0, 1000.0],
            "category": ["a", "a", "a", "a"],
            "with_missing": [1.0, None, 2.0, None],
        }
    )

    table = StandardTable(data=df)
    doctor = DataDoctor(high_cardinality_min_unique=10)  # avoid high-card flag in small data
    report = doctor.diagnose(table)

    # Basic shape
    assert report.row_count == 4
    assert report.duplicate_row_count == 0

    # Primary key inference
    assert report.inferred_primary_keys == ["pk"]

    # Column summaries
    pk_summary = report.column_summaries["pk"]
    assert pk_summary.missing_count == 0
    assert pk_summary.unique_count == 4
    assert pk_summary.is_constant is False

    cat_summary = report.column_summaries["category"]
    assert cat_summary.is_constant is True
    assert cat_summary.unique_count == 1

    miss_summary = report.column_summaries["with_missing"]
    assert miss_summary.missing_count == 2
    assert 0.0 < miss_summary.missing_ratio < 1.0

    value_summary = report.column_summaries["value"]
    assert value_summary.numeric_stats is not None
    # The extreme 1000.0 should be flagged as an outlier by IQR
    assert value_summary.numeric_stats.outlier_count >= 1

    # Warnings should mention constant column and outliers
    joined_warnings = "\n".join(report.warnings)
    assert "constant" in joined_warnings
    assert "outliers" in joined_warnings


def test_duplicate_rows_detection() -> None:
    df = pd.DataFrame(
        {
            "a": [1, 1, 1],
            "b": [2, 2, 2],
        }
    )
    table = StandardTable(data=df)
    doctor = DataDoctor()
    report = doctor.diagnose(table)

    # Two rows are duplicates of the first row
    assert report.row_count == 3
    assert report.duplicate_row_count == 2
