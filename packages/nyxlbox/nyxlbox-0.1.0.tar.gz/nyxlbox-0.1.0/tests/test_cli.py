import json
from pathlib import Path

from typer.testing import CliRunner

from nyxlbox.cli import app
from nyxlbox import Experiment, PromptCase, save_experiment, load_results


runner = CliRunner()


def create_sample_experiment(tmp_path: Path) -> Path:
    experiment = Experiment(
        name="cli_test",
        model_name="dummy_cli_model",
        cases=[
            PromptCase(input_text="hello"),
            PromptCase(input_text="nyxlbox"),
        ],
    )

    experiment_path = tmp_path / "experiment.json"
    save_experiment(experiment, experiment_path)
    return experiment_path


def create_gold_file(tmp_path: Path) -> Path:
    gold_outputs = ["HELLO", "NYXLBOX"]
    gold_path = tmp_path / "gold.json"
    gold_path.write_text(json.dumps(gold_outputs), encoding="utf-8")
    return gold_path


def test_cli_run_creates_results(tmp_path):
    experiment_path = create_sample_experiment(tmp_path)
    results_path = tmp_path / "results.json"

    result = runner.invoke(
        app,
        [
            "run",
            str(experiment_path),
            "--results",
            str(results_path),
            "--model-kind",
            "upper",
        ],
    )

    assert result.exit_code == 0
    assert results_path.exists()

    results = load_results(results_path)
    assert len(results) == 2
    outputs = [item.output_text for item in results]
    assert outputs == ["HELLO", "NYXLBOX"]


def test_cli_eval_reports_accuracy(tmp_path):
    experiment_path = create_sample_experiment(tmp_path)
    results_path = tmp_path / "results.json"

    run_result = runner.invoke(
        app,
        [
            "run",
            str(experiment_path),
            "--results",
            str(results_path),
            "--model-kind",
            "upper",
        ],
    )
    assert run_result.exit_code == 0

    gold_path = create_gold_file(tmp_path)

    eval_result = runner.invoke(
        app,
        [
            "eval",
            str(results_path),
            str(gold_path),
        ],
    )

    assert eval_result.exit_code == 0
    text = eval_result.stdout

    assert "Evaluated 2 items." in text
    assert "Exact match accuracy: 1.000" in text
