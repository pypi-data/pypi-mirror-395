from __future__ import annotations

from pathlib import Path

import pandas as pd
import pytest

from data_prep_engine.ingestion.loader import Loader, IngestionError


def _write_csv(path: Path) -> None:
    df = pd.DataFrame({"a": [1, 2, 3], "b": ["x", "y", "z"]})
    df.to_csv(path, index=False)


def _write_json(path: Path) -> None:
    df = pd.DataFrame({"a": [10, 20], "b": ["p", "q"]})
    df.to_json(path, orient="records", lines=True)


def _write_parquet(path: Path) -> None:
    df = pd.DataFrame({"a": [100, 200], "b": ["u", "v"]})
    df.to_parquet(path, index=False)


def test_csv_ingestion(tmp_path: Path) -> None:
    file_path = tmp_path / "data.csv"
    _write_csv(file_path)

    loader = Loader()
    table = loader.load(str(file_path))

    df = table.to_pandas()
    assert df.shape == (3, 2)
    assert list(df.columns) == ["a", "b"]


def test_json_ingestion(tmp_path: Path) -> None:
    file_path = tmp_path / "data.json"
    _write_json(file_path)

    loader = Loader()
    table = loader.load(str(file_path), format_hint="json")

    df = table.to_pandas()
    assert df.shape == (2, 2)
    assert set(df.columns) == {"a", "b"}


def test_parquet_ingestion(tmp_path: Path) -> None:
    file_path = tmp_path / "data.parquet"
    _write_parquet(file_path)

    loader = Loader()
    table = loader.load(str(file_path))  # infer from suffix

    df = table.to_pandas()
    assert df.shape == (2, 2)
    assert set(df.columns) == {"a", "b"}


def test_unknown_format_raises(tmp_path: Path) -> None:
    file_path = tmp_path / "data.unknown"
    file_path.write_text("whatever")

    loader = Loader()

    with pytest.raises(IngestionError):
        loader.load(str(file_path))
