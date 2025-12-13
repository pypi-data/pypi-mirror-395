import nyxlbox


def reverse_model(prompt: str) -> str:
    return prompt[::-1]


def test_function_adapter_calls_underlying_function():
    adapter = nyxlbox.FunctionAdapter(reverse_model, name="reverse_adapter")

    output = adapter("abc")
    assert output == "cba"
    assert adapter.name == "reverse_adapter"


def test_function_adapter_works_with_run_experiment():
    experiment = nyxlbox.Experiment(
        name="adapter_experiment",
        model_name="reverse_model",
        cases=[
            nyxlbox.PromptCase(input_text="one"),
            nyxlbox.PromptCase(input_text="two"),
        ],
    )

    adapter = nyxlbox.FunctionAdapter(reverse_model)

    results = nyxlbox.run_experiment(experiment, adapter)

    outputs = [item.output_text for item in results]
    assert outputs == ["eno", "owt"]

    for item in results:
        assert item.model_name == "reverse_model"
        assert item.error is None
