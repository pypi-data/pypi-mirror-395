"""
Usage:
python gen_judgment.py --model-list [LIST-OF-MODEL-ID] --parallel [num-concurrent-api-call] --mode [single|pairwise-baseline|pairwise-all]
"""
import argparse
import os
from concurrent.futures import ThreadPoolExecutor
import json
from pathlib import Path

import numpy as np
from tqdm import tqdm

from fastchat.llm_judge.common import (
    load_questions,
    load_model_answers,
    load_judge_prompts,
    check_data,
    play_a_match_pair,
    play_a_match_single,
    get_model_list,
    Judge,
    MatchPair,
    MatchSingle,
    NEED_REF_CATS,
    load_cache,
    lookup_cache
)
from fastchat.clients.openai import OpenAIClient

def make_match(
    questions,
    models,
    model_answers,
    judge,
    baseline_model,
    ref_answers=None,
    multi_turn=False,
):
    matches = []
    for q in questions:
        if multi_turn and len(q["turns"]) != 2:
            continue
        for i in range(len(models)):
            q_id = q["question_id"]
            m_1 = models[i]
            m_2 = baseline_model
            if m_1 == m_2:
                continue
            a_1 = model_answers[m_1][q_id]
            a_2 = model_answers[baseline_model][q_id]
            if ref_answers is not None:
                ref = ref_answers[judge.model_name][q_id]
                match = MatchPair(
                    dict(q),
                    m_1,
                    m_2,
                    a_1,
                    a_2,
                    judge,
                    ref_answer=ref,
                    multi_turn=multi_turn,
                )
            else:
                match = MatchPair(
                    dict(q), m_1, m_2, a_1, a_2, judge, multi_turn=multi_turn
                )
            matches.append(match)
    return matches


def make_match_all_pairs(
    questions,
    models,
    model_answers,
    judge,
    baseline_model=None,
    ref_answers=None,
    multi_turn=False,
):
    matches = []
    for q in questions:
        if multi_turn and len(q["turns"]) != 2:
            continue
        for i in range(len(models)):
            for j in range(i + 1, len(models)):
                q_id = q["question_id"]
                m_1 = models[i]
                m_2 = models[j]
                a_1 = model_answers[m_1][q_id]
                a_2 = model_answers[m_2][q_id]
                if ref_answers is not None:
                    ref = ref_answers[judge.model_name][q_id]
                    match = MatchPair(
                        dict(q),
                        m_1,
                        m_2,
                        a_1,
                        a_2,
                        judge,
                        ref_answer=ref,
                        multi_turn=multi_turn,
                    )
                else:
                    match = MatchPair(
                        dict(q), m_1, m_2, a_1, a_2, judge, multi_turn=multi_turn
                    )
                matches.append(match)
    return matches


def make_match_single(
    questions,
    models,
    model_answers,
    judge,
    baseline_model=None,
    ref_answers=None,
    multi_turn=False,
):
    matches = []
    for q in questions:
        if multi_turn and len(q["turns"]) != 2:
            continue
        for i in range(len(models)):
            q_id = q["question_id"]
            m = models[i]
            a = model_answers[m].get(q_id)
            if a is None:
                # NOTE(dfridman): allow absent responses (see `check_data`` function)
                continue
            if ref_answers is not None:
                ref = ref_answers[judge.model_name][q_id]
                matches.append(
                    MatchSingle(
                        dict(q), m, a, judge, ref_answer=ref, multi_turn=multi_turn
                    )
                )
            else:
                matches.append(MatchSingle(dict(q), m, a, judge, multi_turn=multi_turn))
    return matches


def make_judge_pairwise(judge_model, judge_prompts):
    judges = {}
    judges["default"] = Judge(judge_model, judge_prompts["pair-v2"])
    judges["math"] = Judge(judge_model, judge_prompts["pair-math-v1"], ref_based=True)
    judges["default-mt"] = Judge(
        judge_model, judge_prompts["pair-v2-multi-turn"], multi_turn=True
    )
    judges["math-mt"] = Judge(
        judge_model,
        judge_prompts["pair-math-v1-multi-turn"],
        ref_based=True,
        multi_turn=True,
    )
    return judges


def make_judge_single(judge_model, judge_prompts):
    judges = {}
    judges["default"] = Judge(judge_model, judge_prompts["single-v1"])
    judges["math"] = Judge(judge_model, judge_prompts["single-math-v1"], ref_based=True)
    judges["default-mt"] = Judge(
        judge_model, judge_prompts["single-v1-multi-turn"], multi_turn=True
    )
    judges["math-mt"] = Judge(
        judge_model,
        judge_prompts["single-math-v1-multi-turn"],
        ref_based=True,
        multi_turn=True,
    )
    return judges


