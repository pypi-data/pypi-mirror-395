"""
HumanEval: Evaluating Large Language Models Trained on Code
Mark Chen and Jerry Tworek and Heewoo Jun and Qiming Yuan and Henrique Ponde de Oliveira Pinto and Jared Kaplan and Harri Edwards and Yuri Burda and Nicholas Joseph and Greg Brockman and Alex Ray and Raul Puri and Gretchen Krueger and Michael Petrov and Heidy Khlaaf and Girish Sastry and Pamela Mishkin and Brooke Chan and Scott Gray and Nick Ryder and Mikhail Pavlov and Alethea Power and Lukasz Kaiser and Mohammad Bavarian and Clemens Winter and Philippe Tillet and Felipe Petroski Such and Dave Cummings and Matthias Plappert and Fotios Chantzis and Elizabeth Barnes and Ariel Herbert-Voss and William Hebgen Guss and Alex Nichol and Alex Paino and Nikolas Tezak and Jie Tang and Igor Babuschkin and Suchir Balaji and Shantanu Jain and William Saunders and Christopher Hesse and Andrew N. Carr and Jan Leike and Josh Achiam and Vedant Misra and Evan Morikawa and Alec Radford and Matthew Knight and Miles Brundage and Mira Murati and Katie Mayer and Peter Welinder and Bob McGrew and Dario Amodei and Sam McCandlish and Ilya Sutskever and Wojciech Zaremba 
https://arxiv.org/abs/2107.03374 https://github.com/openai/human-eval/ 
"""

import random
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Literal, Optional
from datasets import load_dataset
from simple_evals.evals.human_eval.evaluation import estimate_pass_at_k
from simple_evals.evals.human_eval.execution import check_correctness  # , unsafe_execute

import simple_evals.common as common
from simple_evals.common import HTML_JINJA
from simple_evals.simple_evals_types import (
    Eval,
    EvalResult,
    SamplerBase,
    SingleEvalResult,
    SeedGenerator,
)


def evaluate_functional_correctness(
    sample: dict[str, str],
    completions: list[str],
    n_workers: int = 4,
    timeout: float = 3.0,
):
    """
    Evaluates the functional correctness of generated samples, and writes
    results to f"{sample_file}_results.jsonl.gz"
    """
    import copy

    # Check the generated samples against test suites.
    with ThreadPoolExecutor(max_workers=n_workers) as executor:
        futures = []
        for i, completion in enumerate(completions):
            args = (sample, completion, timeout, i)
            future = executor.submit(check_correctness, *args)
            futures.append(future)
        results = []
        for future in as_completed(futures):
            result = future.result()
            results.append(result)
    passed = [int(r["passed"]) for r in results]
    return passed


class HumanEval(Eval):
    def __init__(
        self,
        eval_name: Literal["humaneval", "humanevalplus"] = "humaneval",
        num_examples: (
            int | None
        ) = None,  # restrict to a subset of the data for debugging
        num_samples_per_task: int = 5,
        ks_passes: list[int] = [1, 2, 5],
        timeout: int = 120,
        num_threads: int = 3,
        first_n: int | float | None = None,
        cache_dir: str = "cache",
        seed_generator: SeedGenerator | None = None,
        custom_eval_config: Optional[any] = None,
    ):
        super().__init__(seed_generator=seed_generator, custom_eval_config=custom_eval_config)
        
        # Assert that custom scorers are not supported for HumanEval
        if custom_eval_config and custom_eval_config.scorer:
            raise ValueError("Custom scorers are not supported for HumanEval. Use default functional correctness evaluation.")
        
        self.eval_name = eval_name
        dataset_tag = {
            "humaneval": "openai/openai_humaneval",
            "humanevalplus": "evalplus/humanevalplus",
        }
        self.examples = load_dataset(dataset_tag[eval_name])["test"]
        self.examples = [dict(example) for example in self.examples]

        if num_examples:
            # Use seed_generator for consistent sampling
            base_seed = self.seed_generator.get_seed(0)  # Use index 0 for initial sampling
            rng = random.Random(base_seed)
            self.examples = rng.sample(self.examples, num_examples)
            
        self._num_samples_per_task = num_samples_per_task
        self._ks_passes = ks_passes
        self._timeout = timeout
        self.num_threads = num_threads
        self.first_n = first_n
        self.cache_dir = cache_dir

    async def __call__(self, sampler: SamplerBase) -> EvalResult:
        # Use custom prompt template if provided, otherwise use default

        instruction = "Read the following function signature and docstring, and fully implement the function described. Your response should only contain the code for this function.\n"

        def find_code(completion):
            # Use custom extractor if provided, otherwise use default
            if self.custom_eval_config and self.custom_eval_config.extractor:
                return self.custom_eval_config.extract_answer(completion)
            else:
                # Use default extraction logic
                pattern = re.compile(r"(?<=```python\n)((?:\n|.)+?)(?=\n```)", re.DOTALL)
                matches = pattern.findall(completion)
                extracted_answer = matches[0] if len(matches) >= 1 else completion
                extracted_answer = extracted_answer[
                    extracted_answer.find(":\n    ") + 2 :
                ]  # remove signature
                return extracted_answer

        async def fn(sample: dict[str, str], index: int):
            if self.custom_eval_config and self.custom_eval_config.prompt_template:
                prompt = self.custom_eval_config.format_prompt(instruction=instruction, prompt=sample["prompt"])
            else:
                prompt = instruction + sample["prompt"]
            prompt_messages = [
                sampler._pack_message(content=prompt, role="user")
            ]
            completions = []
            for i in range(self._num_samples_per_task):
                completion_seed = self.seed_generator.get_seed(index, i)  # Use sub_index for multiple samples
                completions.append(find_code(await sampler(prompt_messages, seed=completion_seed)))
                
            results = evaluate_functional_correctness(
                sample, completions, timeout=self._timeout
            )
            total = len(results)
            correct = sum(results)
            score = sum(results) / len(results)
            html = common.jinja_env.from_string(HTML_JINJA).render(
                prompt_messages=prompt_messages,
                next_message=dict(content=completions[0], role="assistant"),
                score=score,
                correct_answer=[1] * len(results),
                extracted_answer=results,
            )
            convo = prompt_messages + [
                dict(content=completion, role="assistant") for completion in completions
            ]
            return SingleEvalResult(
                html=html,
                score=score,
                convo=convo,
                metrics={
                    f"pass@{k}": estimate_pass_at_k([total], [correct], k).tolist()[0]
                    # this will be aggrated so no need of .mean()
                    for k in self._ks_passes
                    if total >= k
                },
            )

        results = await common.map_with_progress(
            fn,
            self.examples,
            num_threads=self.num_threads,
            cache_dir=self.cache_dir,
            first_n=self.first_n,
        )
        return common.aggregate_results(results, task_name=self.eval_name)
