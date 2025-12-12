"""Result model for evaluations."""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class EvalStatus(str, Enum):
    """Status of an evaluation result."""
    
    PASSED = "passed"
    FAILED = "failed"
    ERROR = "error"
    SKIPPED = "skipped"


class EvalResult(BaseModel):
    """Result model for evaluations.
    
    Contains the evaluation outcome, score, and detailed information
    about what was evaluated and why it passed/failed.
    
    Example:
        result = EvalResult(
            status=EvalStatus.PASSED,
            score=1.0,
            eval_name="regex_assertion",
            message="Output matches pattern: .*Paris.*"
        )
    """
    
    status: EvalStatus = Field(
        description="Overall evaluation status: passed, failed, error, or skipped"
    )
    score: float = Field(
        ge=0.0,
        le=1.0,
        description="Numeric score between 0 (worst) and 1 (best)"
    )
    eval_name: str = Field(
        description="Name of the evaluator that produced this result"
    )
    message: Optional[str] = Field(
        default=None,
        description="Human-readable message explaining the result"
    )
    details: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Detailed information about the evaluation (matches, violations, etc.)"
    )
    assertions: Optional[List["AssertionDetail"]] = Field(
        default=None,
        description="List of individual assertion results (for multi-assertion evals)"
    )
    duration_ms: Optional[float] = Field(
        default=None,
        description="Time taken to run the evaluation in milliseconds"
    )
    evaluated_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Timestamp when evaluation was performed"
    )
    metadata: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Additional metadata from the evaluator"
    )

    @property
    def passed(self) -> bool:
        """Check if the evaluation passed."""
        return self.status == EvalStatus.PASSED
    
    @property
    def failed(self) -> bool:
        """Check if the evaluation failed."""
        return self.status == EvalStatus.FAILED

    @classmethod
    def pass_result(
        cls,
        eval_name: str,
        score: float = 1.0,
        message: Optional[str] = None,
        **kwargs: Any,
    ) -> "EvalResult":
        """Create a passing result.
        
        Args:
            eval_name: Name of the evaluator.
            score: Score between 0 and 1 (default 1.0).
            message: Optional message.
            **kwargs: Additional fields.
            
        Returns:
            EvalResult with PASSED status.
        """
        return cls(
            status=EvalStatus.PASSED,
            score=score,
            eval_name=eval_name,
            message=message,
            **kwargs,
        )
    
    @classmethod
    def fail_result(
        cls,
        eval_name: str,
        score: float = 0.0,
        message: Optional[str] = None,
        **kwargs: Any,
    ) -> "EvalResult":
        """Create a failing result.
        
        Args:
            eval_name: Name of the evaluator.
            score: Score between 0 and 1 (default 0.0).
            message: Optional message.
            **kwargs: Additional fields.
            
        Returns:
            EvalResult with FAILED status.
        """
        return cls(
            status=EvalStatus.FAILED,
            score=score,
            eval_name=eval_name,
            message=message,
            **kwargs,
        )
    
    @classmethod
    def error_result(
        cls,
        eval_name: str,
        error: Exception,
        **kwargs: Any,
    ) -> "EvalResult":
        """Create an error result.
        
        Args:
            eval_name: Name of the evaluator.
            error: The exception that occurred.
            **kwargs: Additional fields.
            
        Returns:
            EvalResult with ERROR status.
        """
        return cls(
            status=EvalStatus.ERROR,
            score=0.0,
            eval_name=eval_name,
            message=f"Evaluation error: {str(error)}",
            details={"error_type": type(error).__name__, "error_message": str(error)},
            **kwargs,
        )


class AssertionDetail(BaseModel):
    """Detail for a single assertion within an evaluation."""
    
    name: str = Field(
        description="Name or description of the assertion"
    )
    passed: bool = Field(
        description="Whether this assertion passed"
    )
    expected: Optional[Any] = Field(
        default=None,
        description="Expected value (if applicable)"
    )
    actual: Optional[Any] = Field(
        default=None,
        description="Actual value found"
    )
    message: Optional[str] = Field(
        default=None,
        description="Additional context about the assertion"
    )


# Update forward reference
EvalResult.model_rebuild()

