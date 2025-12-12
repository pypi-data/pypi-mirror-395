"""
GPQA: A Graduate-Level Google-Proof Q&A Benchmark
David Rein, Betty Li Hou, Asa Cooper Stickland, Jackson Petty, Richard Yuanzhe Pang, Julien Dirani, Julian Michael, Samuel R. Bowman
https://arxiv.org/abs/2311.12022
"""

import random
import re
from typing import Optional, Any

import blobfile as bf
import pandas

from datasets import load_dataset

import simple_evals.common as common
from simple_evals.common import ANSWER_PATTERN_MULTICHOICE, HTML_JINJA, QUERY_TEMPLATE_MULTICHOICE
from simple_evals.evals.math_grading.nemo_grader import extract_answer as extract_nemo_answer
from simple_evals.simple_evals_types import Eval, EvalResult, MessageList, SamplerBase, SingleEvalResult
from simple_evals.seed_generator import SeedGenerator


NEMO_QUERY_TEMPLATE_MULTICHOICE = """
What is the correct answer to this question: {Question}
Choices:
A. {A}
B. {B}
C. {C}
D. {D}
Let's think step by step, and put the final answer (should be a single letter A, B, C, or D) into a \\boxed{{}}
""".strip()


class GPQAEval(Eval):
    def __init__(
        self,
        n_repeats: int = 4,
        variant: str = "diamond",
        num_examples: int | None = None,  # restrict to a subset of the data for debugging
        num_threads: int = 10,
        first_n: int | float | None = None,
        cache_dir: str = "cache",
        seed_generator: SeedGenerator | None = None,
        is_nemo: bool = False,
        custom_eval_config: Optional[Any] = None,
    ):
        super().__init__(seed_generator=seed_generator, custom_eval_config=custom_eval_config)
        
        df = load_dataset("Idavidrein/gpqa", f"gpqa_{variant}")["train"].to_pandas()

        examples = [row.to_dict() for _, row in df.iterrows()]
        rng = random.Random(0)
        if num_examples:
            assert n_repeats == 1, "n_repeats only supported for num_examples = None"
            examples = rng.sample(examples, num_examples)
        examples = examples * n_repeats
        examples = [example | {"permutation": rng.sample(range(4), 4)} for example in examples]
        self.examples = examples
        self.n_repeats = n_repeats
        self.num_threads = num_threads
        self.first_n = first_n
        self.cache_dir = cache_dir
        self.variant = variant
        self.is_nemo = is_nemo
        self.query_template = NEMO_QUERY_TEMPLATE_MULTICHOICE if is_nemo else QUERY_TEMPLATE_MULTICHOICE

    async def __call__(self, sampler: SamplerBase) -> EvalResult:
        async def fn(row: dict, index: int):
            choices = [
                row["Correct Answer"],
                row["Incorrect Answer 1"],
                row["Incorrect Answer 2"],
                row["Incorrect Answer 3"],
            ]
            choices = [choices[i] for i in row["permutation"]]
            correct_index = choices.index(row["Correct Answer"])
            correct_answer = "ABCD"[correct_index]
            choices_dict = dict(
                A=choices[0], B=choices[1], C=choices[2], D=choices[3], Question=row["Question"]
            )
            
            # Use custom prompt template if provided, otherwise use default
            if self.custom_eval_config and self.custom_eval_config.prompt_template:
                prompt_content = self.custom_eval_config.format_prompt(**choices_dict)
            else:
                prompt_content = self.query_template.format(**choices_dict)
            
            prompt_messages = [
                sampler._pack_message(content=prompt_content, role="user")
            ]
            completion_seed = self.seed_generator.get_seed(index)
            response_text = await sampler(prompt_messages, seed=completion_seed)
            
            # Use custom extractor if provided, otherwise use default
            if self.custom_eval_config and self.custom_eval_config.extractor:
                extracted_answer = self.custom_eval_config.extract_answer(response_text)
            else:
                # Use default extraction logic
                if self.is_nemo:
                    extracted_answer = extract_nemo_answer(response_text)
                else:
                    match = re.search(ANSWER_PATTERN_MULTICHOICE, response_text)
                    extracted_answer = match.group(1) if match else None
            
            # Use custom scorer if provided, otherwise use default
            if self.custom_eval_config and self.custom_eval_config.scorer:
                score = self.custom_eval_config.score_answer(extracted_answer, correct_answer)
            else:
                # Use default scoring logic
                score = 1.0 if extracted_answer == correct_answer else 0.0
            
            html = common.jinja_env.from_string(HTML_JINJA).render(
                prompt_messages=prompt_messages,
                next_message=dict(content=response_text, role="assistant"),
                score=score,
                correct_answer=correct_answer,
                extracted_answer=extracted_answer,
            )
            convo = prompt_messages + [dict(content=response_text, role="assistant")]
            # metrics = {"chars": len(response_text)}
            # NOTE(dfridman): the above metric (number of generated characters) is not required
            # and complicates parsing the output
            metrics = {}
            return SingleEvalResult(
                html=html, score=score, convo=convo, metrics=metrics
            )

        results = await common.map_with_progress(
            fn,
            self.examples,
            num_threads=self.num_threads,
            cache_dir=self.cache_dir,
            first_n=self.first_n
        )
        task_name = f"gpqa_{self.variant}"
        if self.is_nemo:
            task_name += "_nemo"
        return common.aggregate_results(results, task_name=task_name)
