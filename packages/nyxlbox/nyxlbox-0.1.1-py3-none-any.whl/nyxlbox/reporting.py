from __future__ import annotations

from pathlib import Path
from typing import Iterable, List

from .core import RunResult
from .eval import EvaluatedResult, exact_match, evaluate_results


def _escape_cell(value: str) -> str:
    # Simple escape to avoid breaking markdown tables
    return value.replace("|", "\\|").replace("\n", " ")


def generate_markdown_report(
    results: Iterable[RunResult],
    gold_outputs: List[str],
    title: str = "NyxlBox experiment report",
) -> str:
    """
    Generate a simple markdown report for a set of results and gold outputs
    using exact match accuracy.
    """
    results_list = list(results)

    evaluated: List[EvaluatedResult] = evaluate_results(
        results=results_list,
        gold_outputs=gold_outputs,
        evaluators=[exact_match()],
    )

    total = len(evaluated)
    passed = 0

    rows = []

    for idx, item in enumerate(evaluated):
        res = item.result
        gold = gold_outputs[idx] if idx < len(gold_outputs) else ""

        exact = next(
            (m for m in item.metrics if m.name == "exact_match"),
            None,
        )

        passed_flag = bool(exact and exact.passed)
        if passed_flag:
            passed += 1

        rows.append(
            {
                "case_id": res.case_id,
                "input_text": res.input_text or "",
                "output_text": res.output_text or "",
                "gold_output": gold,
                "passed": "yes" if passed_flag else "no",
            }
        )

    accuracy = passed / total if total else 0.0

    lines: List[str] = []
    lines.append(f"# {title}")
    lines.append("")
    lines.append(f"- Total cases: {total}")
    lines.append(f"- Exact match accuracy: {accuracy:.3f}")
    lines.append("")
    lines.append("| case_id | input | output | expected | pass |")
    lines.append("|---------|-------|--------|----------|------|")

    for row in rows:
        lines.append(
            "| "
            + " | ".join(
                [
                    _escape_cell(str(row["case_id"])),
                    _escape_cell(row["input_text"]),
                    _escape_cell(row["output_text"]),
                    _escape_cell(row["gold_output"]),
                    _escape_cell(row["passed"]),
                ]
            )
            + " |"
        )

    lines.append("")
    return "\n".join(lines)


def save_markdown_report(
    results: Iterable[RunResult],
    gold_outputs: List[str],
    path: str | Path,
    title: str = "NyxlBox experiment report",
) -> None:
    path_obj = Path(path)
    text = generate_markdown_report(results, gold_outputs, title=title)
    path_obj.write_text(text, encoding="utf-8")
