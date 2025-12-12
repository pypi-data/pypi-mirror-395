"""
Measuring Massive Multitask Language Understanding
Dan Hendrycks, Collin Burns, Steven Basart, Andy Zou, Mantas Mazeika, Dawn Song, Jacob Steinhardt
https://arxiv.org/abs/2009.03300
"""

import random
import re
from typing import Optional

import pandas as pd
from datasets import load_dataset
import simple_evals.common as common
from simple_evals.common import (
    HTML_JINJA,
    MULTILINGUAL_ANSWER_PATTERN_TEMPLATE,
    MULTILINGUAL_ANSWER_REGEXES,
    format_multichoice_question,
    normalize_extracted_answer,
    normalize_response,
)
from simple_evals.simple_evals_types import Eval, EvalResult, SamplerBase, SingleEvalResult, SeedGenerator

subject2category = {
    "abstract_algebra": "stem",
    "anatomy": "other",
    "astronomy": "stem",
    "business_ethics": "other",
    "clinical_knowledge": "other",
    "college_biology": "stem",
    "college_chemistry": "stem",
    "college_computer_science": "stem",
    "college_mathematics": "stem",
    "college_medicine": "other",
    "college_physics": "stem",
    "computer_security": "stem",
    "conceptual_physics": "stem",
    "econometrics": "social_sciences",
    "electrical_engineering": "stem",
    "elementary_mathematics": "stem",
    "formal_logic": "humanities",
    "global_facts": "other",
    "high_school_biology": "stem",
    "high_school_chemistry": "stem",
    "high_school_computer_science": "stem",
    "high_school_european_history": "humanities",
    "high_school_geography": "social_sciences",
    "high_school_government_and_politics": "social_sciences",
    "high_school_macroeconomics": "social_sciences",
    "high_school_mathematics": "stem",
    "high_school_microeconomics": "social_sciences",
    "high_school_physics": "stem",
    "high_school_psychology": "social_sciences",
    "high_school_statistics": "stem",
    "high_school_us_history": "humanities",
    "high_school_world_history": "humanities",
    "human_aging": "other",
    "human_sexuality": "social_sciences",
    "international_law": "humanities",
    "jurisprudence": "humanities",
    "logical_fallacies": "humanities",
    "machine_learning": "stem",
    "management": "other",
    "marketing": "other",
    "medical_genetics": "other",
    "miscellaneous": "other",
    "moral_disputes": "humanities",
    "moral_scenarios": "humanities",
    "nutrition": "other",
    "philosophy": "humanities",
    "prehistory": "humanities",
    "professional_accounting": "other",
    "professional_law": "humanities",
    "professional_medicine": "other",
    "professional_psychology": "social_sciences",
    "public_relations": "social_sciences",
    "security_studies": "social_sciences",
    "sociology": "social_sciences",
    "us_foreign_policy": "social_sciences",
    "virology": "other",
    "world_religions": "humanities",
}


