import json
from glob import glob

import pathlib

from nemo_evaluator.api.api_dataclasses import EvaluationResult, MetricResult, Score, TaskResult, GroupResult


def parse_output(output_dir: str) -> EvaluationResult:
    results_files = list(pathlib.Path(output_dir).rglob("**/result.json"))
    if not results_files:
        raise FileNotFoundError("Failed to find `result.json`.")
    if len(results_files) > 1:
        raise ValueError(
            "More than 1 `result.json` files found. `output_dir` must contain a single evaluation"
        )
    with open(results_files[0]) as fp:
        results = json.load(fp)
    
    judge = results["judge"]
    # NOTE(dfridman): following the convention `BENCHMARK_NAME:JUDGE_NAME`
    task = f"{results['task']}:{judge}"
    group_result = GroupResult(
        metrics={
            "average_score": MetricResult(
                scores={
                    "average_score": Score(
                        value=results["total"],
                        stats={}
                    ),
                    "num_missing": Score(value=results["num_missing"], stats={}),
                }
            )
        }
    )
    groups = {task: group_result}

    tasks = {}
    for category, category_score in results["category"].items():
        task_result = TaskResult(
            metrics={
                "average_score": MetricResult(
                    scores={
                        "average_score": Score(
                            value=category_score,
                            stats={}
                        )
                    }
                )
            }
        )
        tasks[category] = task_result
    evaluation_result = EvaluationResult(
        tasks=tasks,
        groups=groups
    )
    return evaluation_result
