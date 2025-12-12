"""
Scorers for evaluating extracted answers against ground truth.
"""

import importlib
from abc import ABC, abstractmethod
from typing import Any, Optional


class Scorer(ABC):
    """Base class for scorers that evaluate answers."""
    
    @abstractmethod
    def score(self, extracted_answer: Any, ground_truth: Any, **kwargs) -> float:
        """
        Score an extracted answer against ground truth.
        
        Args:
            extracted_answer: The answer extracted from model response
            ground_truth: The correct answer
            **kwargs: Additional context or parameters
            
        Returns:
            Score (typically 0.0 for incorrect, 1.0 for correct)
        """
        pass


class EqualityScorer(Scorer):
    """Simple equality-based scorer."""
    
    def __init__(self, case_sensitive: bool = False, strip_whitespace: bool = True):
        """
        Initialize EqualityScorer.
        
        Args:
            case_sensitive: Whether to do case-sensitive comparison
            strip_whitespace: Whether to strip whitespace before comparison
        """
        self.case_sensitive = case_sensitive
        self.strip_whitespace = strip_whitespace
    
    def score(self, extracted_answer: Any, ground_truth: Any, **kwargs) -> float:
        """
        Score by exact equality.
        
        Args:
            extracted_answer: The extracted answer
            ground_truth: The correct answer
            **kwargs: Additional context (unused)
            
        Returns:
            1.0 if answers match, 0.0 otherwise
        """
        if extracted_answer is None:
            return 0.0
        
        # Convert to strings for comparison
        extracted_str = str(extracted_answer)
        ground_truth_str = str(ground_truth)
        
        if self.strip_whitespace:
            extracted_str = extracted_str.strip()
            ground_truth_str = ground_truth_str.strip()
        
        if not self.case_sensitive:
            extracted_str = extracted_str.lower()
            ground_truth_str = ground_truth_str.lower()
        
        return 1.0 if extracted_str == ground_truth_str else 0.0


class MathScorer(Scorer):
    """Scorer for mathematical problems with symbolic evaluation."""
    
    def __init__(self, use_sympy: bool = True, tolerance: float = 1e-6):
        """
        Initialize MathScorer.
        
        Args:
            use_sympy: Whether to use sympy for symbolic evaluation
            tolerance: Numerical tolerance for floating point comparisons
        """
        self.use_sympy = use_sympy
        self.tolerance = tolerance
    
    def score(self, extracted_answer: Any, ground_truth: Any, **kwargs) -> float:
        """
        Score mathematical answers.
        
        Args:
            extracted_answer: The extracted answer
            ground_truth: The correct answer
            **kwargs: Additional context (unused)
            
        Returns:
            1.0 if answers match mathematically, 0.0 otherwise
        """
        if extracted_answer is None:
            return 0.0
        
        try:
            if self.use_sympy:
                return self._score_with_sympy(extracted_answer, ground_truth)
            else:
                return self._score_simple(extracted_answer, ground_truth)
        except Exception:
            # If any error occurs during scoring, return 0.0
            return 0.0
    
    def _score_with_sympy(self, extracted_answer: Any, ground_truth: Any) -> float:
        """Score using sympy for symbolic evaluation."""
        try:
            import sympy
            from sympy import simplify, N
            
            # Convert to sympy expressions
            extracted_expr = sympy.sympify(str(extracted_answer))
            ground_truth_expr = sympy.sympify(str(ground_truth))
            
            # Simplify and compare
            extracted_simplified = simplify(extracted_expr)
            ground_truth_simplified = simplify(ground_truth_expr)
            
            # Try exact equality first
            if extracted_simplified == ground_truth_simplified:
                return 1.0
            
            # Try numerical evaluation
            try:
                extracted_num = N(extracted_simplified)
                ground_truth_num = N(ground_truth_simplified)
                
                if abs(extracted_num - ground_truth_num) < self.tolerance:
                    return 1.0
            except:
                pass
            
            return 0.0
        except ImportError:
            # Fall back to simple scoring if sympy is not available
            return self._score_simple(extracted_answer, ground_truth)
    
    def _score_simple(self, extracted_answer: Any, ground_truth: Any) -> float:
        """Simple string-based scoring."""
        extracted_str = str(extracted_answer).strip()
        ground_truth_str = str(ground_truth).strip()
        
        return 1.0 if extracted_str == ground_truth_str else 0.0


class LLMScorer(Scorer):
    """Scorer that uses an LLM to evaluate answers."""
    
    def __init__(self, judge_config: dict[str, Any]):
        """
        Initialize LLMScorer.
        
        Args:
            judge_config: Configuration for the judge LLM
        """
        self.judge_config = judge_config
        self._judge = None
    
    def score(self, extracted_answer: Any, ground_truth: Any, **kwargs) -> float:
        """
        Score using LLM judge.
        
        Args:
            extracted_answer: The extracted answer
            ground_truth: The correct answer
            **kwargs: Additional context like question, response, etc.
            
        Returns:
            Score from LLM judge (0.0 to 1.0)
        """
        if self._judge is None:
            # Import here to avoid circular imports
            import simple_evals.common as common
            self._judge = common.load_judge(self.judge_config)
        
        if self._judge is None:
            return 0.0
        
        # Create evaluation prompt
        question = kwargs.get('question', '')
        response = kwargs.get('response', '')
        
        prompt = f"""Question: {question}

Model Response: {response}

Extracted Answer: {extracted_answer}
Correct Answer: {ground_truth}

Is the extracted answer correct? Respond with only "Yes" or "No"."""
        
        try:
            judge_response = self._judge([{"role": "user", "content": prompt}])
            return 1.0 if "yes" in judge_response.lower() else 0.0
        except Exception:
            return 0.0


def create_scorer(scoring_config: str | dict[str, Any] | None) -> Optional[Scorer]:
    """
    Factory function to create scorers from configuration.
    
    Args:
        scoring_config: Can be:
            - String path to a module class (e.g., "module.ClassName")
            - Dict with scorer configuration
            - None (no scoring)
            
    Returns:
        Scorer instance or None
    """
    if scoring_config is None:
        return None
    
    if isinstance(scoring_config, str):
        # Module path to class
        try:
            module_path, class_name = scoring_config.rsplit('.', 1)
            module = importlib.import_module(module_path)
            scorer_class = getattr(module, class_name)
            return scorer_class()
        except (ImportError, AttributeError, ValueError) as e:
            raise ValueError(f"Failed to import scorer from {scoring_config}: {e}")
    
    elif isinstance(scoring_config, dict):
        # Dict configuration
        scorer_type = scoring_config.get('type')
        if scorer_type is None:
            raise ValueError("scoring_config dict must contain 'type' key")
        
        if scorer_type == 'equality':
            return EqualityScorer(**scoring_config)
        elif scorer_type == 'math':
            return MathScorer(**scoring_config)
        elif scorer_type == 'llm':
            return LLMScorer(**scoring_config)
        else:
            raise ValueError(f"Unknown scorer type: {scorer_type}")
    
    else:
        raise ValueError(f"Invalid scoring_config format: {type(scoring_config)}")
