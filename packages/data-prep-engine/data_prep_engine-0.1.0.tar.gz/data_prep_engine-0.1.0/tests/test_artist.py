from __future__ import annotations

import os
import pandas as pd
import matplotlib

matplotlib.use("Agg")

from data_prep_engine.core.standard_table import StandardTable
from data_prep_engine.diagnostics.report import DataDoctor
from data_prep_engine.visualization.artist import Artist


def test_artist_numeric_plot(tmp_path):
    df = pd.DataFrame({"value": [1, 2, 3, 100]})
    table = StandardTable(df)
    report = DataDoctor().diagnose(table)

    fig = Artist.plot(table, report, column="value")
    assert fig is not None

    img_path = tmp_path / "value.png"
    Artist.to_png(fig, str(img_path))
    assert os.path.exists(img_path)


def test_artist_categorical_plot():
    df = pd.DataFrame({"color": ["red", "red", "blue", None]})
    table = StandardTable(df)
    report = DataDoctor().diagnose(table)

    fig = Artist.plot(table, report, column="color")
    assert fig is not None


def test_artist_auto_column_selection():
    df = pd.DataFrame({"a": ["x", "x", "x"], "b": [1, 2, 3]})
    table = StandardTable(df)
    report = DataDoctor().diagnose(table)

    fig = Artist.plot(table, report)  # Should auto-select "b"
    assert fig is not None
