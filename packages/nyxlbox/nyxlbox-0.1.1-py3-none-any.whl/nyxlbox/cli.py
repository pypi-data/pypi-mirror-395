from __future__ import annotations

import json
from pathlib import Path

import typer

from . import (
    Experiment,
    PromptCase,
    evaluate_results,
    exact_match,
    generate_markdown_report,
    load_experiment,
    load_experiment_yaml,
    load_results,
    run_experiment,
    save_results,
)

app = typer.Typer(help="NyxlBox command line interface.")


def _load_experiment_auto(path: Path) -> Experiment:
    suffix = path.suffix.lower()
    if suffix in {".yaml", ".yml"}:
        return load_experiment_yaml(path)
    return load_experiment(path)


def _get_model_callable(model_kind: str):
    normalized = model_kind.lower()
    if normalized == "echo":
        return lambda text: text
    if normalized == "upper":
        return lambda text: text.upper()
    if normalized == "reverse":
        return lambda text: text[::-1]
    raise typer.BadParameter(
        "Unknown model_kind. Supported values are: echo, upper, reverse."
    )


@app.command()
def run(
    experiment: Path = typer.Argument(
        ...,
        help="Path to experiment file (JSON or YAML).",
    ),
    results: Path = typer.Option(
        ...,
        "--results",
        "-r",
        help="Path to write results JSON file.",
    ),
    model_kind: str = typer.Option(
        "upper",
        "--model-kind",
        "-m",
        help="Built in model kind: echo, upper, reverse.",
    ),
) -> None:
    """
    Run an experiment and store results as JSON.
    """
    exp = _load_experiment_auto(experiment)
    model = _get_model_callable(model_kind)

    run_results = run_experiment(exp, model)

    save_results(run_results, results)

    typer.echo(
        f"Ran experiment '{exp.name}' with model '{exp.model_name}' on {len(run_results)} cases."
    )
    typer.echo(f"Saved results to {results}")


@app.command()
def eval(
    results_path: Path = typer.Argument(
        ...,
        help="Path to results JSON file.",
    ),
    gold_path: Path = typer.Argument(
        ...,
        help="Path to JSON file with expected outputs as a list of strings.",
    ),
) -> None:
    """
    Evaluate results against gold outputs using exact match.
    """
    results = load_results(results_path)

    gold_text = gold_path.read_text(encoding="utf-8")
    gold_outputs = json.loads(gold_text)

    if not isinstance(gold_outputs, list):
        raise typer.BadParameter(
            "Gold outputs file must contain a JSON list of strings."
        )

    evaluator = exact_match()
    evaluated = evaluate_results(
        results=results,
        gold_outputs=gold_outputs,
        evaluators=[evaluator],
    )

    total = len(evaluated)
    passed = 0

    for item in evaluated:
        for metric in item.metrics:
            if metric.name == "exact_match" and metric.passed:
                passed += 1

    accuracy = passed / total if total else 0.0

    typer.echo(f"Evaluated {total} items.")
    typer.echo(f"Exact match accuracy: {accuracy:.3f}")


@app.command()
def report(
    results_path: Path = typer.Argument(
        ...,
        help="Path to results JSON file.",
    ),
    gold_path: Path = typer.Argument(
        ...,
        help="Path to JSON file with expected outputs as a list of strings.",
    ),
    out: Path = typer.Option(
        ...,
        "--out",
        "-o",
        help="Path to write markdown report.",
    ),
    title: str = typer.Option(
        "NyxlBox experiment report",
        "--title",
        help="Title for the markdown report.",
    ),
) -> None:
    """
    Generate a markdown report from results and gold outputs.
    """
    results = load_results(results_path)

    gold_text = gold_path.read_text(encoding="utf-8")
    gold_outputs = json.loads(gold_text)

    if not isinstance(gold_outputs, list):
        raise typer.BadParameter(
            "Gold outputs file must contain a JSON list of strings."
        )

    report_text = generate_markdown_report(
        results=results,
        gold_outputs=gold_outputs,
        title=title,
    )

    out.write_text(report_text, encoding="utf-8")
    typer.echo(f"Report written to {out}")
