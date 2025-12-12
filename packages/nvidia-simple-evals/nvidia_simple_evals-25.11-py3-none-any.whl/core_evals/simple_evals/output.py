import json
import pathlib
import re
import yaml

from nemo_evaluator.api.api_dataclasses import EvaluationResult, MetricResult, Score, TaskResult


# This is the only required function
def parse_output(output_dir: str) -> EvaluationResult:
    # Extract eval_type name from the run_config.yml file
    output_path = pathlib.Path(output_dir)
    
    # Read run_config.yml to get eval_type
    run_config_file = output_path / "run_config.yml"
    with open(run_config_file) as fp:
        run_config = yaml.safe_load(fp)
    eval_type = run_config.get("config", {}).get("type")
    
    if not eval_type:
        raise ValueError(f"Could not find eval_type in run_config.yml in {output_dir}")
    
    # Look for JSON files in the eval_type subdirectory
    eval_type_dir = output_path / eval_type
    result_files = list(eval_type_dir.glob("*.json"))
    if not result_files:
        raise FileNotFoundError(f"Failed to find `{eval_type}.json` with metric in {eval_type_dir}.")
    if len(result_files) > 1:
        raise ValueError(
            f"More than 1 `{eval_type}.json` files found in {eval_type_dir}. `output_dir` must contain a single evaluation."
        )

    with open(result_files[0]) as fp:
        results = json.load(fp)

    task_name = results.pop("task_name")

    group_metric_names = ["score"]
    if "score_macro" in results:
        group_metric_names.append("score_macro")
    scores = {}
    for metric_name in group_metric_names:
        stats = {}
        full_stat_names = [k for k in results.keys() if k.startswith(f"{metric_name}:")]
        for full_stat_name in full_stat_names:
            if full_stat_name in results:
                m = re.match(".*:(.*)", full_stat_name)
                stat_name = m.group(1)
                if stat_name == "std":
                    stat_name = "stddev"
                stats[stat_name] = results.pop(full_stat_name)
        metric_type = "macro" if "macro" in metric_name == "score_macro" else "micro"
        scores[metric_type] = Score(
            value=results.pop(metric_name),
            stats=stats,
        )
    group_result = dict(
        metrics={
            "score": MetricResult(scores=scores)
        }
    )
    groups = {task_name: group_result}

    tasks = {}
    task_names = [key for key in results.keys() if ":" not in key]
    for task_name in task_names:
        full_stat_names = [k for k in results.keys() if k.startswith(f"{task_name}:")]
        stats = {}
        for full_stat_name in full_stat_names:
            m = re.match(".*:(.*)", full_stat_name)
            stat_name = m.group(1)
            stats[stat_name] = results.pop(full_stat_name)
        tasks[task_name] = TaskResult(
            metrics={
                "score": MetricResult(
                    scores={
                        "micro": Score(
                            value=results.pop(task_name),
                            stats=stats,
                        )
                    }
                )
            }
        )
    if not tasks:
        tasks = groups
    return EvaluationResult(groups=groups, tasks=tasks)
