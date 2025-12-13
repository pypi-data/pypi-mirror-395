import nyxlbox


def dummy_model(prompt: str) -> str:
    return prompt[::-1]


def test_experiment_json_round_trip():
    experiment = nyxlbox.Experiment(
        name="reverse_test",
        model_name="dummy_model",
        cases=[
            nyxlbox.PromptCase(input_text="alpha", case_id="a1"),
            nyxlbox.PromptCase(input_text="beta", case_id="b2"),
        ],
        metadata={"purpose": "json_roundtrip"},
    )

    json_text = nyxlbox.experiment_to_json(experiment)
    loaded = nyxlbox.experiment_from_json(json_text)

    assert loaded.name == experiment.name
    assert loaded.model_name == experiment.model_name
    assert len(loaded.cases) == 2
    assert loaded.metadata["purpose"] == "json_roundtrip"
    assert loaded.cases[0].input_text == "alpha"
    assert loaded.cases[0].case_id == "a1"


def test_experiment_file_round_trip(tmp_path):
    experiment = nyxlbox.Experiment(
        name="file_roundtrip",
        model_name="dummy_model",
        cases=[
            nyxlbox.PromptCase(input_text="gamma"),
        ],
    )

    path = tmp_path / "experiment.json"
    nyxlbox.save_experiment(experiment, path)

    loaded = nyxlbox.load_experiment(path)

    assert loaded.name == "file_roundtrip"
    assert len(loaded.cases) == 1
    assert loaded.cases[0].input_text == "gamma"


def test_results_file_round_trip(tmp_path):
    experiment = nyxlbox.Experiment(
        name="results_test",
        model_name="dummy_model",
        cases=[
            nyxlbox.PromptCase(input_text="one"),
            nyxlbox.PromptCase(input_text="two"),
        ],
    )

    results = nyxlbox.run_experiment(experiment, dummy_model)

    path = tmp_path / "results.json"
    nyxlbox.save_results(results, path)

    loaded_results = nyxlbox.load_results(path)

    assert len(loaded_results) == len(results)

    original_outputs = [item.output_text for item in results]
    loaded_outputs = [item.output_text for item in loaded_results]

    assert original_outputs == loaded_outputs

    for item in loaded_results:
        assert item.model_name == "dummy_model"
        assert item.started_at <= item.finished_at
