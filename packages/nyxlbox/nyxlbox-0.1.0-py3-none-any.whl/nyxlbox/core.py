"""
Core models and utilities for NyxBox.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Callable, List, Optional

from pydantic import BaseModel, Field


class PromptCase(BaseModel):
    """
    A single prompt case in an experiment.
    """

    input_text: str
    case_id: Optional[str] = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class Experiment(BaseModel):
    """
    A collection of prompt cases for a given model.
    """

    name: str
    model_name: str
    cases: List[PromptCase] = Field(default_factory=list)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
    )
    metadata: dict[str, Any] = Field(default_factory=dict)


class RunResult(BaseModel):
    """
    The result of running a single prompt case.
    """

    case_id: str
    input_text: str
    output_text: Optional[str]
    model_name: str
    started_at: datetime
    finished_at: datetime
    error: Optional[str] = None
    metadata: dict[str, Any] = Field(default_factory=dict)


ModelFunction = Callable[[str], str]


def run_experiment(experiment: Experiment, model_fn: ModelFunction) -> List[RunResult]:
    """
    Run all prompt cases in an experiment using a simple callable model.

    The model_fn receives the input_text and must return a string output.
    """

    results: List[RunResult] = []

    for index, case in enumerate(experiment.cases, start=1):
        case_id = case.case_id or f"case_{index}"
        started_at = datetime.now(timezone.utc)
        output_text: Optional[str] = None
        error: Optional[str] = None

        try:
            output_text = model_fn(case.input_text)
        except Exception as exc:
            error = repr(exc)

        finished_at = datetime.now(timezone.utc)

        result = RunResult(
            case_id=case_id,
            input_text=case.input_text,
            output_text=output_text,
            model_name=experiment.model_name,
            started_at=started_at,
            finished_at=finished_at,
            error=error,
            metadata=dict(case.metadata),
        )
        results.append(result)

    return results
