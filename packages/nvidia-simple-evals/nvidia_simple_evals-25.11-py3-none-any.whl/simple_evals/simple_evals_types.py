from dataclasses import dataclass, field
from typing import Any
from simple_evals.custom_parametrization.config_loader import EvalConfig
from simple_evals.seed_generator import SeedGenerator
import json

Message = dict[str, Any]  # keys role, content
MessageList = list[Message]


class SamplerBase:
    """
    Base class for defining a sampling model, which can be evaluated,
    or used as part of the grading process.
    """

    def __call__(self, message_list: MessageList) -> str:
        raise NotImplementedError


@dataclass
class EvalResult:
    """
    Result of running an evaluation (usually consisting of many samples)
    """

    task_name: str  # task name (e.g. mgsm)
    score: float | None  # top-line metric
    metrics: dict[str, float] | None  # other metrics
    htmls: list[str]  # strings of valid HTML
    convos: list[MessageList]  # sampled conversations

    def to_dict(self) -> dict:
        return {
            'task_name': self.task_name,
            'score': self.score,
            'metrics': self.metrics,
            'htmls': self.htmls,
            'convos': self.convos
        }

    def __str__(self) -> str:
        return json.dumps(self.to_dict())

    @classmethod
    def from_dict(cls, data: dict) -> 'EvalResult':
        return cls(
            task_name=data['task_name'],
            score=data['score'],
            metrics=data['metrics'],
            htmls=data['htmls'],
            convos=data['convos']
        )

    @classmethod
    def from_json(cls, json_str: str) -> 'EvalResult':
        return cls.from_dict(json.loads(json_str))


@dataclass
class SingleEvalResult:
    """
    Result of evaluating a single sample
    """

    score: float | None
    metrics: dict[str, float] = field(default_factory=dict)
    html: str | None = None
    convo: MessageList | None = None  # sampled conversation

    def to_dict(self) -> dict:
        return {
            'score': self.score,
            'metrics': self.metrics,
            'html': self.html,
            'convo': self.convo
        }

    def __str__(self) -> str:
        return json.dumps(self.to_dict())

    @classmethod
    def from_dict(cls, data: dict) -> 'SingleEvalResult':
        return cls(
            score=data['score'],
            metrics=data.get('metrics', {}),
            html=data.get('html'),
            convo=data.get('convo')
        )

    @classmethod
    def from_json(cls, json_str: str) -> 'SingleEvalResult':
        return cls.from_dict(json.loads(json_str))


class Eval:
    """
    Base class for defining an evaluation.
    """

    def __init__(
        self, 
        seed_generator: SeedGenerator | None = None,
        custom_eval_config: EvalConfig | None = None
    ):
        self.seed_generator = seed_generator or SeedGenerator()
        self.custom_eval_config = custom_eval_config

    async def __call__(self, sampler: SamplerBase) -> EvalResult:
        raise NotImplementedError
