"""
Command line interface for NyxBox.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import List

import typer

from .core import Experiment, RunResult, run_experiment
from .eval import EvaluatedResult, evaluate_results, exact_match
from .storage import (
    load_experiment,
    load_results,
    save_results,
)


app = typer.Typer(help="NyxBox command line interface.")


def _get_model_function(kind: str):
    """
    Return a simple model function based on the given kind.
    """

    def echo_model(prompt: str) -> str:
        return prompt

    def upper_model(prompt: str) -> str:
        return prompt.upper()

    def reverse_model(prompt: str) -> str:
        return prompt[::-1]

    mapping = {
        "echo": echo_model,
        "upper": upper_model,
        "reverse": reverse_model,
    }

    if kind not in mapping:
        available = ", ".join(sorted(mapping.keys()))
        raise typer.BadParameter(
            f"Unknown model kind '{kind}'. Available kinds: {available}",
        )

    return mapping[kind]


@app.command()
def run(
    experiment_path: Path = typer.Argument(
        ...,
        exists=True,
        readable=True,
        help="Path to the experiment JSON file.",
    ),
    results_path: Path = typer.Option(
        Path("results.json"),
        "--results",
        "-r",
        help="Path to save the results JSON file.",
    ),
    model_kind: str = typer.Option(
        "upper",
        "--model-kind",
        "-m",
        help="Built in model kind to use: echo, upper, reverse.",
    ),
) -> None:
    """
    Run an experiment from a JSON file using a simple built in model.
    """

    typer.echo(f"Loading experiment from {experiment_path}...")
    experiment: Experiment = load_experiment(experiment_path)

    model_fn = _get_model_function(model_kind)

    typer.echo(
        f"Running experiment '{experiment.name}' with model '{experiment.model_name}' (kind={model_kind})...",
    )
    results: List[RunResult] = run_experiment(experiment, model_fn)

    typer.echo(f"Saving {len(results)} results to {results_path}...")
    save_results(results, results_path)

    typer.echo("Done.")


def _load_gold_outputs(path: Path) -> List[str]:
    """
    Load gold outputs as a list of strings from a JSON file.
    """

    text = path.read_text(encoding="utf-8")
    data = json.loads(text)

    if not isinstance(data, list):
        raise ValueError("Gold outputs file must contain a JSON list.")

    items: List[str] = []
    for index, item in enumerate(data):
        if not isinstance(item, str):
            raise ValueError(
                f"Gold output at index {index} is not a string: {item!r}",
            )
        items.append(item)

    return items


@app.command()
def eval(
    results_path: Path = typer.Argument(
        ...,
        exists=True,
        readable=True,
        help="Path to the results JSON file.",
    ),
    gold_path: Path = typer.Argument(
        ...,
        exists=True,
        readable=True,
        help="Path to the gold outputs JSON file (list of strings).",
    ),
) -> None:
    """
    Evaluate results against gold outputs using exact match metric.
    """

    typer.echo(f"Loading results from {results_path}...")
    results: List[RunResult] = load_results(results_path)

    typer.echo(f"Loading gold outputs from {gold_path}...")
    gold_outputs: List[str] = _load_gold_outputs(gold_path)

    typer.echo("Running evaluation (exact_match)...")
    evaluated: List[EvaluatedResult] = evaluate_results(
        results=results,
        gold_outputs=gold_outputs,
        evaluators=[exact_match()],
    )

    total = len(evaluated)
    if total == 0:
        typer.echo("No results to evaluate.")
        raise typer.Exit(code=0)

    passed_count = 0
    for item in evaluated:
        for metric in item.metrics:
            if metric.name == "exact_match" and metric.passed:
                passed_count += 1

    accuracy = passed_count / total

    typer.echo(f"Evaluated {total} items.")
    typer.echo(f"Exact match accuracy: {accuracy:.3f}")
