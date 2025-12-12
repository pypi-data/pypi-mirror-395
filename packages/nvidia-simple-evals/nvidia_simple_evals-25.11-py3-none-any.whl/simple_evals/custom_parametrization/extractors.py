"""
Extractors for parsing model responses and extracting answers.
"""

import re
from abc import ABC, abstractmethod
from typing import  Optional


class Extractor(ABC):
    """Base class for extractors that parse model responses."""
    
    @abstractmethod
    def extract(self, response: str, **kwargs) -> str | None:
        """
        Extract answer from model response.
        
        Args:
            response: The model's response text
            **kwargs: Additional context or parameters
            
        Returns:
            Extracted answer or None if extraction fails
        """
        pass


class RegexExtractor(Extractor):
    """Extractor that uses regex patterns to extract answers."""
    
    def __init__(self, patterns: list[dict[str, str | int]]):
        """
        Initialize RegexExtractor with patterns.
        
        Args:
            patterns: List of pattern dictionaries with keys:
                - 'regex': The regex pattern string
                - 'match_group': Which capture group to extract (default: 1)
                - 'name': Optional name for the pattern (for debugging)
        """
        self.patterns = []
        for pattern in patterns:
            if isinstance(pattern, str):
                # Simple string pattern
                self.patterns.append({
                    'regex': pattern,
                    'match_group': 1,
                    'name': f'pattern_{len(self.patterns)}'
                })
            elif isinstance(pattern, dict):
                # Pattern dictionary
                pattern_dict = {
                    'regex': pattern['regex'],
                    'match_group': pattern.get('match_group', 1),
                    'name': pattern.get('name', f'pattern_{len(self.patterns)}')
                }
                self.patterns.append(pattern_dict)
            else:
                raise ValueError(f"Invalid pattern format: {pattern}")
    
    def extract(self, response: str, **kwargs) -> str | None:
        """
        Extract answer using regex patterns.
        
        IMPORTANT: This extractor looks for the LAST match of each pattern in the response.
        This is useful when the model might provide multiple answers or explanations,
        and you want to extract the final answer.
        
        Args:
            response: The model's response text
            **kwargs: Additional context (unused)
            
        Returns:
            Extracted answer from the LAST match, or None if no pattern matches
        """
        for pattern_info in self.patterns:
            regex = pattern_info['regex']
            match_group = pattern_info['match_group']
            
            # Find ALL matches and get the LAST one
            matches = list(re.finditer(regex, response, re.MULTILINE | re.DOTALL))
            if matches:
                # Get the last match from the list
                last_match = matches[-1]
                try:
                    extracted = last_match.group(match_group)
                    if extracted:
                        return extracted.strip()
                except IndexError:
                    # If the specified group doesn't exist, continue to next pattern
                    continue
        
        return None


def create_extractor(extraction_config: list[dict] | str | None) -> Optional[Extractor]:
    """
    Factory function to create extractors from configuration.
    
    Args:
        extraction_config: Can be:
            - List of regex patterns (dicts with 'regex' and optional 'match_group')
            - String path to a module class (e.g., "module.ClassName")
            - None (no extraction)
            
    Returns:
        Extractor instance or None
    """
    if extraction_config is None:
        return None
    
    if isinstance(extraction_config, list):
        # Regex patterns
        return RegexExtractor(extraction_config)
    
    elif isinstance(extraction_config, str):
        # Module path to class
        try:
            module_path, class_name = extraction_config.rsplit('.', 1)
            import importlib
            module = importlib.import_module(module_path)
            extractor_class = getattr(module, class_name)
            return extractor_class()
        except (ImportError, AttributeError, ValueError) as e:
            raise ValueError(f"Failed to import extractor from {extraction_config}: {e}")
