"""
Configuration loader for evaluation configurations.
"""

import yaml
from pathlib import Path
from jinja2 import Template

from .extractors import create_extractor
from .scorers import create_scorer


class EvalConfig:
    """Configuration for an evaluation task."""
    
    def __init__(
        self,
        extraction: list[dict] | str | dict[str, any] | None = None,
        scoring: str | dict[str, any] | None = None,
        prompt_template: str | None = None,
        eval_name: str | None = None,
        **kwargs
    ):
        """
        Initialize evaluation configuration.
        
        Args:
            extraction: Extraction configuration (regex patterns, module path, dict config, or None)
            scoring: Scoring configuration (module path, dict config, or None)
            prompt_template: Jinja2 template for prompts
            eval_name: Name of the evaluation (for compatibility)
            **kwargs: Additional configuration parameters
        """
        self.extraction = extraction
        self.scoring = scoring
        self.prompt_template = prompt_template
        self.eval_name = eval_name
        self.extra_config = kwargs
        
        # Create extractor and scorer instances using factory pattern
        self.extractor = create_extractor(extraction)
        self.scorer = create_scorer(scoring)
        
        # Compile template if provided
        self.template = None
        if prompt_template:
            self.template = Template(prompt_template)
    
    @classmethod
    def from_file(cls, config_path: str | Path) -> "EvalConfig":
        """
        Create EvalConfig instance from YAML file.
        
        Args:
            config_path: Path to YAML configuration file
            
        Returns:
            EvalConfig instance
        """
        config_path = Path(config_path)
        
        if not config_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {config_path}")
        
        with open(config_path, 'r', encoding='utf-8') as f:
            config_data = yaml.safe_load(f)
        
        return cls(**config_data)
    
    def format_prompt(self, **kwargs) -> str:
        """
        Format prompt using the template.
        
        Args:
            **kwargs: Variables to substitute in the template
            
        Returns:
            Formatted prompt string
        """
        if self.template is None:
            raise ValueError("No prompt template configured")
        
        return self.template.render(**kwargs)
    
    def extract_answer(self, response: str, **kwargs) -> any:
        """
        Extract answer from response.
        
        Args:
            response: Model response text
            **kwargs: Additional context
            
        Returns:
            Extracted answer or None
        """
        if self.extractor is None:
            return None
        
        return self.extractor.extract(response, **kwargs)
    
    def score_answer(self, extracted_answer: any, ground_truth: any, **kwargs) -> float:
        """
        Score extracted answer against ground truth.
        
        Args:
            extracted_answer: Extracted answer
            ground_truth: Correct answer
            **kwargs: Additional context
            
        Returns:
            Score (0.0 to 1.0)
        """
        if self.scorer is None:
            return 0.0
        
        return self.scorer.score(extracted_answer, ground_truth, **kwargs)


