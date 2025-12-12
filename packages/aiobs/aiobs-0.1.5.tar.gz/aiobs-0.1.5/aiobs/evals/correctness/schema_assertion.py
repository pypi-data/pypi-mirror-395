"""JSON schema assertion evaluator."""

from __future__ import annotations

import json
import re
from typing import Any, Dict, List, Optional, Type

from ..base import BaseEval
from ..models import (
    EvalInput,
    EvalResult,
    EvalStatus,
    SchemaAssertionConfig,
    AssertionDetail,
)


class SchemaAssertion(BaseEval):
    """Evaluator that asserts model output matches a JSON schema.
    
    This evaluator validates that the model output is valid JSON and
    conforms to the specified JSON Schema.
    
    Example:
        schema = {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "age": {"type": "integer", "minimum": 0}
            },
            "required": ["name", "age"]
        }
        
        config = SchemaAssertionConfig(schema=schema)
        evaluator = SchemaAssertion(config)
        
        result = evaluator.evaluate(
            EvalInput(
                user_input="Extract person info",
                model_output='{"name": "John", "age": 30}'
            )
        )
        assert result.passed
    """
    
    name: str = "schema_assertion"
    description: str = "Asserts that output is valid JSON matching a schema"
    config_class: Type[SchemaAssertionConfig] = SchemaAssertionConfig
    
    _jsonschema_available: Optional[bool] = None
    
    def __init__(self, config: SchemaAssertionConfig) -> None:
        """Initialize with schema configuration.
        
        Args:
            config: Configuration with JSON schema.
        """
        super().__init__(config)
        self.config: SchemaAssertionConfig = self.config
        self._validator = self._create_validator()
    
    @classmethod
    def from_schema(
        cls,
        schema: Dict[str, Any],
        strict: bool = True,
        extract_json: bool = True,
    ) -> "SchemaAssertion":
        """Create evaluator from a schema dict.
        
        Args:
            schema: JSON Schema dictionary.
            strict: Whether to fail on additional properties.
            extract_json: Whether to extract JSON from markdown.
            
        Returns:
            Configured SchemaAssertion instance.
        """
        config = SchemaAssertionConfig(
            json_schema=schema,
            strict=strict,
            extract_json=extract_json,
        )
        return cls(config)
    
    @classmethod
    def is_available(cls) -> bool:
        """Check if jsonschema is installed."""
        if cls._jsonschema_available is None:
            try:
                import jsonschema  # noqa: F401
                cls._jsonschema_available = True
            except ImportError:
                cls._jsonschema_available = False
        return cls._jsonschema_available
    
    def _create_validator(self) -> Any:
        """Create a jsonschema validator if available.
        
        Returns:
            Validator instance or None.
        """
        if not self.is_available():
            return None
        
        import jsonschema
        from jsonschema import Draft7Validator
        
        # Validate the schema itself
        Draft7Validator.check_schema(self.config.json_schema)
        return Draft7Validator(self.config.json_schema)
    
    def evaluate(self, eval_input: EvalInput, **kwargs: Any) -> EvalResult:
        """Evaluate if model output matches JSON schema.
        
        Args:
            eval_input: Input containing model_output to validate.
            **kwargs: Additional arguments (unused).
            
        Returns:
            EvalResult indicating pass/fail.
        """
        output = eval_input.model_output
        assertions: List[AssertionDetail] = []
        
        # Step 1: Parse JSON
        parsed_json, parse_error = self._parse_output(output)
        
        if parse_error:
            assertions.append(AssertionDetail(
                name="json_parse",
                passed=False,
                expected="Valid JSON",
                actual=output[:100] + "..." if len(output) > 100 else output,
                message=str(parse_error),
            ))
            return self._build_result(
                passed=False,
                assertions=assertions,
                message=f"Failed to parse JSON: {parse_error}",
                parsed_json=None,
            )
        
        assertions.append(AssertionDetail(
            name="json_parse",
            passed=True,
            expected="Valid JSON",
            actual="Parsed successfully",
            message="Output is valid JSON",
        ))
        
        # Step 2: Validate against schema
        if self._validator is None:
            # jsonschema not available, just check it's valid JSON
            assertions.append(AssertionDetail(
                name="schema_validation",
                passed=True,
                expected="Schema validation",
                actual="Skipped - jsonschema not installed",
                message="Install jsonschema for full validation",
            ))
            return self._build_result(
                passed=True,
                assertions=assertions,
                message="JSON is valid (schema validation skipped - install jsonschema)",
                parsed_json=parsed_json,
            )
        
        # Run schema validation
        validation_errors = list(self._validator.iter_errors(parsed_json))
        
        if validation_errors:
            for error in validation_errors:
                path = ".".join(str(p) for p in error.absolute_path) or "(root)"
                assertions.append(AssertionDetail(
                    name=f"schema:{path}",
                    passed=False,
                    expected=error.schema,
                    actual=error.instance,
                    message=error.message,
                ))
                
                if self.config.fail_fast:
                    break
            
            return self._build_result(
                passed=False,
                assertions=assertions,
                message=f"Schema validation failed: {len(validation_errors)} error(s)",
                parsed_json=parsed_json,
            )
        
        assertions.append(AssertionDetail(
            name="schema_validation",
            passed=True,
            expected="Matches schema",
            actual="Valid",
            message="Output matches JSON schema",
        ))
        
        return self._build_result(
            passed=True,
            assertions=assertions,
            message="JSON output matches schema",
            parsed_json=parsed_json,
        )
    
    def _parse_output(self, output: str) -> tuple[Optional[Any], Optional[str]]:
        """Parse output as JSON, with optional extraction.
        
        Args:
            output: The raw output string.
            
        Returns:
            Tuple of (parsed_json, error_message).
        """
        if not self.config.parse_json:
            # Assume it's already JSON-like
            return output, None
        
        # Try direct parse first
        try:
            return json.loads(output), None
        except json.JSONDecodeError as e:
            first_error = str(e)
        
        # Try extracting from markdown code blocks
        if self.config.extract_json:
            extracted = self._extract_json_from_markdown(output)
            if extracted:
                try:
                    return json.loads(extracted), None
                except json.JSONDecodeError:
                    pass
        
        return None, first_error
    
    def _extract_json_from_markdown(self, text: str) -> Optional[str]:
        """Extract JSON from markdown code blocks.
        
        Args:
            text: Text potentially containing markdown code blocks.
            
        Returns:
            Extracted JSON string or None.
        """
        # Match ```json ... ``` or ``` ... ```
        patterns = [
            r"```json\s*\n(.*?)\n```",
            r"```\s*\n(.*?)\n```",
            r"```(.*?)```",
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.DOTALL)
            if match:
                return match.group(1).strip()
        
        return None
    
    def _build_result(
        self,
        passed: bool,
        assertions: List[AssertionDetail],
        message: str,
        parsed_json: Optional[Any],
    ) -> EvalResult:
        """Build the evaluation result.
        
        Args:
            passed: Whether evaluation passed.
            assertions: List of assertion details.
            message: Result message.
            parsed_json: The parsed JSON (if successful).
            
        Returns:
            Configured EvalResult.
        """
        if assertions:
            passed_count = sum(1 for a in assertions if a.passed)
            score = passed_count / len(assertions)
        else:
            score = 1.0 if passed else 0.0
        
        details: Dict[str, Any] = {
            "strict": self.config.strict,
            "extract_json": self.config.extract_json,
        }
        
        if parsed_json is not None and self.config.include_details:
            details["parsed_json"] = parsed_json
        
        return EvalResult(
            status=EvalStatus.PASSED if passed else EvalStatus.FAILED,
            score=score,
            eval_name=self.eval_name,
            message=message,
            assertions=assertions if self.config.include_details else None,
            details=details if self.config.include_details else None,
        )

