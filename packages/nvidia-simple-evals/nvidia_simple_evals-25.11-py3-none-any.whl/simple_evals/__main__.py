import argparse
import asyncio
import json
import logging
import os
import random
import numpy as np
from pathlib import Path
from typing import Union
import simple_evals.common as common
from simple_evals.constants import GPQA_VARIANTS, MULTILINGUAL_MMLU, MULTILINGUAL_MMLU_LITE
from simple_evals.evals.gpqa_eval import GPQAEval
from simple_evals.evals.humaneval_eval import HumanEval
from simple_evals.evals.simpleqa_eval import SimpleQAEval
from simple_evals.evals.math_eval import MathEval
from simple_evals.evals.mgsm_eval import MGSMEval
from simple_evals.evals.mmlu_eval import MMLUEval
from simple_evals.evals.mmlu_pro_eval import MMLUProEval
from simple_evals.evals.browsecomp_eval import BrowseCompEval
from simple_evals.evals.healthbench_eval import HealthBenchEval
from simple_evals.sampler.chat_completion_sampler import (
    OPENAI_SYSTEM_MESSAGE_API, ChatCompletionSampler)
from simple_evals.seed_generator import SeedGenerator
from simple_evals.custom_parametrization.config_loader import EvalConfig


def int_or_float(value):
    try:
        if "." in value:
            return float(value)
        return int(value)
    except ValueError:
        raise argparse.ArgumentTypeError(f"Invalid number: {value}")


