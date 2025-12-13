"""
NyxlBox

Lightweight LLM experiment runner for prompts and model comparison.
"""

from __future__ import annotations

from .adapters import BaseAdapter, FunctionAdapter
from .core import Experiment, PromptCase, RunResult, run_experiment
from .eval import (
    EvaluationMetric,
    EvaluatedResult,
    contains_substring,
    evaluate_results,
    exact_match,
)
from .storage import (
    experiment_from_json,
    experiment_to_json,
    load_experiment,
    load_results,
    results_from_json,
    results_to_json,
    save_experiment,
    save_results,
)


__all__ = [
    "__version__",
    "Experiment",
    "PromptCase",
    "RunResult",
    "run_experiment",
    "experiment_to_json",
    "experiment_from_json",
    "results_to_json",
    "results_from_json",
    "save_experiment",
    "load_experiment",
    "save_results",
    "load_results",
    "EvaluationMetric",
    "EvaluatedResult",
    "exact_match",
    "contains_substring",
    "evaluate_results",
    "BaseAdapter",
    "FunctionAdapter",
]


__version__ = "0.1.0"
