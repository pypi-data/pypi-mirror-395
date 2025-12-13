"""
Serialization and storage utilities for NyxBox.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import List, Sequence

from .core import Experiment, RunResult


def experiment_to_json(experiment: Experiment, indent: int = 2) -> str:
    """
    Serialize an Experiment to a JSON string.
    """
    data = experiment.model_dump()
    return json.dumps(data, indent=indent, default=str)


def experiment_from_json(json_text: str) -> Experiment:
    """
    Deserialize an Experiment from a JSON string.
    """
    data = json.loads(json_text)
    return Experiment.model_validate(data)


def save_experiment(experiment: Experiment, path: str | Path, indent: int = 2) -> None:
    """
    Save an Experiment to a JSON file.
    """
    path_obj = Path(path)
    json_text = experiment_to_json(experiment, indent=indent)
    path_obj.write_text(json_text, encoding="utf-8")


def load_experiment(path: str | Path) -> Experiment:
    """
    Load an Experiment from a JSON file.
    """
    path_obj = Path(path)
    json_text = path_obj.read_text(encoding="utf-8")
    return experiment_from_json(json_text)


def results_to_json(results: Sequence[RunResult], indent: int = 2) -> str:
    """
    Serialize a sequence of RunResult objects to a JSON string.
    """
    data: List[dict] = [item.model_dump() for item in results]
    return json.dumps(data, indent=indent, default=str)


def results_from_json(json_text: str) -> List[RunResult]:
    """
    Deserialize a list of RunResult objects from a JSON string.
    """
    data = json.loads(json_text)
    return [RunResult.model_validate(item) for item in data]


def save_results(results: Sequence[RunResult], path: str | Path, indent: int = 2) -> None:
    """
    Save a sequence of RunResult objects to a JSON file.
    """
    path_obj = Path(path)
    json_text = results_to_json(results, indent=indent)
    path_obj.write_text(json_text, encoding="utf-8")


def load_results(path: str | Path) -> List[RunResult]:
    """
    Load a list of RunResult objects from a JSON file.
    """
    path_obj = Path(path)
    json_text = path_obj.read_text(encoding="utf-8")
    return results_from_json(json_text)
