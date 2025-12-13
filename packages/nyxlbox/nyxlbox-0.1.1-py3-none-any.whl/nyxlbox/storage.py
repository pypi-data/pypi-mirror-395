from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable, List

import yaml

from .core import Experiment, RunResult


def _ensure_path(path: str | Path) -> Path:
    return path if isinstance(path, Path) else Path(path)


def experiment_to_json(experiment: Experiment, indent: int = 2) -> str:
    data = experiment.model_dump(mode="python")
    return json.dumps(data, ensure_ascii=False, indent=indent, default=str)


def experiment_from_json(json_text: str) -> Experiment:
    data = json.loads(json_text)
    if not isinstance(data, dict):
        raise ValueError("Experiment JSON root must be an object")
    return Experiment.model_validate(data)


def results_to_json(results: Iterable[RunResult], indent: int = 2) -> str:
    data = [item.model_dump(mode="python") for item in results]
    return json.dumps(data, ensure_ascii=False, indent=indent, default=str)


def results_from_json(json_text: str) -> List[RunResult]:
    data = json.loads(json_text)
    if not isinstance(data, list):
        raise ValueError("Results JSON root must be a list")
    return [RunResult.model_validate(item) for item in data]


def save_experiment(experiment: Experiment, path: str | Path) -> None:
    path_obj = _ensure_path(path)
    text = experiment_to_json(experiment)
    path_obj.write_text(text, encoding="utf-8")


def load_experiment(path: str | Path) -> Experiment:
    path_obj = _ensure_path(path)
    text = path_obj.read_text(encoding="utf-8")
    return experiment_from_json(text)


def save_results(results: Iterable[RunResult], path: str | Path) -> None:
    path_obj = _ensure_path(path)
    text = results_to_json(list(results))
    path_obj.write_text(text, encoding="utf-8")


def load_results(path: str | Path) -> List[RunResult]:
    path_obj = _ensure_path(path)
    text = path_obj.read_text(encoding="utf-8")
    return results_from_json(text)


def save_experiment_yaml(experiment: Experiment, path: str | Path) -> None:
    """
    Save an Experiment to a YAML file.

    The YAML structure matches the Experiment model fields, for example:

    name: demo
    model_name: upper
    cases:
      - input_text: "hello"
        case_id: "c1"
    metadata:
      purpose: demo
    """
    path_obj = _ensure_path(path)
    data = experiment.model_dump(mode="python")
    text = yaml.safe_dump(data, sort_keys=False, allow_unicode=True)
    path_obj.write_text(text, encoding="utf-8")


def load_experiment_yaml(path: str | Path) -> Experiment:
    """
    Load an Experiment from a YAML file.

    Supports two shapes:
    - plain Experiment mapping
    - mapping with an "experiment" key whose value is the Experiment mapping
      plus optional extra config fields (ignored here).
    """
    path_obj = _ensure_path(path)
    text = path_obj.read_text(encoding="utf-8")
    data = yaml.safe_load(text)

    if not isinstance(data, dict):
        raise ValueError("Experiment YAML root must be a mapping")

    if "experiment" in data and isinstance(data["experiment"], dict):
        exp_data = data["experiment"]
    else:
        exp_data = data

    return Experiment.model_validate(exp_data)
