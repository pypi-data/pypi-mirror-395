"""
Measuring Mathematical Problem Solving With the MATH Dataset
Dan Hendrycks, Collin Burns, Saurav Kadavath, Akul Arora, Steven Basart, Eric Tang, Dawn Song, Jacob Steinhardt
https://arxiv.org/abs/2103.03874
"""

import random
import re
from typing import Literal, Optional, Any

import simple_evals.common as common
from simple_evals.common import HTML_JINJA, check_equality
from simple_evals.evals.math_grading.nemo_grader import extract_answer as extract_nemo_answer
from simple_evals.simple_evals_types import Eval, EvalResult, SamplerBase, SingleEvalResult, SeedGenerator
from datasets import load_dataset
import pandas as pd
from simple_evals.seed_generator import SeedGenerator



QUERY_TEMPLATE = """
Solve the following math problem step by step. The last line of your response should be of the form Answer: $ANSWER (without quotes) where $ANSWER is the answer to the problem.

{Question}

Remember to put your answer on its own line after "Answer:", and you do not need to use a \\boxed command.
""".strip()


class MathEval(Eval):
    def __init__(
        self,
        equality_checker, # judge model: OpenAIJudge or ChatCompletionSampler
        eval_name: Literal["math_test_500", "AIME_2024",  "AIME_2025", "AA_AIME_2024", "AA_math_test_500", "math_test_500_nemo", "aime_2024_nemo", "aime_2025_nemo"] = "math_test_500",
        num_examples: int | None = None,
        n_repeats: int = 16,
        num_threads: int = 50,
        first_n: int | float | None = None,
        cache_dir: str = "cache",
        seed_generator: SeedGenerator | None = None,
        custom_eval_config: Optional[any] = None,
    ):
        super().__init__(seed_generator=seed_generator, custom_eval_config=custom_eval_config)
        
        if eval_name in ["math_test_500", "AA_math_test_500",  "math_test_500_nemo"]:
            df = load_dataset("HuggingFaceH4/MATH-500")["test"].to_pandas()
            df = df.rename(columns={"problem": "Question", "answer": "Answer"})
        elif eval_name in ["AIME_2024", "AA_AIME_2024", "aime_2024_nemo"]:
            df = load_dataset("AI-MO/aimo-validation-aime")["train"].to_pandas()
            df = df[df["url"].str.extract(r'/(\d{4})_AIME')[0] == "2024"]
            if len(df) == 0:
                raise ValueError("No AIME 2024 problems found in the dataset.")
            df = df.rename(columns={"problem": "Question", "answer": "Answer"})
        elif eval_name in ["AIME_2025", "aime_2025_nemo"]:
            df = pd.concat([
                load_dataset("opencompass/AIME2025", name="AIME2025-I", split="test").to_pandas(),
                load_dataset("opencompass/AIME2025", name="AIME2025-II", split="test").to_pandas()
            ])
            df = df.rename(columns={"question": "Question", "answer": "Answer"})
        else:
            raise ValueError(f"Invalid eval_name: '{eval_name}' provided. Valid options are 'math_test_500', 'AIME_2024', or 'AIME_25'.")

        examples = [row.to_dict() for _, row in df.iterrows()]
        if num_examples:
            assert n_repeats == 1, "n_repeats only supported for num_examples = None"
            rng = random.Random(self.seed_generator.get_seed(0))
            examples = rng.sample(examples, num_examples)
        self.examples = examples * n_repeats
        self.equality_checker = equality_checker
        self.num_threads = num_threads
        self.first_n = first_n
        self.cache_dir = cache_dir
        self.eval_name = eval_name

        # Load configuration based on eval_name
        config = common.load_task_config(eval_name)
        if config is not None:
            # Use config-based template and regex
            self.query_template = common.load_template(config["template_file"]).strip()
            regex_file = config.get("regex_file", None)
            # NOTE(dfridman): if regex_file is not provided, must use nemo_extractor
            self.answer_pattern = common.load_regex(regex_file) if regex_file is not None else None
            self.use_sympy_first = config.get("use_sympy_first", False)
            self.nemo_extractor = config.get("nemo_extractor", False)
        else:
            # Use existing constants
            self.query_template = QUERY_TEMPLATE
            self.answer_pattern = common.ANSWER_PATTERN
            self.use_sympy_first = False
            self.nemo_extractor = False

    async def __call__(self, sampler: SamplerBase) -> EvalResult:
        async def fn(row: dict, index: int):
            # Use custom prompt template if provided, otherwise use default
            if self.custom_eval_config and self.custom_eval_config.prompt_template:
                prompt_content = self.custom_eval_config.format_prompt(**row)
            else:
                prompt_content = self.query_template.format(**row)
            
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
                if self.nemo_extractor:
                    extracted_answer = extract_nemo_answer(response_text)
                else:
                    # Use regex pattern
                    match = re.search(self.answer_pattern, response_text)
                    extracted_answer = match.group(1) if match else ""
            
            # Use custom scorer if provided, otherwise use default
            if self.custom_eval_config and self.custom_eval_config.scorer:
                score = self.custom_eval_config.score_answer(extracted_answer, row["Answer"])
            else:
                # Use default scoring logic
                if self.equality_checker is not None:
                    score = await check_equality(self.equality_checker, row["Answer"], extracted_answer, use_sympy=self.use_sympy_first)
                else:
                    # Fall back to simple string comparison
                    score = 1.0 if extracted_answer == row["Answer"] else 0.0
            
            html = common.jinja_env.from_string(HTML_JINJA).render(
                prompt_messages=prompt_messages,
                next_message=dict(content=response_text, role="assistant"),
                score=score,
                correct_answer=row["Answer"],
                extracted_answer=extracted_answer,
            )
            convo = prompt_messages + [dict(content=response_text, role="assistant")]
            return SingleEvalResult(
                html=html,
                score=score,
                convo=convo,
            )

        results = await common.map_with_progress(
            fn,
            self.examples,
            num_threads=self.num_threads,
            cache_dir=self.cache_dir,
            first_n=self.first_n
        )
        return common.aggregate_results(results, task_name=self.eval_name)