if __name__ == "__main__":
    this_dir = Path(__file__).absolute().parent.parent
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--responses_dir",
        type=str,
        default=None,
        help="Directory with .jsonl model responses. If not provided, assumes the data is at --output_path"
    )
    parser.add_argument(
        "--output_path",
        type=str,
        default="/results",
        help="Directory to output results of the run",
    )
    parser.add_argument(
        "--judge-file",
        type=str,
        default=os.path.join(this_dir, "data", "judge_prompts.jsonl"),
        help="The file of judge prompts.",
    )
    parser.add_argument(
        "--reference-model",
        type=str,
        default="gpt-4",
        choices=["gpt-4", "gpt-4-0125-preview"],
        help="Allow only 2 sets of reference answers. One - for MT-Bench (gpt-4), another - for MT-Bench-cor1 (gpt-4-0125-preview)"
    )
    parser.add_argument("--baseline-model", type=str, default="gpt-3.5-turbo")
    parser.add_argument(
        "--mode",
        type=str,
        default="single",
        choices=["pairwise-baseline", "pairwise-all", "single"],
        help=(
            "Evaluation mode. "
            "`pairwise-baseline` runs pairwise comparision against a baseline. "
            "`pairwise-all` runs pairwise comparision between all pairs. "
            "`single` runs single answer grading."
        ),
    )
    parser.add_argument(
        "--model-list",
        type=str,
        nargs="+",
        default=None,
        help="A list of models to be evaluated",
    )
    parser.add_argument(
        "--parallel", type=int, default=1, help="The number of concurrent API calls."
    )
    parser.add_argument(
        "--first-n", type=int, help="A debug option. Only run the first `n` judgments."
    )
    # Judge args
    parser.add_argument(
        "--judge-model", type=str, default="gpt-4",
        help="The name or identifier of the judge model. GPT-4 by default."
    )
    parser.add_argument("--judge_url", type=str, default=None, help="URL for the judge API. Default: None")
    parser.add_argument("--judge_api_key_name", type=str, default=None,  help="Name of the env variable that stores API key for the judge API. Default: None")
    parser.add_argument("--judge_request_timeout", type=int, default=60, help="Request timeout for the judge API. Default: 60")
    parser.add_argument("--judge_max_retries", type=int, default=16, help="Max retries for the judge API. Default: 16")
    parser.add_argument("--judge_temperature", type=float, default=0.0, help="Temperature for the judge API. Default: 0.0")
    parser.add_argument("--judge_top_p", type=float, default=0.0001, help="Top-p for the judge API. Default: 0.0001")
    parser.add_argument("--judge_max_tokens", type=int, default=1024, help="Max tokens for the judge API. Default: 1024")
    args = parser.parse_args()

    judge_config = {
        "model": args.judge_model,
        "url": args.judge_url,
        "api_key": args.judge_api_key_name,
        "timeout": args.judge_request_timeout,
        "max_retries": args.judge_max_retries,
        "temperature": args.judge_temperature,
        "top_p": args.judge_top_p,
        "max_tokens": args.judge_max_tokens,
    }

    client = OpenAIClient(**judge_config)

    data_path = os.path.join(this_dir, "data", "mt_bench")
    question_file = os.path.join(data_path, "question.jsonl")

    answer_dir = args.responses_dir
    if answer_dir is None:
        answer_dir = os.path.join(args.output_path, "responses")
    ref_answer_dir = os.path.join(data_path, "reference_answer")

    # Load questions
    questions = load_questions(question_file, None, None)

    # Load answers
    model_answers = load_model_answers(answer_dir)
    ref_answers = load_model_answers(ref_answer_dir)
    ref_answers[args.judge_model] = ref_answers[args.reference_model]

    # Load judge
    judge_prompts = load_judge_prompts(args.judge_file)

    if args.first_n:
        questions = questions[: args.first_n]

    if args.model_list is None:
        models = get_model_list(answer_dir)
    else:
        models = args.model_list

    judgements_dir = os.path.join(args.output_path, "judgements")
    if args.mode == "single":
        judges = make_judge_single(args.judge_model, judge_prompts)
        play_a_match_func = play_a_match_single
        output_file = os.path.join(judgements_dir, f"{args.judge_model.strip('/').replace('/', '--')}_single.jsonl")
        make_match_func = make_match_single
        baseline_model = None
    else:
        judges = make_judge_pairwise(args.judge_model, judge_prompts)
        play_a_match_func = play_a_match_pair
        output_file = os.path.join(judgements_dir, f"{args.judge_model.strip('/').replace('/', '--')}_pair.jsonl")
        if args.mode == "pairwise-all":
            make_match_func = make_match_all_pairs
            baseline_model = None
        else:
            make_match_func = make_match
            baseline_model = args.baseline_model


    check_data(questions, model_answers, ref_answers, models, judges)

    # Make matches
    matches = []

    question_math = [q for q in questions if q["category"] in NEED_REF_CATS]
    question_default = [q for q in questions if q["category"] not in NEED_REF_CATS]

    matches += make_match_func(
        question_default, models, model_answers, judges["default"], baseline_model
    )
    matches += make_match_func(
        question_math,
        models,
        model_answers,
        judges["math"],
        baseline_model,
        ref_answers,
    )
    matches += make_match_func(
        question_default,
        models,
        model_answers,
        judges["default-mt"],
        baseline_model,
        multi_turn=True,
    )
    matches += make_match_func(
        question_math,
        models,
        model_answers,
        judges["math-mt"],
        baseline_model,
        ref_answers,
        multi_turn=True,
    )

    match_stat = {}
    match_stat["bench_name"] = "mt_bench"
    match_stat["mode"] = args.mode
    match_stat["judge"] = args.judge_model
    match_stat["baseline"] = baseline_model
    match_stat["model_list"] = models
    match_stat["total_num_questions"] = len(questions)
    match_stat["total_num_matches"] = len(matches)
    match_stat["output_path"] = output_file

    # Show match stats and prompt enter to continue
    print("Stats:")
    print(json.dumps(match_stat, indent=4))
    #input("Press Enter to confirm...")

    # Play matches
    cache = load_cache(output_file)
    matches = [
        # do not recompute
        m for m in matches if lookup_cache(m, cache) == -1
    ]
    if args.parallel == 1:
        for match in tqdm(matches):
            play_a_match_func(match, output_file=output_file, client=client)
    else:

        def play_a_match_wrapper(match):
            play_a_match_func(match, output_file=output_file, client=client)

        np.random.seed(0)
        np.random.shuffle(matches)

        with ThreadPoolExecutor(args.parallel) as executor:
            for match in tqdm(
                executor.map(play_a_match_wrapper, matches), total=len(matches)
            ):
                pass
