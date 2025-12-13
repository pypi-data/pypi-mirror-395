import nyxlbox


def dummy_model(prompt: str) -> str:
    return prompt.upper()


def test_exact_match_evaluation():
    experiment = nyxlbox.Experiment(
        name="eval_exact_match",
        model_name="dummy_model",
        cases=[
            nyxlbox.PromptCase(input_text="hello"),
            nyxlbox.PromptCase(input_text="nyxlbox"),
        ],
    )

    results = nyxlbox.run_experiment(experiment, dummy_model)

    gold_outputs = ["HELLO", "NYXLBOX"]
    evaluator = nyxlbox.exact_match()

    evaluated = nyxlbox.evaluate_results(
        results=results,
        gold_outputs=gold_outputs,
        evaluators=[evaluator],
    )

    assert len(evaluated) == 2

    for item in evaluated:
        assert len(item.metrics) == 1
        metric = item.metrics[0]
        assert metric.name == "exact_match"
        assert metric.passed is True
        assert metric.score == 1.0


def test_contains_substring_evaluation():
    experiment = nyxlbox.Experiment(
        name="eval_contains",
        model_name="dummy_model",
        cases=[
            nyxlbox.PromptCase(input_text="nyxlbox evaluation"),
        ],
    )

    results = nyxlbox.run_experiment(experiment, dummy_model)

    gold_outputs = ["NYXLBOX EVALUATION"]
    evaluator = nyxlbox.contains_substring("NYXLBOX")

    evaluated = nyxlbox.evaluate_results(
        results=results,
        gold_outputs=gold_outputs,
        evaluators=[evaluator],
    )

    assert len(evaluated) == 1
    metrics = evaluated[0].metrics
    assert len(metrics) == 1

    metric = metrics[0]
    assert metric.name == "contains_substring"
    assert metric.passed is True
    assert metric.score == 1.0
    assert "substring" in metric.details


def test_evaluate_results_length_mismatch_raises():
    experiment = nyxlbox.Experiment(
        name="length_mismatch",
        model_name="dummy_model",
        cases=[
            nyxlbox.PromptCase(input_text="one"),
            nyxlbox.PromptCase(input_text="two"),
        ],
    )

    results = nyxlbox.run_experiment(experiment, dummy_model)

    gold_outputs = ["ONE"]

    evaluator = nyxlbox.exact_match()

    try:
        nyxlbox.evaluate_results(
            results=results,
            gold_outputs=gold_outputs,
            evaluators=[evaluator],
        )
    except ValueError as exc:
        message = str(exc)
        assert "length mismatch" in message
    else:
        raise AssertionError("Expected ValueError for length mismatch")
