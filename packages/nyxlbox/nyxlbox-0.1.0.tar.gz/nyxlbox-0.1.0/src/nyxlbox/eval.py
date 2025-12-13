"""
Evaluation utilities for NyxBox.
"""

from __future__ import annotations

from typing import Any, Callable, List, Optional, Sequence

from pydantic import BaseModel, Field

from .core import RunResult


class EvaluationMetric(BaseModel):
    """
    A single metric evaluation for one result.
    """

    name: str
    passed: Optional[bool] = None
    score: Optional[float] = None
    details: dict[str, Any] = Field(default_factory=dict)


class EvaluatedResult(BaseModel):
    """
    A RunResult combined with its evaluation metrics.
    """

    result: RunResult
    gold_output: Optional[str] = None
    metrics: List[EvaluationMetric] = Field(default_factory=list)


EvaluatorFunction = Callable[[RunResult, str], EvaluationMetric]


def exact_match(
    case_sensitive: bool = True,
    strip_whitespace: bool = True,
) -> EvaluatorFunction:
    """
    Create an evaluator that checks if model output equals the gold output.
    """

    def evaluator(result: RunResult, gold_output: str) -> EvaluationMetric:
        output_text = result.output_text or ""

        left = output_text
        right = gold_output

        if strip_whitespace:
            left = left.strip()
            right = right.strip()

        if not case_sensitive:
            left = left.lower()
            right = right.lower()

        is_match = left == right

        return EvaluationMetric(
            name="exact_match",
            passed=is_match,
            score=1.0 if is_match else 0.0,
            details={
                "output_text": output_text,
                "gold_output": gold_output,
            },
        )

    return evaluator


def contains_substring(
    substring: str,
    case_sensitive: bool = False,
) -> EvaluatorFunction:
    """
    Create an evaluator that checks if the gold output substring is present in the model output.
    """

    def evaluator(result: RunResult, gold_output: str) -> EvaluationMetric:
        output_text = result.output_text or ""

        haystack = output_text
        needle = substring

        if not case_sensitive:
            haystack = haystack.lower()
            needle = needle.lower()

        contains = needle in haystack

        return EvaluationMetric(
            name="contains_substring",
            passed=contains,
            score=1.0 if contains else 0.0,
            details={
                "output_text": output_text,
                "substring": substring,
                "gold_output": gold_output,
            },
        )

    return evaluator


def evaluate_results(
    results: Sequence[RunResult],
    gold_outputs: Sequence[str],
    evaluators: Sequence[EvaluatorFunction],
) -> List[EvaluatedResult]:
    """
    Evaluate a sequence of RunResult objects against gold outputs.
    """

    if len(results) != len(gold_outputs):
        raise ValueError(
            f"results and gold_outputs length mismatch: {len(results)} vs {len(gold_outputs)}",
        )

    evaluated_items: List[EvaluatedResult] = []

    for result, gold in zip(results, gold_outputs, strict=True):
        metrics: List[EvaluationMetric] = []

        for evaluator in evaluators:
            metric = evaluator(result, gold)
            metrics.append(metric)

        evaluated_items.append(
            EvaluatedResult(
                result=result,
                gold_output=gold,
                metrics=metrics,
            ),
        )

    return evaluated_items
