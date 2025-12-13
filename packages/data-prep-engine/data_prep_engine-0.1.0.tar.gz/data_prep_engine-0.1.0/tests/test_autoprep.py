from __future__ import annotations

from pathlib import Path

import matplotlib
import pandas as pd

matplotlib.use("Agg")  # ensure headless plotting

from data_prep_engine.autoprep import AutoPrep
from data_prep_engine.core.standard_table import StandardTable
from data_prep_engine.diagnostics.report import DataDoctor


def _make_sample_csv(path: Path) -> None:
    df = pd.DataFrame(
        {
            "id": [1, 1, 2, 3],
            "num": [10.0, None, 12.0, 1000.0],
            "cat": ["a", None, "a", "b"],
        }
    )
    df.to_csv(path, index=False)


def test_autoprep_run_from_uri(tmp_path: Path) -> None:
    file_path = tmp_path / "data.csv"
    _make_sample_csv(file_path)

    prep = AutoPrep.default()
    result = prep.run_from_uri(str(file_path))

    # Basic shape preserved
    assert result.raw_table.shape[0] == 4
    assert result.cleaned_table.shape[0] <= 4  # duplicates may be removed

    # No missing values in cleaned table
    cleaned_df = result.cleaned_table.to_pandas()
    assert cleaned_df.isna().sum().sum() == 0

    # Outlier should be reduced
    assert cleaned_df["num"].max() < 1000.0

    # There should be at least one sanitization log
    assert len(result.sanitization_logs) > 0


def test_autoprep_run_from_table() -> None:
    df = pd.DataFrame(
        {
            "id": [1, 2, 3, 3],
            "x": [1.0, 2.0, None, 100.0],
        }
    )
    table = StandardTable(df)
    prep = AutoPrep.default()

    result = prep.run_from_table(table)

    # Diagnostics before and after should differ for missing/outliers
    before = result.diagnostics_before
    after = result.diagnostics_after

    assert before.row_count == after.row_count or after.row_count < before.row_count
    assert any("missing values" in w.lower() or "outliers" in w.lower() for w in before.warnings) or \
           any("outliers" in w.lower() for w in before.warnings + after.warnings)


def test_autoprep_plot(tmp_path: Path) -> None:
    df = pd.DataFrame({"value": [1, 2, 3, 100]})
    table = StandardTable(df)

    doctor = DataDoctor()
    diagnostics = doctor.diagnose(table)

    from data_prep_engine.autoprep import AutoPrepResult

    dummy_result = AutoPrepResult(
        raw_table=table,
        cleaned_table=table,
        diagnostics_before=diagnostics,
        diagnostics_after=diagnostics,
        sanitization_logs=[],
    )

    prep = AutoPrep.default()
    fig = prep.plot(dummy_result, column="value")
    assert fig is not None

    img_path = tmp_path / "value_autoprep.png"
    fig.savefig(img_path)
    assert img_path.exists()
