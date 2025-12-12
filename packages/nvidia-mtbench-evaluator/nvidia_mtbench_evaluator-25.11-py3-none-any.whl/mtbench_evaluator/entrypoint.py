'''
This script hits a hosted model at the specified url and generates mtbench responses.
It then feeds those responses to gpt-4 (by hitting either an Azure OpenAI endpoint or OpenAI directly)
and generates judgements.
Lastly it aggregates together the scores from the judgements and renders a leaderboard

'''
import argparse
import os
from pathlib import Path
import subprocess
import sys


import pty
from mtbench_evaluator.fastchat.fastchat.clients.openai import OpenAIClient


def validate_judge(client):
    print("Validating judge setup, should take a minute or less")
    try:
        response = client.generate(
            messages=[
                {"role": "system", "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair."},
                {"role": "user", "content": "Compose a poem that explains the concept of recursion in programming."}
            ],
        )
        validation_ok = True
    except Exception as e:
        print(f"Error ocurred during judge validation: {type(e)}, {e}")
    if not validation_ok:
        print("Your Judge is not able to be contacted successfully. This is a preliminary check that is unrelated to mtbench.\n Please verify you are successfully able to hit the endpoint (e.g. send a curl request to it)")
        sys.exit(1)
    print("Judge Setup Validated")

def run_command(command, cwd=None):
    master, slave = pty.openpty()
    process = subprocess.Popen(command, stdout=slave, stderr=slave, stdin=subprocess.PIPE, cwd=cwd)
    os.close(slave)

    while True:
        try:
            output = os.read(master, 1024)
        except OSError:
            break
        if not output:
            break
        print(output.decode(), end='', flush=True)

    rc = process.wait()
    return rc

def run_mtbench(
        workdir,
        model,
        timeout,
        max_retries,
        url,
        temperature,
        top_p,
        max_tokens,
        api_key,
        first_n,
        parallelism,
        mpi_rank,
    ):
    print(f"Running mtbench run")
    try:
        os.makedirs(f"{workdir}/responses", exist_ok=True)
    except OSError as error:
        print(f"An error occurred while creating directory {workdir}/responses: {error}")
        raise error

    command = [
        "python", "-m",
        "fastchat.llm_judge.scripts.mt_inference",
        "--model", model,
        "--timeout", str(timeout),
        "--max_retries", str(max_retries),
        "--temperature", str(temperature),
        "--top_p", str(top_p),
        "--max_tokens", str(max_tokens),
        "--output_path", f"{workdir}/responses",
        "--parallel", str(parallelism),
        "--mpi_rank", str(mpi_rank),
    ]

    if api_key:
        command += ["--api_key", api_key]
    
    if url:
        command += ["--url", url]

    if first_n:
        command += ["--first_n", str(first_n)]

    current_parent = str(Path(__file__).parent)
    return_code = run_command(command, cwd=os.path.join(current_parent, 'fastchat'))

    if return_code != 0:
        raise RuntimeError("Obtaining mtbench results failed")

def judge_responses(workdir, judge_config, judge_parallelism, judge_reference_model, first_n=None):
    try:
        os.makedirs(f"{workdir}/judgements", exist_ok=True)
    except OSError as error:
        print(f"An error occurred while creating directory {workdir}/judgements: {error}")
        raise error
    command = [
        "python", "-m",
        "fastchat.llm_judge.scripts.gen_judgment",
        "--judge-model", judge_config["model"],
        "--parallel", str(judge_parallelism),
        "--judge_request_timeout", str(judge_config["timeout"]),
        "--judge_max_retries", str(judge_config["max_retries"]),
        "--judge_temperature", str(judge_config["temperature"]),
        "--judge_top_p", str(judge_config["top_p"]),
        "--judge_max_tokens", str(judge_config["max_tokens"]),
        "--output_path", f"{workdir}",
    ]
    if judge_config["api_key"]:
        command += ["--judge_api_key_name", judge_config["api_key"]]

    if judge_config["url"]:
        command += ["--judge_url", judge_config["url"]]

    if first_n:
        command += ["--first-n", str(first_n)]
    if judge_reference_model:
        command += ["--reference-model", judge_reference_model]

    print("Beginning Judging")
    current_parent = str(Path(__file__).parent)
    return_code = run_command(command, cwd=os.path.join(current_parent, 'fastchat'))

    if return_code != 0:
        print("Judging failed")
        sys.exit(1)


