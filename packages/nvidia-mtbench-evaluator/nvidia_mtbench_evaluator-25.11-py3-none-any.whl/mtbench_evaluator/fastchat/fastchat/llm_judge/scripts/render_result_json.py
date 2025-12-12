import argparse
from pathlib import Path
import os

import pandas as pd
import json


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--workdir", required=True, type=str)
    parser.add_argument(
        "--reference-model",
        required=True,
        choices=["gpt-4", "gpt-4-0125-preview"],
        help="Allow only 2 sets of reference answers. One - for MT-Bench (gpt-4), another - for MT-Bench-cor1 (gpt-4-0125-preview)"
    )
    parser.add_argument("--judge_name", default="gpt-4", type=str)
    args = parser.parse_args()

    judge_name = args.judge_name.strip("/").replace("/", "--")

    df_results = pd.read_json(os.path.join(args.workdir, "judgements", f"{judge_name}_single.jsonl"), lines=True)
    df_results = df_results.sort_values(by=["question_id", "turn"])[["question_id", "turn", "score"]]

    question_file = os.path.join(Path(__file__).absolute().parent.parent, "data", "mt_bench", "question.jsonl")
    df_questions = pd.read_json(question_file, lines=True)[["question_id", "category"]]
    df_results = df_results.merge(df_questions, on="question_id")

    missing = df_results["score"]==-1
    df_results = df_results[~missing]

    category_scores = df_results.groupby(by="category").mean().to_dict()["score"]

    task = {
        "gpt-4": "mtbench",
        "gpt-4-0125-preview": "mtbench_cor1"
    }[args.reference_model]

    output = {
        "total": df_results["score"].mean(),
        "category": category_scores,
        "num_missing": int(missing.sum()),
        "judge": args.judge_name,
        "task": task,
    }

    # NOTE(dfridman): no prefix for gpt-4 for backward-compatibility
    prefix = ""
    if args.judge_name != "gpt-4":
        prefix = f"{judge_name}-"

    with open(os.path.join(args.workdir, f"{prefix}result.json"), "w") as f:
        json.dump(output, f)