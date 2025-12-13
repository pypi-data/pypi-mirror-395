# NyxlBox

NyxlBox is a lightweight framework for defining, running, evaluating, and reporting on LLM-style prompt experiments.  
It supports JSON/YAML experiment files, CLI execution, evaluation metrics, and markdown report generation.

---

## Installation

pip install nyxlbox

Requires Python 3.10+.

---

## Quick Start

Create experiment.yaml:

name: demo
model_name: upper
cases:
  - input_text: "hello"
  - input_text: "nyxlbox"

Run experiment:

nyxlbox run experiment.yaml --results results.json --model-kind upper

Evaluate:

nyxlbox eval results.json gold.json

Generate markdown report:

nyxlbox report results.json gold.json --out report.md

---

## Python API Example

from nyxlbox import (
    Experiment, PromptCase, run_experiment,
    evaluate_results, exact_match,
)

exp = Experiment(
    name="demo",
    model_name="upper",
    cases=[PromptCase(input_text="hello")],
)

results = run_experiment(exp, lambda t: t.upper())
evaluated = evaluate_results(results, ["HELLO"], [exact_match()])

---

## YAML Support

Simple YAML:

name: demo
model_name: upper
cases:
  - input_text: hello

Rich YAML:

experiment:
  name: demo
  model_name: upper
  cases:
    - input_text: hello

model_kind: upper
gold_outputs:
  - HELLO

---

## CLI Commands

nyxlbox run EXP --results OUT --model-kind upper  
nyxlbox eval RESULTS GOLD  
nyxlbox report RESULTS GOLD --out REPORT.md  

---

## Features

- JSON & YAML experiment definitions  
- Experiment runner  
- Exact match & substring evaluation  
- Markdown reporting  
- CLI tool and Python API  
- Extensible adapter system  

---

## License

Apache License 2.0
