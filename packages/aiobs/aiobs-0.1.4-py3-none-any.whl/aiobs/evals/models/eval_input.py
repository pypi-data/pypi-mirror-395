"""Input model for evaluations."""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class EvalInput(BaseModel):
    """Standard input model for evaluations.
    
    This is the core data structure that evaluators use to assess
    model outputs. It captures the full context of an LLM interaction.
    
    Example:
        eval_input = EvalInput(
            user_input="What is the capital of France?",
            model_output="The capital of France is Paris.",
            system_prompt="You are a helpful geography assistant."
        )
    """
    
    user_input: str = Field(
        description="The user's input/query to the model"
    )
    model_output: str = Field(
        description="The model's generated response to evaluate"
    )
    system_prompt: Optional[str] = Field(
        default=None,
        description="The system prompt provided to the model"
    )
    expected_output: Optional[str] = Field(
        default=None,
        description="Expected/ground-truth output for comparison evals"
    )
    context: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Additional context (e.g., retrieved docs, conversation history)"
    )
    metadata: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Additional metadata (e.g., latency, token counts, timestamps)"
    )
    tags: Optional[List[str]] = Field(
        default=None,
        description="Tags for categorizing or filtering eval inputs"
    )

    def with_expected(self, expected_output: str) -> "EvalInput":
        """Return a copy with expected_output set.
        
        Args:
            expected_output: The expected/ground-truth output.
            
        Returns:
            New EvalInput with expected_output set.
        """
        return self.model_copy(update={"expected_output": expected_output})
    
    def with_metadata(self, **kwargs: Any) -> "EvalInput":
        """Return a copy with additional metadata merged.
        
        Args:
            **kwargs: Key-value pairs to add to metadata.
            
        Returns:
            New EvalInput with merged metadata.
        """
        current_metadata = self.metadata or {}
        return self.model_copy(update={"metadata": {**current_metadata, **kwargs}})