def produce_summary(workdir, judge_model, judge_reference_model):
    command = [
        "python", "-m",
        "fastchat.llm_judge.scripts.render_result_json",
        "--workdir", f"{workdir}",
        "--judge_name", f"{judge_model}",
        "--reference-model", judge_reference_model
    ]
    print("Generating result")
    current_parent = str(Path(__file__).parent)
    return_code = run_command(command, cwd=os.path.join(current_parent, 'fastchat'))

    if return_code != 0:
        print("Result generation failed!")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description='Script for generating and judging MTBench results.')

    #general arguments
    parser.add_argument(
        "--model",
        type=str,
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
    parser.add_argument('--workdir', type=str,default='/workspace/', help="Folder where results will be accessed and stored")
    parser.add_argument(
        "--parallelism",
        type=int,
        default=1,
        help="The number of concurrent API calls to the model API.",
    )
    parser.add_argument('--first_n', type=int, default=None, help="Number of samples to process, for debug purposes")

    parser.add_argument('--judge', action='store_true', help='Judge responses')
    parser.add_argument('--generate', action='store_true', help='Generate responses')

    #arguments specific to judging mtbench results
    parser.add_argument('--judge_model', type=str, default='gpt-4', help="GPT-4 by default")
    parser.add_argument('--judge_reference_model', type=str, default="gpt-4", choices=["gpt-4", "gpt-4-0125-preview"], help="Source of references to be used in judging")
    parser.add_argument('--judge_parallelism', type=int, default=1, help='Number of thread workers for judge to use. If using nvidia azure endpoint you typically need to have the rate limit increased before being able to use this')
    parser.add_argument("--judge_url", type=str, default=None, help="URL for the judge API. Default: None")
    parser.add_argument("--judge_api_key_name", type=str, default=None,  help="Name of the env variable that stores API key for the judge API. Default: None")
    parser.add_argument("--judge_request_timeout", type=int, default=60, help="Request timeout for the judge API. Default: 60")
    parser.add_argument("--judge_max_retries", type=int, default=16, help="Max retries for the judge API. Default: 16")
    parser.add_argument("--judge_temperature", type=float, default=0.0, help="Temperature for the judge API. Default: 0.0")
    parser.add_argument("--judge_top_p", type=float, default=0.0001, help="Top-p for the judge API. Default: 0.0001")
    parser.add_argument("--judge_max_tokens", type=int, default=1024, help="Max tokens for the judge API. Default: 1024")

    args = parser.parse_args()

    mpi_rank = 0

    if args.judge and mpi_rank==0:
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
        validate_judge(client)
    # NOTE(dfridman): lstrip("/") - otherwise, workdir_model_path becomes args.model
    abs_workdir = os.path.abspath(args.workdir)
    workdir_model_path = os.path.join(abs_workdir, "mtbench", args.model.lstrip("/"))
    if args.first_n:
        workdir_model_path = os.path.join(workdir_model_path, f"first_{args.first_n}")
    if args.generate:
        run_mtbench(
            workdir_model_path,
            args.model,
            args.timeout,
            args.max_retries,
            args.url,
            args.temperature,
            args.top_p,
            args.max_tokens,
            args.api_key,
            args.first_n,
            args.parallelism,
            mpi_rank,
        )

    if mpi_rank==0 and args.judge:
        judge_responses(
            workdir_model_path,
            judge_config,
            args.judge_parallelism,
            args.judge_reference_model,
            args.first_n
        )
        produce_summary(workdir_model_path, args.judge_model, args.judge_reference_model)


if __name__ == "__main__":
    main()
