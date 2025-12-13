import nyxlbox


def dummy_model(prompt: str) -> str:
    return prompt.upper()


def test_can_import_nyxlbox():
    assert hasattr(nyxlbox, "__version__")
    assert isinstance(nyxlbox.__version__, str)
    assert len(nyxlbox.__version__) > 0


def test_run_experiment_returns_results():
    experiment = nyxlbox.Experiment(
        name="uppercase_test",
        model_name="dummy_model",
        cases=[
            nyxlbox.PromptCase(input_text="hello"),
            nyxlbox.PromptCase(input_text="nyxlbox"),
        ],
    )

    results = nyxlbox.run_experiment(experiment, dummy_model)

    assert len(results) == 2

    for result in results:
        assert result.output_text == result.input_text.upper()
        assert result.model_name == "dummy_model"
        assert result.started_at <= result.finished_at
        assert result.error is None
