from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Iterable, List, Sequence, Tuple

from ..core.standard_table import StandardTable


class SanitizationStep(ABC):
    """
    Base class for all sanitization steps.

    Each step receives a StandardTable and returns a possibly modified copy,
    plus a list of human-readable log messages describing the changes.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """Human-readable name of the step."""
        raise NotImplementedError

    @abstractmethod
    def sanitize(self, table: StandardTable) -> Tuple[StandardTable, List[str]]:
        """
        Apply the sanitization step.

        Returns
        -------
        (StandardTable, List[str])
            The transformed table and log messages describing what was done.
        """
        raise NotImplementedError


@dataclass
class SanitizationResult:
    cleaned_table: StandardTable
    logs: List[str] = field(default_factory=list)

    def iter_logs(self) -> Iterable[str]:
        return iter(self.logs)


class SanitizationPipeline:
    """
    Orchestrates a sequence of SanitizationSteps.

    Example
    -------
    pipeline = SanitizationPipeline([MissingValueHandler(), DuplicateHandler()])
    result = pipeline.run(table)
    """

    def __init__(self, steps: Sequence[SanitizationStep]) -> None:
        self._steps: List[SanitizationStep] = list(steps)

    @property
    def steps(self) -> Tuple[SanitizationStep, ...]:
        return tuple(self._steps)

    def run(self, table: StandardTable) -> SanitizationResult:
        logs: List[str] = []
        current = table

        for step in self._steps:
            current, step_logs = step.sanitize(current)
            logs.append(f"[{step.name}]")
            logs.extend(f"  - {msg}" for msg in step_logs)

        return SanitizationResult(cleaned_table=current, logs=logs)
