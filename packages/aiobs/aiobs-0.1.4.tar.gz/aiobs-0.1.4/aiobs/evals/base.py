"""Base evaluator interface for aiobs.evals."""

from __future__ import annotations

import time
from abc import ABC, abstractmethod
from typing import Any, List, Optional, Type, TypeVar

from .models import BaseEvalConfig, EvalInput, EvalResult

ConfigT = TypeVar("ConfigT", bound=BaseEvalConfig)


class BaseEval(ABC):
    """Abstract base class for all evaluators.
    
    Evaluators assess model outputs against various criteria such as
    correctness, safety, performance, and more.
    
    Subclasses must implement:
        - evaluate(): Synchronous evaluation of a single input
        
    Optionally override:
        - evaluate_async(): Asynchronous evaluation
        - evaluate_batch(): Batch evaluation
        
    Example usage:
        from aiobs.evals import RegexAssertion, RegexAssertionConfig
        
        config = RegexAssertionConfig(
            patterns=[r".*Paris.*"],
            case_sensitive=False
        )
        evaluator = RegexAssertion(config)
        
        result = evaluator.evaluate(
            EvalInput(
                user_input="What is the capital of France?",
                model_output="The capital of France is Paris."
            )
        )
        print(result.status)  # EvalStatus.PASSED
    """
    
    # Class-level attributes
    name: str = "base_eval"
    description: str = "Base evaluator"
    config_class: Type[BaseEvalConfig] = BaseEvalConfig
    
    def __init__(self, config: Optional[ConfigT] = None) -> None:
        """Initialize the evaluator with optional configuration.
        
        Args:
            config: Configuration for evaluator behavior. If None, uses defaults.
        """
        self.config: ConfigT = config or self.config_class()  # type: ignore
        # Allow config to override the eval name
        if self.config.name:
            self._instance_name = self.config.name
        else:
            self._instance_name = self.name
    
    @property
    def eval_name(self) -> str:
        """Get the name to use in results."""
        return self._instance_name
    
    @classmethod
    def is_available(cls) -> bool:
        """Check if this evaluator can be used (dependencies present).
        
        Returns:
            True if all required dependencies are available.
        """
        return True
    
    @abstractmethod
    def evaluate(self, eval_input: EvalInput, **kwargs: Any) -> EvalResult:
        """Evaluate a model output synchronously.
        
        Args:
            eval_input: The input containing user_input, model_output, etc.
            **kwargs: Additional arguments for the evaluator.
        
        Returns:
            EvalResult with status, score, and details.
        """
        raise NotImplementedError
    
    async def evaluate_async(self, eval_input: EvalInput, **kwargs: Any) -> EvalResult:
        """Evaluate a model output asynchronously.
        
        Default implementation calls synchronous evaluate().
        Override for truly async evaluators.
        
        Args:
            eval_input: The input containing user_input, model_output, etc.
            **kwargs: Additional arguments for the evaluator.
        
        Returns:
            EvalResult with status, score, and details.
        """
        return self.evaluate(eval_input, **kwargs)
    
    def evaluate_batch(
        self,
        inputs: List[EvalInput],
        **kwargs: Any,
    ) -> List[EvalResult]:
        """Evaluate multiple model outputs in batch.
        
        Default implementation calls evaluate() for each input.
        Override for optimized batch processing.
        
        Args:
            inputs: List of EvalInput objects to evaluate.
            **kwargs: Additional arguments for the evaluator.
        
        Returns:
            List of EvalResult objects, one per input.
        """
        return [self.evaluate(inp, **kwargs) for inp in inputs]
    
    async def evaluate_batch_async(
        self,
        inputs: List[EvalInput],
        **kwargs: Any,
    ) -> List[EvalResult]:
        """Evaluate multiple model outputs asynchronously in batch.
        
        Default implementation calls evaluate_async() for each input.
        Override for optimized async batch processing.
        
        Args:
            inputs: List of EvalInput objects to evaluate.
            **kwargs: Additional arguments for the evaluator.
        
        Returns:
            List of EvalResult objects, one per input.
        """
        results = []
        for inp in inputs:
            result = await self.evaluate_async(inp, **kwargs)
            results.append(result)
        return results
    
    def _timed_evaluate(
        self,
        eval_input: EvalInput,
        **kwargs: Any,
    ) -> EvalResult:
        """Run evaluation with timing.
        
        Args:
            eval_input: The input to evaluate.
            **kwargs: Additional arguments.
            
        Returns:
            EvalResult with duration_ms populated.
        """
        start = time.perf_counter()
        result = self.evaluate(eval_input, **kwargs)
        duration_ms = (time.perf_counter() - start) * 1000
        result.duration_ms = duration_ms
        return result
    
    def __call__(self, eval_input: EvalInput, **kwargs: Any) -> EvalResult:
        """Allow evaluator to be called directly.
        
        Args:
            eval_input: The input to evaluate.
            **kwargs: Additional arguments.
            
        Returns:
            EvalResult from evaluate().
        """
        return self._timed_evaluate(eval_input, **kwargs)
    
    def __repr__(self) -> str:
        """String representation."""
        return f"{self.__class__.__name__}(name={self.eval_name!r})"

