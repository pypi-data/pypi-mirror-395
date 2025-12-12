import argparse
import json
import os
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from fastchat.clients.openai import OpenAIClient
from fastchat.llm_judge.common import load_questions


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--model",
        type=str,
        required=True,
        help="The name or identifier of the model."
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=10,
        help="Request timeout for the model API."
    )
    parser.add_argument(
        "--max_retries",
        type=int,
        default=16,
        help="Max retries for the model API."
    )
    parser.add_argument(
        "--url",
        type=str,
        help="URL for the model API."
    )
    parser.add_argument(
        "--temperature",
        type=float,
        default=0.0,
        help="Temperature for the model API."
    )
    parser.add_argument(
        "--top_p",
        type=float,
        default=0.0001,
        help="Top-p for the model API."
    )
    parser.add_argument(
        "--max_tokens",
        type=int,
        default=1024,
        help="Max tokens for the model API."
    )
    parser.add_argument(
        "--api_key",
        type=str,
        help="Name of the env variable that stores API key for the model API."
    )
    parser.add_argument("--output_path", required=True)
    parser.add_argument(
        "--parallel",
        type=int,
        default=1,
        help="The number of concurrent API calls.",
    )
    parser.add_argument("--first_n", type=int, default=None, help="For debugging: limits number of questions to process")
    parser.add_argument("--mpi_rank", type=int, default=0, help="Rank of the process in MPI jobs")
    return parser.parse_args()


def main():
    args = parse_args()

    client = OpenAIClient(
        model=args.model,
        url=args.url,
        api_key=args.api_key,
        timeout=args.timeout,
        max_retries=args.max_retries,
        temperature=args.temperature,
        top_p=args.top_p,
    )

    def _infer_single(question: dict[str, str]) -> tuple[dict[str, str], dict[str, str]]:
        question_1_str = question["turns"][0]
        question_1 = {"role": "user", "content": question_1_str}
        response_1_str = client.generate([question_1])
        response_1 = {"role": "assistant", "content": response_1_str}
        question_2_str = question["turns"][1]
        question_2 = {"role": "user", "content": question_2_str}
        response_2_str = client.generate([question_1, response_1, question_2])
        response_2 = {"role": "assistant", "content": response_2_str}
        return response_1, response_2

    this_dir = Path(__file__).absolute().parent.parent
    data_path = os.path.join(this_dir, "data", "mt_bench")
    question_file = os.path.join(data_path, "question.jsonl")
    questions = load_questions(question_file, None, args.first_n)

    if args.parallel == 1:
        responses = map(_infer_single, questions)
    else:
        with ThreadPoolExecutor(args.parallel) as executor:
            responses = executor.map(_infer_single, questions)

    output = []
    for q, (first_turn, second_turn) in zip(questions, responses):
        q["choices"] = [{"index": 0, "turns": [first_turn["content"], second_turn["content"]]}]
        output.append(q)

    if args.mpi_rank==0:
        out_file = os.path.join(args.output_path, f"{args.model.split('/')[-1]}.jsonl")
        os.makedirs(args.output_path, exist_ok=True)
        with open(out_file, "w") as fp:
            fp.write("\n".join(map(json.dumps, output)))


if __name__ == "__main__":
    main()