class MMLUEval(Eval):
    def __init__(
        self, 
        num_examples: int | None = None, 
        language: str = "EN-US", 
        num_threads: int = 10, 
        first_n: int | float | None = None,
        cache_dir: str = "cache",
        seed_generator: SeedGenerator | None = None,
        downsampling_ratio: float | None = None,
        custom_eval_config: Optional[any] = None
    ):
        super().__init__(seed_generator=seed_generator, custom_eval_config=custom_eval_config)
        
        # Validate parameters
        if num_examples is not None and downsampling_ratio is not None:
            raise ValueError("Cannot specify both num_examples and downsampling_ratio")
        if downsampling_ratio is not None and not 0 < downsampling_ratio <= 1:
            raise ValueError("downsampling_ratio must be between 0 and 1")
        
        if language != "en":
            if language.endswith("-lite"):
                df = load_dataset("CohereLabs/Global-MMLU-Lite", language.replace("-lite", ""), split="test").to_pandas()
                # Add missing subject and subject_category columns for the `mmlu_my-lite` dataset
                if language.startswith("my") and "subject" not in df.columns:
                    df["subject"] = "other"
                    df["subject_category"] = "other"
            else:
                df = load_dataset("CohereLabs/Global-MMLU", language, split="test").to_pandas()
            # Remap columns to standard names (non-English only, no capitalize)
            column_map = {
                'sample_id': 'Sample_id',
                'subject': 'Subject',
                'subject_category': 'Subject_category',
                'question': 'Question',
                'option_a': 'A',
                'option_b': 'B',
                'option_c': 'C',
                'option_d': 'D',
                'answer': 'Answer',
            }
            # Only rename columns that exist in the DataFrame
            df = df.rename(columns={k: v for k, v in column_map.items() if k in df.columns})
        else:
            df = pd.concat([load_dataset("cais/mmlu", category, split="test").to_pandas() for category in subject2category.keys()], ignore_index=True)
            df.columns = df.columns.str.capitalize()
            choices = ['A', 'B', 'C', 'D']
            df[choices] = pd.DataFrame(df['Choices'].tolist(), index=df.index)
            df["Answer"] = df['Answer'].map(lambda x: choices[x])
        
        # If downsampling_ratio is provided, calculate num_examples
        if downsampling_ratio is not None:
            num_examples = int(len(df) * downsampling_ratio)
            
        examples = [row.to_dict() for _, row in df.iterrows()]
        if num_examples:
            # Use seed_generator for consistent sampling
            base_seed = self.seed_generator.get_seed(0)
            rng = random.Random(base_seed)
            examples = rng.sample(examples, num_examples)
            
        self.examples = examples
        self.num_threads = num_threads
        self.first_n = first_n
        self.cache_dir = cache_dir
        self.language = language

    async def __call__(self, sampler: SamplerBase) -> EvalResult:
        async def fn(row: dict, index: int):
            # Use custom prompt template if provided, otherwise use default
            if self.custom_eval_config and self.custom_eval_config.prompt_template:
                prompt_content = self.custom_eval_config.format_prompt(**row)
            else:
                prompt_content = format_multichoice_question(row)
            
            prompt_messages = [
                sampler._pack_message(content=prompt_content, role="user")
            ]
            completion_seed = self.seed_generator.get_seed(index)
            response_text = normalize_response(await sampler(prompt_messages, seed=completion_seed))
            
            # Use custom extractor if provided, otherwise use default
            if self.custom_eval_config and self.custom_eval_config.extractor:
                extracted_answer = self.custom_eval_config.extract_answer(response_text)
            else:
                # Use default extraction logic
                extracted_answer = None
                for answer_regex in MULTILINGUAL_ANSWER_REGEXES:
                    regex = MULTILINGUAL_ANSWER_PATTERN_TEMPLATE.format(answer_regex)
                    match = re.search(regex, response_text)
                    if match:
                        extracted_answer = normalize_extracted_answer(match.group(1))
                        break
            
            # Use custom scorer if provided, otherwise use default
            if self.custom_eval_config and self.custom_eval_config.scorer:
                score = self.custom_eval_config.score_answer(extracted_answer, row["Answer"])
            else:
                score = 1.0 if extracted_answer == row["Answer"] else 0.0
            
            html = common.jinja_env.from_string(HTML_JINJA).render(
                prompt_messages=prompt_messages,
                next_message=dict(content=response_text, role="assistant"),
                score=score,
                correct_answer=row["Answer"],
                extracted_answer=extracted_answer,
            )
            convo = prompt_messages + [dict(content=response_text, role="assistant")]
            category = subject2category.get(row["Subject"], "other")
            return SingleEvalResult(
                html=html, score=score, metrics={category: score}, convo=convo
            )

        results = await common.map_with_progress(
            fn, 
            self.examples, 
            num_threads=self.num_threads, 
            cache_dir=self.cache_dir, 
            first_n=self.first_n
        )
        task_name = "mmlu" if self.language == "en" else f"mmlu_{self.language}"
        return common.aggregate_results(results, add_macro=True, task_name=task_name)
