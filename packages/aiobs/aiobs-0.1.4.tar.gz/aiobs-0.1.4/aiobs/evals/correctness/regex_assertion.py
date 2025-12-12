"""Regex-based assertion evaluator."""

from __future__ import annotations

import re
from typing import Any, List, Optional, Type

from ..base import BaseEval
from ..models import (
    EvalInput,
    EvalResult,
    EvalStatus,
    RegexAssertionConfig,
    AssertionDetail,
)


class RegexAssertion(BaseEval):
    """Evaluator that asserts model output matches regex patterns.
    
    This evaluator checks if the model output matches specified regex patterns
    and does NOT match negative patterns.
    
    Example:
        # Check that output contains an email
        config = RegexAssertionConfig(
            patterns=[r"[\\w.-]+@[\\w.-]+\\.\\w+"],
            case_sensitive=False
        )
        evaluator = RegexAssertion(config)
        
        result = evaluator.evaluate(
            EvalInput(
                user_input="Give me an email",
                model_output="Contact us at support@example.com"
            )
        )
        assert result.passed
        
        # Check that output does NOT contain certain words
        config = RegemaAssertionConfig(
            negative_patterns=[r"\\b(sorry|cannot|unable)\\b"],
            case_sensitive=False
        )
    """
    
    name: str = "regex_assertion"
    description: str = "Asserts that output matches/doesn't match regex patterns"
    config_class: Type[RegexAssertionConfig] = RegexAssertionConfig
    
    def __init__(self, config: Optional[RegexAssertionConfig] = None) -> None:
        """Initialize with config or create from patterns.
        
        Args:
            config: Configuration with patterns and options.
        """
        super().__init__(config)
        self.config: RegexAssertionConfig = self.config
        self._compiled_patterns = self.config.get_compiled_patterns()
        self._compiled_negative_patterns = self.config.get_compiled_negative_patterns()
    
    @classmethod
    def from_patterns(
        cls,
        patterns: Optional[List[str]] = None,
        negative_patterns: Optional[List[str]] = None,
        case_sensitive: bool = True,
        match_mode: str = "any",
    ) -> "RegexAssertion":
        """Create evaluator from pattern lists.
        
        Args:
            patterns: Patterns that must match.
            negative_patterns: Patterns that must NOT match.
            case_sensitive: Whether matching is case-sensitive.
            match_mode: 'any' or 'all' for positive patterns.
            
        Returns:
            Configured RegexAssertion instance.
        """
        config = RegexAssertionConfig(
            patterns=patterns or [],
            negative_patterns=negative_patterns or [],
            case_sensitive=case_sensitive,
            match_mode=match_mode,
        )
        return cls(config)
    
    def evaluate(self, eval_input: EvalInput, **kwargs: Any) -> EvalResult:
        """Evaluate if model output matches regex patterns.
        
        Args:
            eval_input: Input containing model_output to check.
            **kwargs: Additional arguments (unused).
            
        Returns:
            EvalResult indicating pass/fail.
        """
        output = eval_input.model_output
        assertions: List[AssertionDetail] = []
        
        # Check positive patterns
        positive_matches: List[bool] = []
        for pattern in self._compiled_patterns:
            match = pattern.search(output)
            matched = match is not None
            positive_matches.append(matched)
            
            assertions.append(AssertionDetail(
                name=f"match:{pattern.pattern}",
                passed=matched,
                expected=f"Output should match: {pattern.pattern}",
                actual=match.group(0) if match else None,
                message="Pattern matched" if matched else "Pattern not found",
            ))
            
            if not matched and self.config.fail_fast:
                return self._build_result(
                    passed=False,
                    assertions=assertions,
                    message=f"Pattern not found: {pattern.pattern}",
                )
        
        # Check negative patterns
        negative_violations: List[str] = []
        for pattern in self._compiled_negative_patterns:
            match = pattern.search(output)
            violated = match is not None
            
            assertions.append(AssertionDetail(
                name=f"no_match:{pattern.pattern}",
                passed=not violated,
                expected=f"Output should NOT match: {pattern.pattern}",
                actual=match.group(0) if match else None,
                message="Pattern incorrectly found" if violated else "Pattern correctly absent",
            ))
            
            if violated:
                negative_violations.append(pattern.pattern)
                if self.config.fail_fast:
                    return self._build_result(
                        passed=False,
                        assertions=assertions,
                        message=f"Negative pattern matched: {pattern.pattern}",
                    )
        
        # Determine overall pass/fail
        positive_pass = self._check_positive_patterns(positive_matches)
        negative_pass = len(negative_violations) == 0
        passed = positive_pass and negative_pass
        
        # Build message
        if passed:
            message = "All regex assertions passed"
        else:
            messages = []
            if not positive_pass:
                if self.config.match_mode == "all":
                    messages.append("Not all required patterns matched")
                else:
                    messages.append("No patterns matched")
            if not negative_pass:
                messages.append(f"Negative patterns matched: {negative_violations}")
            message = "; ".join(messages)
        
        return self._build_result(
            passed=passed,
            assertions=assertions,
            message=message,
        )
    
    def _check_positive_patterns(self, matches: List[bool]) -> bool:
        """Check if positive pattern requirement is met.
        
        Args:
            matches: List of match results for each pattern.
            
        Returns:
            True if requirement is met.
        """
        if not matches:
            return True  # No patterns to check
        
        if self.config.match_mode == "all":
            return all(matches)
        else:  # "any"
            return any(matches)
    
    def _build_result(
        self,
        passed: bool,
        assertions: List[AssertionDetail],
        message: str,
    ) -> EvalResult:
        """Build the evaluation result.
        
        Args:
            passed: Whether evaluation passed.
            assertions: List of assertion details.
            message: Result message.
            
        Returns:
            Configured EvalResult.
        """
        # Calculate score based on passed assertions
        if assertions:
            passed_count = sum(1 for a in assertions if a.passed)
            score = passed_count / len(assertions)
        else:
            score = 1.0 if passed else 0.0
        
        return EvalResult(
            status=EvalStatus.PASSED if passed else EvalStatus.FAILED,
            score=score,
            eval_name=self.eval_name,
            message=message,
            assertions=assertions if self.config.include_details else None,
            details={
                "match_mode": self.config.match_mode,
                "pattern_count": len(self.config.patterns),
                "negative_pattern_count": len(self.config.negative_patterns),
            } if self.config.include_details else None,
        )

