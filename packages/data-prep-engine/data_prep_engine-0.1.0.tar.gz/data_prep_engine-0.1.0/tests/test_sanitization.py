from __future__ import annotations

import pandas as pd

from data_prep_engine.core.standard_table import StandardTable
from data_prep_engine.sanitization.pipeline import SanitizationPipeline
from data_prep_engine.sanitization.steps.missing_handler import MissingValueHandler
from data_prep_engine.sanitization.steps.duplicate_handler import DuplicateHandler
from data_prep_engine.sanitization.steps.outlier_handler import OutlierHandler


def test_missing_value_handler_imputes_numeric_and_categorical() -> None:
    df = pd.DataFrame(
        {
            "num": [1.0, None, 3.0, None],
            "cat": ["a", None, "a", None],
        }
    )
    table = StandardTable(data=df)
    step = MissingValueHandler()
    new_table, logs = step.sanitize(table)

    new_df = new_table.to_pandas()
    assert new_df["num"].isna().sum() == 0
    assert new_df["cat"].isna().sum() == 0
    assert len(logs) >= 2  # both columns should be mentioned


def test_duplicate_handler_removes_duplicates() -> None:
    df = pd.DataFrame(
        {
            "a": [1, 1, 2, 2],
            "b": ["x", "x", "y", "y"],
        }
    )
    table = StandardTable(data=df)
    step = DuplicateHandler()
    new_table, logs = step.sanitize(table)

    new_df = new_table.to_pandas()
    assert len(new_df) == 2  # unique rows only
    assert "Removed 2 duplicate rows" in logs[0]


def test_outlier_handler_caps_extreme_values() -> None:
    df = pd.DataFrame(
        {
            "value": [10.0, 11.0, 12.0, 1000.0],
        }
    )
    table = StandardTable(data=df)
    step = OutlierHandler()
    new_table, logs = step.sanitize(table)

    new_df = new_table.to_pandas()
    # Extreme outlier should be reduced
    assert new_df["value"].max() < 1000.0
    assert any("Capped" in log for log in logs)


def test_sanitization_pipeline_runs_all_steps_in_order() -> None:
    df = pd.DataFrame(
        {
            "num": [1.0, None, 3.0, None],
            "cat": ["a", None, "a", None],
            "value": [10.0, 11.0, 12.0, 1000.0],
        }
    )
    table = StandardTable(data=df)

    pipeline = SanitizationPipeline(
        [
            MissingValueHandler(),
            DuplicateHandler(),
            OutlierHandler(),
        ]
    )

    result = pipeline.run(table)
    cleaned = result.cleaned_table.to_pandas()

    # No missing values remain
    assert cleaned.isna().sum().sum() == 0

    # Duplicates removed (there were duplicates created by imputation)
    # At minimum, we should have <= original row count
    assert len(cleaned) <= len(df)

    # Outlier capped
    assert cleaned["value"].max() < 1000.0

    # Logs contain entries from each step
    joined_logs = "\n".join(result.logs)
    assert "[MissingValueHandler]" in joined_logs
    assert "[DuplicateHandler]" in joined_logs
    assert "[OutlierHandler]" in joined_logs