async def run():
    parser = argparse.ArgumentParser(
        description="Run a single evaluation using a specified model and evaluation type."
    )
    parser.add_argument(
        "--model",
        type=str,
        default="meta/llama-3.1-8b-instruct",
        help="Model name to use. Default: meta/llama-3.1-8b-instruct",
    )
    parser.add_argument(
        "--eval_name",
        type=str,
        default="mmlu",
        choices=[
            "math_test_500", "AIME_2024", "AIME_2025",  "AA_math_test_500", "AA_AIME_2024",
            "mmlu", "mmlu_pro", "mgsm", "humaneval", "humanevalplus", "simpleqa",
            "math_test_500_nemo", "aime_2024_nemo", "aime_2025_nemo",
            "browsecomp", "healthbench", "healthbench_hard", "healthbench_consensus"]
        + MULTILINGUAL_MMLU
        + MULTILINGUAL_MMLU_LITE
        + GPQA_VARIANTS,
        help="Name of the evaluation to run. Default: math",
    )
    parser.add_argument(
        "--url",
        type=str,
        default="https://integrate.api.nvidia.com/v1/chat/completions",
        help="URL for the model API. Default: https://integrate.api.nvidia.com/v1/chat/completions",
    )
    parser.add_argument(
        "--examples", type=int, help="Number of examples to use (overrides default)"
    )
    parser.add_argument(
        "--temperature",
        type=float,
        default=0,
        help="Sampling temperature. Default: 0.0.",
    )
    parser.add_argument(
        "--top_p",
        type=float,
        default=1.0,
        help="Top-p sampling parameter. Default: 1.0.",
    )
    parser.add_argument(
        "--max_tokens",
        type=int,
        default=4096,
        help="Maximum number of tokens for the model to generate. Default: 512.",
    )
    parser.add_argument(
        "--out_dir",
        type=str,
        default="/tmp",
        help="Directory to save output files. Default: /tmp",
    )
    parser.add_argument(
        "--max_retries", type=int, default=10, help="Server max retries (default: 10)"
    )

    parser.add_argument(
        "--timeout",
        type=int,
        default=120,
        help="Server timeout in seconds (default: None)",
    )
    parser.add_argument("--num_threads", type=int, default=20, help="Number of threads")
    parser.add_argument(
        "--first_n", type=int_or_float, default=None,
        help="Use only first n examples. If a float is provided, it will be interpreted as a percentage of the total number of examples."
    )
    parser.add_argument(
        "--cache_dir", type=str, default="cache", help="Repsonses cache dir"
    )
    parser.add_argument(
        "--num_repeats",
        type=int,
        default=1,
        help="Number of repeats for each sample, available only for math, humaneval and gpqa",
    )
    parser.add_argument("--debug", action="store_true", help="Run in debug mode.")
    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Random seed for reproducibility (default: 42)",
    )
    parser.add_argument(
        "--downsampling_ratio",
        type=float,
        default=None,
        help="Ratio of examples to use from the dataset (between 0 and 1)",
    )
    parser.add_argument(
        "--add_system_prompt",
        action="store_true",
        help="Add system prompt for the model",
    )

    parser.add_argument(
        "--judge_url",
        type=str,
        default=None,
        help="URL for the judge API. Default: None",
    )

    parser.add_argument(
        "--judge_model_id",
        type=str,
        default=None,
        help="Model ID for the judge API. Default: None",
    )

    parser.add_argument(
        "--judge_api_key_name",
        type=str,
        default=None,
        help="Name of the env variable that stores API key for the judge API. Default: None",
    )

    parser.add_argument(
        "--judge_request_timeout",
        type=int,
        default=60,
        help="Request timeout for the judge API. Default: 60",
    )

    parser.add_argument(
        "--judge_max_retries",
        type=int,
        default=16,
        help="Max retries for the judge API. Default: 16",
    )

    parser.add_argument(
        "--judge_temperature",
        type=float,
        default=0.0,
        help="Temperature for the judge API. Default: 0.0",
    )

    parser.add_argument(
        "--judge_top_p",
        type=float,
        default=0.0001,
        help="Top-p for the judge API. Default: 0.0001",
    )
    
    parser.add_argument(
        "--judge_max_tokens",
        type=int,
        default=1024,
        help="Max tokens for the judge API. Default: 1024",
    )
    
    parser.add_argument(
        "--judge_max_concurrent_requests",
        type=int,
        default=None,
        help=(
        "Max concurrent requests for the judge API (only used with generic backend). "
        "Default: None (inherits from num_threads). "
        "Note: The upper limit is num_threads; if you set this higher than num_threads, "
        "the actual concurrency will be capped at num_threads."
    ),
    )
    
    parser.add_argument(
        "--judge_backend",
        type=str,
        default="openai",
        choices=["openai", "generic"],
        help="Backend for the judge API. Default: openai",
    )
    
    parser.add_argument(
        "--custom_eval_cfg_file",
        type=str,
        default=None,
        help="Path to custom evaluation configuration file (YAML format)",
    )
    
    args = parser.parse_args()
    
    # Initialize the seed generator
    seed_generator = SeedGenerator(base_seed=args.seed)
    
    random.seed(args.seed)
    np.random.seed(args.seed)
    
    # Load evaluation configuration if provided
    eval_config = None
    if args.custom_eval_cfg_file:
        eval_config = EvalConfig.from_file(args.custom_eval_cfg_file)

    common_eval_args = {
        "num_threads": args.num_threads,
        "cache_dir": args.cache_dir,
        "first_n": args.first_n,
        "seed_generator": seed_generator,  # Pass the seed generator instance
        "custom_eval_config": eval_config,  # Pass the EvalConfig instance
    }
    
    sampler = ChatCompletionSampler(
        model=args.model,
        system_message=OPENAI_SYSTEM_MESSAGE_API if args.add_system_prompt else None,
        url=args.url,
        temperature=args.temperature,
        top_p=args.top_p,
        max_tokens=args.max_tokens,
        timeout=args.timeout,
        max_retries=args.max_retries,
        api_key="API_KEY",
    )

    def get_judge_config():
        judge_config = {
            # Parameters that are None by default
            "url": args.judge_url,
            "model": args.judge_model_id,
            "api_key": args.judge_api_key_name, # name of the environment variable
            # Parameters that have default values
            "backend": args.judge_backend,
            "timeout": args.judge_request_timeout,
            "max_retries": args.judge_max_retries,
            "temperature": args.judge_temperature,
            "top_p": args.judge_top_p,
            "max_tokens": args.judge_max_tokens,
        }
        if args.judge_backend == "generic":
            judge_config["max_concurrent_requests"] = args.judge_max_concurrent_requests
        return judge_config

    def get_grader_config(default_model_alias="gpt4"):
        # Get grader configuration from config or use defaults
        grader_config = common_eval_args.get("grader_config")
        if grader_config is None and args.judge_model_id is None:
            grader_config = common.load_default_config(default_model_alias)
            grader_config["api_key"] = args.judge_api_key_name
        elif grader_config and args.judge_api_key_name:
            grader_config["api_key"] = args.judge_api_key_name
        elif args.judge_model_id is not None:
            grader_config = get_judge_config()
        return grader_config

    def get_eval(eval_name):
        # Use eval_name from config if provided
        if eval_config and eval_config.eval_name:
            eval_name = eval_config.eval_name
        
        if eval_name == "mmlu_pro":
            return MMLUProEval(
                downsampling_ratio=args.downsampling_ratio,
                **common_eval_args,
            )
        if eval_name.startswith("mmlu"):
            # Get language from config or derive from eval_name
            language = common_eval_args.get("language", "en")
            if eval_name != "mmlu" and language == "en":
                language = eval_name.split("_")[1]
            
            return MMLUEval(
                language=language,
                downsampling_ratio=args.downsampling_ratio,
                **common_eval_args,
            )
        if eval_name.startswith("gpqa"):
            return GPQAEval(
                n_repeats=args.num_repeats,
                variant=eval_name.split("_")[1],
                is_nemo=eval_name.endswith("_nemo"),
                **common_eval_args,
            )
        if eval_name in [
            "math_test_500", "AIME_2024", "AA_math_test_500", "AA_AIME_2024", "AIME_2025",
            "math_test_500_nemo", "aime_2024_nemo", "aime_2025_nemo"
        ]:
            # Get judge configuration from config or use defaults
            judge_config = common_eval_args.get("judge_config")
            if judge_config is None and args.judge_model_id is None:
                # Fall back to hardcoded defaults
                eval_name_to_judge = {
                    "AA_math_test_500": "llama70b",
                    "AA_AIME_2024": "llama70b",
                    "AIME_2025": "llama70b",
                    "math_test_500": "gpt4",
                    "AIME_2024": "gpt4",
                    "math_test_500_nemo": None,  # use sympy only
                    "aime_2024_nemo": None,  # use sympy only
                    "aime_2025_nemo": None,  # use sympy only
                }
                model_alias = eval_name_to_judge[eval_name]
                judge_config = common.load_default_config(model_alias) if model_alias is not None else None
                if judge_config is not None:
                    judge_config["api_key"] = args.judge_api_key_name
            elif judge_config and args.judge_api_key_name:
                judge_config["api_key"] = args.judge_api_key_name
            elif args.judge_model_id is not None:
                judge_config = get_judge_config()
            
            equality_checker = common.load_judge(judge_config) if judge_config is not None else None
            return MathEval(
                equality_checker=equality_checker,
                eval_name=eval_name,
                n_repeats=args.num_repeats,
                **common_eval_args,
            )
        match eval_name:
            case "mgsm":
                # Get num_examples_per_lang from config or use default
                num_examples_per_lang = common_eval_args.get("num_examples_per_lang", 250)
                
                return MGSMEval(
                    num_examples_per_lang=num_examples_per_lang,
                    **common_eval_args,
                )
            case "humaneval" | "humanevalplus":
                return HumanEval(
                    eval_name=eval_name,
                    num_samples_per_task=args.num_repeats,
                    **common_eval_args
                )
            case "simpleqa":
                return SimpleQAEval(
                    n_repeats=args.num_repeats, 
                    grader_config=get_grader_config(),
                    **common_eval_args
                )
            case "browsecomp":
                return BrowseCompEval(
                    grader_config=get_grader_config(default_model_alias="llama70b"),
                    **common_eval_args,
                )
            case "healthbench" | "healthbench_hard" | "healthbench_consensus":
                subset_name = None
                if eval_name == "healthbench_hard":
                    subset_name = "hard"
                elif eval_name == "healthbench_consensus":
                    subset_name = "consensus"
                return HealthBenchEval(
                    grader_config=get_grader_config(default_model_alias="llama70b"),
                    subset_name=subset_name,
                    **common_eval_args,
                )
            case _:
                raise Exception(f"Unrecognized eval type: {eval_name}")

    # Create the evaluation object
    eval_obj = get_eval(args.eval_name)

    # Run the evaluation
    result = await eval_obj(sampler)
    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
    else:
        logging.getLogger().setLevel(logging.INFO)
    # Prepare file names
    debug_suffix = "_DEBUG" if args.debug else ""
    file_stem = f"{args.eval_name}"
    # Ensure output directory exists
    out_dir = Path(args.out_dir)
    os.makedirs(out_dir, exist_ok=True)  # Create the directory if it doesn't exist

    # Define file paths
    report_filename = out_dir / f"{file_stem}{debug_suffix}.html"
    result_filename = out_dir / f"{file_stem}{debug_suffix}.json"

    print(f"Writing report to {report_filename}")
    with open(report_filename, "w") as fh:
        fh.write(common.make_report(result))

    # Save metrics
    metrics = result.metrics | {"score": result.score} | {"task_name": result.task_name}
    print(metrics)
    print(f"Writing results to {result_filename}")
    with open(result_filename, "w") as f:
        f.write(json.dumps(metrics, indent=2))


def main():
    asyncio.run(run())


if __name__ == "__main__":
    main()
