from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional

from .core.standard_table import StandardTable
from .ingestion import Loader
from .diagnostics.report import DataDoctor, DiagnosticsReport
from .sanitization.pipeline import SanitizationPipeline, SanitizationResult
from .sanitization.steps.missing_handler import MissingValueHandler
from .sanitization.steps.duplicate_handler import DuplicateHandler
from .sanitization.steps.outlier_handler import OutlierHandler
from .visualization.artist import Artist


@dataclass
class AutoPrepResult:
    """
    End-to-end output of the AutoPrep pipeline.
    """
    raw_table: StandardTable
    cleaned_table: StandardTable
    diagnostics_before: DiagnosticsReport
    diagnostics_after: DiagnosticsReport
    sanitization_logs: List[str] = field(default_factory=list)


class AutoPrep:
    """
    Unified wrapper that orchestrates ingestion, diagnostics,
    sanitization, and lightweight visualization.

    Typical usage
    -------------
    prep = AutoPrep.default()
    result = prep.run_from_uri("data.csv")
    fig = prep.plot(result, column="some_column")
    fig.savefig("preview.png")
    """

    def __init__(
        self,
        loader: Optional[Loader] = None,
        doctor: Optional[DataDoctor] = None,
        pipeline: Optional[SanitizationPipeline] = None,
    ) -> None:
        self.loader = loader or Loader()
        self.doctor = doctor or DataDoctor()
        self.pipeline = pipeline or SanitizationPipeline(
            [
                MissingValueHandler(),
                DuplicateHandler(),
                OutlierHandler(),
            ]
        )

    @classmethod
    def default(cls) -> AutoPrep:
        """
        Construct an AutoPrep instance with default components.
        """
        return cls()

    def run_from_uri(
        self, uri: str, format_hint: Optional[str] = None
    ) -> AutoPrepResult:
        """
        Full pipeline starting from a URI.

        Steps:
        1. Ingest -> StandardTable
        2. Diagnose before cleaning
        3. Run sanitization pipeline
        4. Diagnose after cleaning
        """
        raw_table = self.loader.load(uri, format_hint=format_hint)
        return self.run_from_table(raw_table)

    def run_from_table(self, table: StandardTable) -> AutoPrepResult:
        """
        Full pipeline starting from an existing StandardTable.
        """
        diagnostics_before = self.doctor.diagnose(table)
        sanitization_result: SanitizationResult = self.pipeline.run(table)
        diagnostics_after = self.doctor.diagnose(sanitization_result.cleaned_table)

        return AutoPrepResult(
            raw_table=table,
            cleaned_table=sanitization_result.cleaned_table,
            diagnostics_before=diagnostics_before,
            diagnostics_after=diagnostics_after,
            sanitization_logs=list(sanitization_result.logs),
        )

    def plot(self, result: AutoPrepResult, column: Optional[str] = None):
        """
        Produce a smart plot for a given column (or auto-selected one)
        using the cleaned table and diagnostics_after.

        Returns a matplotlib Figure.
        """
        return Artist.plot(result.cleaned_table, result.diagnostics_after, column=column)
