"""Ground truth comparison evaluator."""

from __future__ import annotations

import re
import string
from typing import Any, Optional, Type

from ..base import BaseEval
from ..models import (
    EvalInput,
    EvalResult,
    EvalStatus,
    GroundTruthConfig,
    GroundTruthMatchMode,
    AssertionDetail,
)


class GroundTruthEval(BaseEval):
    """Evaluator that compares model output against expected ground truth.
    
    Supports multiple comparison modes:
    - exact: Exact string match
    - contains: Output contains expected
    - normalized: Whitespace/case normalized comparison
    - semantic: Placeholder for embedding-based comparison
    
    Example:
        config = GroundTruthConfig(
            match_mode=GroundTruthMatchMode.NORMALIZED,
            case_sensitive=False
        )
        evaluator = GroundTruthEval(config)
        
        result = evaluator.evaluate(
            EvalInput(
                user_input="What is 2+2?",
                model_output="The answer is 4.",
                expected_output="4"
            )
        )
    """
    
    name: str = "ground_truth"
    description: str = "Compares model output against expected ground truth"
    config_class: Type[GroundTruthConfig] = GroundTruthConfig
    
    def __init__(self, config: Optional[GroundTruthConfig] = None) -> None:
        """Initialize with configuration.
        
        Args:
            config: Configuration for comparison behavior.
        """
        super().__init__(config)
        self.config: GroundTruthConfig = self.config
    
    @classmethod
    def exact(cls, case_sensitive: bool = True) -> "GroundTruthEval":
        """Create evaluator for exact match comparison.
        
        Args:
            case_sensitive: Whether comparison is case-sensitive.
            
        Returns:
            Configured GroundTruthEval instance.
        """
        return cls(GroundTruthConfig(
            match_mode=GroundTruthMatchMode.EXACT,
            case_sensitive=case_sensitive,
        ))
    
    @classmethod
    def contains(cls, case_sensitive: bool = False) -> "GroundTruthEval":
        """Create evaluator for contains comparison.
        
        Args:
            case_sensitive: Whether comparison is case-sensitive.
            
        Returns:
            Configured GroundTruthEval instance.
        """
        return cls(GroundTruthConfig(
            match_mode=GroundTruthMatchMode.CONTAINS,
            case_sensitive=case_sensitive,
        ))
    
    @classmethod
    def normalized(
        cls,
        case_sensitive: bool = False,
        strip_punctuation: bool = False,
    ) -> "GroundTruthEval":
        """Create evaluator for normalized comparison.
        
        Args:
            case_sensitive: Whether comparison is case-sensitive.
            strip_punctuation: Whether to strip punctuation.
            
        Returns:
            Configured GroundTruthEval instance.
        """
        return cls(GroundTruthConfig(
            match_mode=GroundTruthMatchMode.NORMALIZED,
            case_sensitive=case_sensitive,
            strip_punctuation=strip_punctuation,
        ))
    
    def evaluate(self, eval_input: EvalInput, **kwargs: Any) -> EvalResult:
        """Evaluate model output against ground truth.
        
        Args:
            eval_input: Input containing model_output and expected_output.
            **kwargs: Can contain 'expected' to override eval_input.expected_output.
            
        Returns:
            EvalResult indicating pass/fail.
        """
        # Get expected output from kwargs or eval_input
        expected = kwargs.get("expected", eval_input.expected_output)
        
        if expected is None:
            return EvalResult.error_result(
                eval_name=self.eval_name,
                error=ValueError("No expected_output provided in eval_input or kwargs"),
            )
        
        output = eval_input.model_output
        
        # Perform comparison based on mode
        match_mode = self.config.match_mode
        
        if match_mode == GroundTruthMatchMode.EXACT:
            passed, score, details = self._exact_match(output, expected)
        elif match_mode == GroundTruthMatchMode.CONTAINS:
            passed, score, details = self._contains_match(output, expected)
        elif match_mode == GroundTruthMatchMode.NORMALIZED:
            passed, score, details = self._normalized_match(output, expected)
        elif match_mode == GroundTruthMatchMode.SEMANTIC:
            return EvalResult.error_result(
                eval_name=self.eval_name,
                error=NotImplementedError("Semantic matching not yet implemented"),
            )
        else:
            return EvalResult.error_result(
                eval_name=self.eval_name,
                error=ValueError(f"Unknown match mode: {match_mode}"),
            )
        
        # Build result
        message = f"Ground truth comparison ({match_mode.value}): {'MATCH' if passed else 'NO MATCH'}"
        
        assertions = [
            AssertionDetail(
                name=f"ground_truth_{match_mode.value}",
                passed=passed,
                expected=expected[:200] + "..." if len(expected) > 200 else expected,
                actual=output[:200] + "..." if len(output) > 200 else output,
                message=message,
            )
        ]
        
        result_details = {
            "match_mode": match_mode.value,
            "case_sensitive": self.config.case_sensitive,
            **details,
        }
        
        return EvalResult(
            status=EvalStatus.PASSED if passed else EvalStatus.FAILED,
            score=score,
            eval_name=self.eval_name,
            message=message,
            assertions=assertions if self.config.include_details else None,
            details=result_details if self.config.include_details else None,
        )
    
    def _exact_match(
        self,
        output: str,
        expected: str,
    ) -> tuple[bool, float, dict[str, Any]]:
        """Perform exact match comparison.
        
        Args:
            output: Model output.
            expected: Expected output.
            
        Returns:
            Tuple of (passed, score, details).
        """
        if not self.config.case_sensitive:
            output = output.lower()
            expected = expected.lower()
        
        passed = output == expected
        score = 1.0 if passed else 0.0
        
        return passed, score, {"comparison": "exact"}
    
    def _contains_match(
        self,
        output: str,
        expected: str,
    ) -> tuple[bool, float, dict[str, Any]]:
        """Check if output contains expected.
        
        Args:
            output: Model output.
            expected: Expected output.
            
        Returns:
            Tuple of (passed, score, details).
        """
        if not self.config.case_sensitive:
            output = output.lower()
            expected = expected.lower()
        
        passed = expected in output
        
        # Score based on how much of output is the expected
        if passed:
            score = len(expected) / len(output) if output else 1.0
            score = min(score, 1.0)
        else:
            score = 0.0
        
        return passed, score, {"comparison": "contains"}
    
    def _normalized_match(
        self,
        output: str,
        expected: str,
    ) -> tuple[bool, float, dict[str, Any]]:
        """Perform normalized comparison.
        
        Args:
            output: Model output.
            expected: Expected output.
            
        Returns:
            Tuple of (passed, score, details).
        """
        normalized_output = self._normalize(output)
        normalized_expected = self._normalize(expected)
        
        # Check exact match after normalization
        if normalized_output == normalized_expected:
            return True, 1.0, {"comparison": "normalized", "normalized_match": True}
        
        # Check if one contains the other
        if normalized_expected in normalized_output:
            score = len(normalized_expected) / len(normalized_output)
            return True, score, {"comparison": "normalized", "contains": True}
        
        # Calculate similarity score
        similarity = self._calculate_similarity(normalized_output, normalized_expected)
        passed = similarity >= self.config.similarity_threshold
        
        return passed, similarity, {
            "comparison": "normalized",
            "similarity": similarity,
            "threshold": self.config.similarity_threshold,
        }
    
    def _normalize(self, text: str) -> str:
        """Normalize text for comparison.
        
        Args:
            text: Text to normalize.
            
        Returns:
            Normalized text.
        """
        result = text
        
        # Case normalization
        if not self.config.case_sensitive:
            result = result.lower()
        
        # Whitespace normalization
        if self.config.normalize_whitespace:
            result = " ".join(result.split())
        
        # Punctuation removal
        if self.config.strip_punctuation:
            result = result.translate(str.maketrans("", "", string.punctuation))
        
        return result.strip()
    
    def _calculate_similarity(self, s1: str, s2: str) -> float:
        """Calculate similarity between two strings.
        
        Uses a simple token-based Jaccard similarity.
        
        Args:
            s1: First string.
            s2: Second string.
            
        Returns:
            Similarity score between 0 and 1.
        """
        if not s1 or not s2:
            return 0.0
        
        # Tokenize
        tokens1 = set(s1.split())
        tokens2 = set(s2.split())
        
        if not tokens1 or not tokens2:
            return 0.0
        
        # Jaccard similarity
        intersection = tokens1 & tokens2
        union = tokens1 | tokens2
        
        return len(intersection) / len(union) if union else 0.0

