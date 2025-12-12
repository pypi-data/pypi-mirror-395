"""Latency consistency evaluator."""

from __future__ import annotations

import statistics
from typing import Any, Dict, List, Optional, Type

from ..base import BaseEval
from ..models import (
    EvalInput,
    EvalResult,
    EvalStatus,
    LatencyConsistencyConfig,
    AssertionDetail,
)


class LatencyConsistencyEval(BaseEval):
    """Evaluator that checks latency consistency across multiple runs.
    
    This evaluator analyzes latency data to ensure:
    - Individual latencies are within acceptable bounds
    - Latency variation (std dev, CV) is acceptable
    - P95/P99 latencies are within bounds
    
    The latency data should be provided in the eval_input.metadata dict
    under the key 'latencies' (list of floats in ms), or passed via kwargs.
    
    Example:
        config = LatencyConsistencyConfig(
            max_latency_ms=5000,
            max_p95_ms=4000,
            coefficient_of_variation_threshold=0.3
        )
        evaluator = LatencyConsistencyEval(config)
        
        result = evaluator.evaluate(
            EvalInput(
                user_input="test query",
                model_output="test response",
                metadata={"latencies": [100, 120, 95, 110, 105]}
            )
        )
    """
    
    name: str = "latency_consistency"
    description: str = "Evaluates latency consistency across multiple runs"
    config_class: Type[LatencyConsistencyConfig] = LatencyConsistencyConfig
    
    def __init__(self, config: Optional[LatencyConsistencyConfig] = None) -> None:
        """Initialize with configuration.
        
        Args:
            config: Configuration for latency thresholds.
        """
        super().__init__(config)
        self.config: LatencyConsistencyConfig = self.config
    
    @classmethod
    def with_thresholds(
        cls,
        max_latency_ms: Optional[float] = None,
        max_p95_ms: Optional[float] = None,
        max_p99_ms: Optional[float] = None,
        cv_threshold: float = 0.5,
    ) -> "LatencyConsistencyEval":
        """Create evaluator with specific thresholds.
        
        Args:
            max_latency_ms: Maximum acceptable latency.
            max_p95_ms: Maximum acceptable P95 latency.
            max_p99_ms: Maximum acceptable P99 latency.
            cv_threshold: Maximum coefficient of variation.
            
        Returns:
            Configured LatencyConsistencyEval instance.
        """
        return cls(LatencyConsistencyConfig(
            max_latency_ms=max_latency_ms,
            max_p95_ms=max_p95_ms,
            max_p99_ms=max_p99_ms,
            coefficient_of_variation_threshold=cv_threshold,
        ))
    
    def evaluate(self, eval_input: EvalInput, **kwargs: Any) -> EvalResult:
        """Evaluate latency consistency.
        
        Args:
            eval_input: Input with latencies in metadata['latencies'].
            **kwargs: Can contain 'latencies' list to override.
            
        Returns:
            EvalResult indicating pass/fail with latency statistics.
        """
        # Get latencies from kwargs or metadata
        latencies = kwargs.get("latencies")
        if latencies is None and eval_input.metadata:
            latencies = eval_input.metadata.get("latencies")
        
        # Handle single latency value
        if latencies is None and eval_input.metadata:
            single_latency = eval_input.metadata.get("latency_ms")
            if single_latency is not None:
                latencies = [single_latency]
        
        if not latencies:
            return EvalResult.error_result(
                eval_name=self.eval_name,
                error=ValueError(
                    "No latencies provided. Pass via kwargs['latencies'] "
                    "or eval_input.metadata['latencies']"
                ),
            )
        
        if not isinstance(latencies, (list, tuple)):
            latencies = [latencies]
        
        # Ensure all are floats
        latencies = [float(lat) for lat in latencies]
        
        if len(latencies) < 1:
            return EvalResult.error_result(
                eval_name=self.eval_name,
                error=ValueError("At least one latency value is required"),
            )
        
        # Calculate statistics
        stats = self._calculate_stats(latencies)
        
        # Run assertions
        assertions: List[AssertionDetail] = []
        all_passed = True
        
        # Check max latency
        if self.config.max_latency_ms is not None:
            passed = stats["max"] <= self.config.max_latency_ms
            all_passed = all_passed and passed
            assertions.append(AssertionDetail(
                name="max_latency",
                passed=passed,
                expected=f"<= {self.config.max_latency_ms} ms",
                actual=f"{stats['max']:.2f} ms",
                message="Maximum latency check",
            ))
        
        # Check std dev
        if self.config.max_std_dev_ms is not None and stats["std_dev"] is not None:
            passed = stats["std_dev"] <= self.config.max_std_dev_ms
            all_passed = all_passed and passed
            assertions.append(AssertionDetail(
                name="std_dev",
                passed=passed,
                expected=f"<= {self.config.max_std_dev_ms} ms",
                actual=f"{stats['std_dev']:.2f} ms",
                message="Standard deviation check",
            ))
        
        # Check P95
        if self.config.max_p95_ms is not None and stats["p95"] is not None:
            passed = stats["p95"] <= self.config.max_p95_ms
            all_passed = all_passed and passed
            assertions.append(AssertionDetail(
                name="p95_latency",
                passed=passed,
                expected=f"<= {self.config.max_p95_ms} ms",
                actual=f"{stats['p95']:.2f} ms",
                message="P95 latency check",
            ))
        
        # Check P99
        if self.config.max_p99_ms is not None and stats["p99"] is not None:
            passed = stats["p99"] <= self.config.max_p99_ms
            all_passed = all_passed and passed
            assertions.append(AssertionDetail(
                name="p99_latency",
                passed=passed,
                expected=f"<= {self.config.max_p99_ms} ms",
                actual=f"{stats['p99']:.2f} ms",
                message="P99 latency check",
            ))
        
        # Check coefficient of variation
        if stats["cv"] is not None:
            passed = stats["cv"] <= self.config.coefficient_of_variation_threshold
            all_passed = all_passed and passed
            assertions.append(AssertionDetail(
                name="coefficient_of_variation",
                passed=passed,
                expected=f"<= {self.config.coefficient_of_variation_threshold}",
                actual=f"{stats['cv']:.4f}",
                message="Coefficient of variation check",
            ))
        
        # Build result
        if not assertions:
            # No thresholds configured, just return stats
            return EvalResult.pass_result(
                eval_name=self.eval_name,
                message="Latency statistics calculated (no thresholds configured)",
                details=stats,
            )
        
        # Calculate score based on how many checks passed
        passed_count = sum(1 for a in assertions if a.passed)
        score = passed_count / len(assertions) if assertions else 1.0
        
        message = (
            f"Latency consistency: {passed_count}/{len(assertions)} checks passed. "
            f"Mean: {stats['mean']:.2f}ms, P95: {stats['p95']:.2f}ms"
            if stats['p95'] is not None
            else f"Latency: {stats['mean']:.2f}ms"
        )
        
        return EvalResult(
            status=EvalStatus.PASSED if all_passed else EvalStatus.FAILED,
            score=score,
            eval_name=self.eval_name,
            message=message,
            assertions=assertions if self.config.include_details else None,
            details=stats if self.config.include_details else None,
        )
    
    def _calculate_stats(self, latencies: List[float]) -> Dict[str, Any]:
        """Calculate latency statistics.
        
        Args:
            latencies: List of latency values in ms.
            
        Returns:
            Dictionary of statistics.
        """
        n = len(latencies)
        sorted_latencies = sorted(latencies)
        
        mean = statistics.mean(latencies)
        
        stats: Dict[str, Any] = {
            "count": n,
            "mean": mean,
            "min": min(latencies),
            "max": max(latencies),
            "median": statistics.median(latencies),
        }
        
        if n >= 2:
            std_dev = statistics.stdev(latencies)
            stats["std_dev"] = std_dev
            stats["cv"] = std_dev / mean if mean > 0 else 0.0
            stats["variance"] = statistics.variance(latencies)
        else:
            stats["std_dev"] = None
            stats["cv"] = None
            stats["variance"] = None
        
        # Percentiles
        if n >= 2:
            stats["p50"] = self._percentile(sorted_latencies, 0.50)
            stats["p90"] = self._percentile(sorted_latencies, 0.90)
            stats["p95"] = self._percentile(sorted_latencies, 0.95)
            stats["p99"] = self._percentile(sorted_latencies, 0.99)
        else:
            stats["p50"] = latencies[0]
            stats["p90"] = latencies[0]
            stats["p95"] = latencies[0]
            stats["p99"] = latencies[0]
        
        return stats
    
    def _percentile(self, sorted_data: List[float], p: float) -> float:
        """Calculate percentile from sorted data.
        
        Args:
            sorted_data: Sorted list of values.
            p: Percentile (0-1).
            
        Returns:
            Percentile value.
        """
        n = len(sorted_data)
        if n == 0:
            return 0.0
        if n == 1:
            return sorted_data[0]
        
        k = (n - 1) * p
        f = int(k)
        c = f + 1 if f + 1 < n else f
        
        if f == c:
            return sorted_data[f]
        
        return sorted_data[f] * (c - k) + sorted_data[c] * (k - f)

