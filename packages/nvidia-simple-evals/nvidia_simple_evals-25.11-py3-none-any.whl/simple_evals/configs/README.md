# Evaluation Configuration System

This directory contains configuration files for customizing evaluation behavior in simple-evals. The new configuration system allows you to override extraction, scoring, and prompt templates for any evaluation.

## Overview

The evaluation configuration system consists of three main components:

1. **Extraction**: How to extract answers from model responses
2. **Scoring**: How to score extracted answers against ground truth
3. **Prompt Template**: How to format prompts using Jinja2 templates

## Configuration File Format

Configuration files are YAML files with the following structure:

```yaml
eval_name: mmlu  # Optional: override the evaluation name

# Extraction configuration
extraction:
  - regex: "Answer:\\s*([A-D])"
    match_group: 1
    name: "answer_colon"

# Scoring configuration
scoring:
  type: equality
  case_sensitive: false
  strip_whitespace: true

# Prompt template (Jinja2)
prompt_template: |
  {{ Question }}
  
  A) {{ A }}
  B) {{ B }}
  C) {{ C }}
  D) {{ D }}
  
  Answer with just the letter (A, B, C, or D).

# Additional configuration (overrides hardcoded defaults)
language: "fr"  # For MMLU evaluations
num_examples_per_lang: 100  # For MGSM evaluations
judge_config:  # For math evaluations
  url: "https://api.openai.com/v1/chat/completions"
  model: "gpt-4o-mini"
grader_config:  # For SimpleQA evaluations
  url: "https://api.openai.com/v1/chat/completions"
  model: "gpt-4o-mini"
```

## Usage

### Command Line

Use the `--eval_cfg_file` argument to specify a custom configuration:

```bash
python -m simple_evals \
  --eval_name mmlu \
  --eval_cfg_file configs/mmlu_custom.yml \
  --model your-model \
  --url your-api-url
```

### Programmatic

```python
from simple_evals.config_loader import load_eval_config

# Load configuration from file
config = load_eval_config("configs/mmlu_custom.yml")

# Use the configuration
extracted = config.extract_answer(response_text)
score = config.score_answer(extracted, ground_truth)
prompt = config.format_prompt(Question="What is 2+2?", A="3", B="4", C="5", D="6")
```

## Extraction Options

### 1. Regex Patterns (List)

```yaml
extraction:
  - regex: "Answer:\\s*([A-D])"
    match_group: 1
    name: "answer_colon"
  - regex: "The answer is\\s*([^\\n]+)"
    match_group: 1
    name: "answer_is"
```

### 2. Simple String Patterns

```yaml
extraction:
  - "Answer: ([A-D])"
  - "([A-D])"
```

### 3. Custom Extractor Class

```yaml
extraction: "simple_evals.extractors.NemoExtractor"
```

### 4. No Extraction (Pass-through)

```yaml
extraction: null
```

## Scoring Options

### 1. Equality Scorer

```yaml
scoring:
  type: equality
  case_sensitive: false
  strip_whitespace: true
```

### 2. Math Scorer

```yaml
scoring:
  type: math
  use_sympy: true
  tolerance: 1e-6
```

### 3. LLM Scorer

```yaml
scoring:
  type: llm
  judge_config:
    url: "https://api.openai.com/v1/chat/completions"
    model: "gpt-4"
    api_key: "OPENAI_API_KEY"
    temperature: 0.0
    max_tokens: 10
```

### 4. Custom Scorer Class

```yaml
scoring: "my_module.MyCustomScorer"
```

### 5. No Scoring

```yaml
scoring: null
```

## Prompt Templates

Prompt templates use Jinja2 syntax and can reference any variables from the dataset:

```yaml
prompt_template: |
  {{ Question }}
  
  A) {{ A }}
  B) {{ B }}
  C) {{ C }}
  D) {{ D }}
  
  Please provide your answer by selecting A, B, C, or D.
```

## Example Configurations

### Math Evaluation

```yaml
eval_name: math_test_500
extraction:
  - regex: "Answer:\\s*([^\\n]+)"
    match_group: 1
scoring:
  type: math
  use_sympy: true
prompt_template: |
  Solve the following math problem step by step.
  
  {{ Question }}
  
  Answer: 
```

### Multiple Choice

```yaml
eval_name: mmlu
extraction:
  - regex: "Answer:\\s*([A-D])"
    match_group: 1
scoring:
  type: equality
  case_sensitive: false
prompt_template: |
  {{ Question }}
  
  A) {{ A }}
  B) {{ B }}
  C) {{ C }}
  D) {{ D }}
  
  Answer: 
```

### Code Generation

```yaml
eval_name: humaneval
extraction: null  # Pass through full response
scoring:
  type: equality
  case_sensitive: false
  strip_whitespace: true
prompt_template: |
  {{ prompt }}
  
  Complete the function implementation:
```

## Creating Custom Extractors

You can create custom extractors by inheriting from the `Extractor` base class:

```python
from simple_evals.extractors import Extractor

class MyCustomExtractor(Extractor):
    def extract(self, response: str, **kwargs) -> Any:
        # Your custom extraction logic here
        return extracted_answer
```

## Creating Custom Scorers

You can create custom scorers by inheriting from the `Scorer` base class:

```python
from simple_evals.scorers import Scorer

class MyCustomScorer(Scorer):
    def score(self, extracted_answer: Any, ground_truth: Any, **kwargs) -> float:
        # Your custom scoring logic here
        return score
```

## Overriding Hardcoded Values

The configuration system allows you to override previously hardcoded values in the evaluation framework:

### MMLU Evaluations
```yaml
language: "fr"  # Override the default language derivation
```

### MGSM Evaluations
```yaml
num_examples_per_lang: 100  # Override the hardcoded 250 examples
```

### Math Evaluations
```yaml
judge_config:
  url: "https://api.openai.com/v1/chat/completions"
  model: "gpt-4o-mini"  # Override hardcoded "gpt4" or "llama70b"
  api_key: "OPENAI_API_KEY"
```

### SimpleQA Evaluations
```yaml
grader_config:
  url: "https://api.openai.com/v1/chat/completions"
  model: "gpt-4o-mini"  # Override hardcoded "gpt4"
  api_key: "OPENAI_API_KEY"
```

## Integration with Existing Evaluations

The configuration system integrates seamlessly with existing evaluations. When you provide a configuration file:

1. The `eval_name` from the config is used (if specified)
2. Custom extractor and scorer override the defaults
3. Previously hardcoded values are overridden by config values
4. The evaluation runs with your custom configuration

This allows you to experiment with different extraction and scoring methods without modifying the core evaluation code. 