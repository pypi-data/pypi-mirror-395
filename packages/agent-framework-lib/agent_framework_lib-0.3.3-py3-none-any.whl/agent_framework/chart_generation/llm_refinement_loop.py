"""
LLM refinement loop implementation for chart generation.

This module provides iterative refinement of Chart.js definitions using LLM feedback
to address validation errors and improve chart quality.
"""

import json
import logging
from typing import Any, Dict, List, Optional

from ..model_clients import client_factory
from .interfaces import LLMRefinementLoop
from .models import ValidationError, ValidationResult, RefinementResult

logger = logging.getLogger(__name__)


class ChartJsLLMRefinementLoop(LLMRefinementLoop):
    """
    LLM-based refinement loop for Chart.js definitions.
    
    Uses the existing Model Client Factory to iteratively improve chart definitions
    by providing validation errors as feedback to the LLM.
    """
    
    def __init__(self, model_name: Optional[str] = None):
        """
        Initialize the refinement loop.
        
        Args:
            model_name: Optional specific model to use. If None, uses default model.
        """
        self.model_name = model_name
        self._client = None
    
    async def refine_definition(
        self,
        original_description: str,
        current_definition: Dict[str, Any],
        validation_errors: List[ValidationError],
        max_loops: int = 3
    ) -> RefinementResult:
        """
        Refine a chart definition using LLM feedback.
        
        Args:
            original_description: Original user description
            current_definition: Current chart definition
            validation_errors: Errors to address
            max_loops: Maximum refinement iterations
            
        Returns:
            RefinementResult with improved definition
        """
        logger.info(f"Starting LLM refinement loop with {len(validation_errors)} errors, max loops: {max_loops}")
        
        refined_definition = current_definition.copy()
        iterations_used = 0
        improvement_achieved = False
        final_validation_result = ValidationResult(
            is_valid=False,
            errors=validation_errors,
            warnings=[]
        )
        
        try:
            # Initialize LLM client
            await self._initialize_client()
            
            for iteration in range(max_loops):
                iterations_used = iteration + 1
                logger.info(f"Refinement iteration {iterations_used}/{max_loops}")
                
                # Generate refinement prompt
                prompt = self._create_refinement_prompt(
                    original_description,
                    refined_definition,
                    validation_errors
                )
                
                # Get LLM response
                try:
                    response = await self._call_llm(prompt)
                    new_definition = self._parse_llm_response(response)
                    
                    if new_definition:
                        # Check if we made improvements
                        if self._has_structural_improvements(refined_definition, new_definition):
                            refined_definition = new_definition
                            improvement_achieved = True
                            logger.info(f"Iteration {iterations_used}: Structural improvements detected")
                        else:
                            logger.warning(f"Iteration {iterations_used}: No structural improvements detected")
                    else:
                        logger.warning(f"Iteration {iterations_used}: Failed to parse LLM response")
                        
                except Exception as e:
                    logger.error(f"Iteration {iterations_used}: LLM call failed: {e}")
                    continue
                
                # We'll let the validation happen outside this loop
                # since we don't have direct access to the validation engine here
                break
                
        except Exception as e:
            logger.error(f"Refinement loop failed: {e}")
            # Return original definition if refinement fails completely
            refined_definition = current_definition
        
        # Create final result
        final_validation_result = ValidationResult(
            is_valid=len(validation_errors) == 0,
            errors=validation_errors,
            warnings=[]
        )
        
        result = RefinementResult(
            refined_definition=refined_definition,
            iterations_used=iterations_used,
            final_validation_result=final_validation_result,
            improvement_achieved=improvement_achieved
        )
        
        logger.info(f"Refinement loop completed: {iterations_used} iterations, improvement: {improvement_achieved}")
        return result
    
    async def _initialize_client(self) -> None:
        """Initialize the LLM client using the model client factory."""
        if self._client is None:
            try:
                self._client = client_factory.create_client(model_name=self.model_name)
                logger.debug(f"Initialized LLM client for model: {self.model_name or 'default'}")
            except Exception as e:
                logger.error(f"Failed to initialize LLM client: {e}")
                raise RuntimeError(f"Could not initialize LLM client: {e}")
    
    def _create_refinement_prompt(
        self,
        original_description: str,
        current_definition: Dict[str, Any],
        validation_errors: List[ValidationError]
    ) -> str:
        """
        Create a detailed prompt for LLM refinement.
        
        Args:
            original_description: Original user description
            current_definition: Current chart definition
            validation_errors: Validation errors to fix
            
        Returns:
            Formatted prompt string
        """
        # Format validation errors for the prompt
        error_descriptions = []
        for error in validation_errors:
            error_desc = f"- Field '{error.field_path}': {error.error_message}"
            if error.suggested_fix:
                error_desc += f" (Suggested fix: {error.suggested_fix})"
            error_descriptions.append(error_desc)
        
        errors_text = "\n".join(error_descriptions)
        
        prompt = f"""You are a Chart.js expert helping to fix validation errors in a chart definition.

Original user request: "{original_description}"

Current Chart.js definition:
```json
{json.dumps(current_definition, indent=2)}
```

Validation errors that need to be fixed:
{errors_text}

Please provide a corrected Chart.js definition that:
1. Addresses all the validation errors listed above
2. Maintains the original intent from the user's description
3. Follows Chart.js 4.0+ specifications
4. Is a complete, valid Chart.js configuration

Respond with ONLY the corrected JSON definition, no additional text or explanation.
The response must be valid JSON that can be parsed directly."""

        return prompt
    
    async def _call_llm(self, prompt: str) -> str:
        """
        Call the LLM with the refinement prompt.
        
        Args:
            prompt: The prompt to send to the LLM
            
        Returns:
            LLM response text
        """
        if not self._client:
            raise RuntimeError("LLM client not initialized")
        
        try:
            # Create messages for the LLM
            messages = [
                {
                    "role": "system",
                    "content": "You are a Chart.js expert. Respond only with valid JSON chart definitions."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
            
            # Call the LLM using the client
            # Note: The exact API depends on the AutoGen client interface
            # This is a simplified version that should work with most clients
            response = await self._client.create(messages=messages)
            
            # Extract content from response
            if hasattr(response, 'choices') and response.choices:
                return response.choices[0].message.content
            elif hasattr(response, 'content'):
                return response.content
            else:
                # Fallback for different response formats
                return str(response)
                
        except Exception as e:
            logger.error(f"LLM call failed: {e}")
            raise
    
    def _parse_llm_response(self, response: str) -> Optional[Dict[str, Any]]:
        """
        Parse the LLM response to extract the chart definition.
        
        Args:
            response: Raw LLM response
            
        Returns:
            Parsed chart definition or None if parsing failed
        """
        try:
            # Clean up the response - remove markdown code blocks if present
            cleaned_response = response.strip()
            if cleaned_response.startswith("```json"):
                cleaned_response = cleaned_response[7:]
            if cleaned_response.startswith("```"):
                cleaned_response = cleaned_response[3:]
            if cleaned_response.endswith("```"):
                cleaned_response = cleaned_response[:-3]
            
            cleaned_response = cleaned_response.strip()
            
            # Parse JSON
            definition = json.loads(cleaned_response)
            
            # Basic validation that it looks like a chart definition
            if isinstance(definition, dict) and "type" in definition:
                logger.debug("Successfully parsed LLM response as chart definition")
                return definition
            else:
                logger.warning("Parsed JSON doesn't look like a chart definition")
                return None
                
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse LLM response as JSON: {e}")
            logger.debug(f"Raw response: {response}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error parsing LLM response: {e}")
            return None
    
    def _has_structural_improvements(
        self,
        old_definition: Dict[str, Any],
        new_definition: Dict[str, Any]
    ) -> bool:
        """
        Check if the new definition has structural improvements over the old one.
        
        Args:
            old_definition: Previous chart definition
            new_definition: New chart definition
            
        Returns:
            True if improvements are detected
        """
        try:
            # Check if basic structure is more complete
            old_keys = set(old_definition.keys())
            new_keys = set(new_definition.keys())
            
            # New definition has more top-level keys
            if len(new_keys) > len(old_keys):
                return True
            
            # Check data structure improvements
            old_data = old_definition.get("data", {})
            new_data = new_definition.get("data", {})
            
            if isinstance(old_data, dict) and isinstance(new_data, dict):
                # More datasets or better data structure
                old_datasets = old_data.get("datasets", [])
                new_datasets = new_data.get("datasets", [])
                
                if len(new_datasets) > len(old_datasets):
                    return True
                
                # Check if labels were added
                if "labels" not in old_data and "labels" in new_data:
                    return True
            
            # Check if options were improved
            old_options = old_definition.get("options", {})
            new_options = new_definition.get("options", {})
            
            if isinstance(new_options, dict) and len(new_options) > len(old_options):
                return True
            
            # If definitions are significantly different, consider it an improvement
            old_str = json.dumps(old_definition, sort_keys=True)
            new_str = json.dumps(new_definition, sort_keys=True)
            
            if old_str != new_str:
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Error checking structural improvements: {e}")
            # If we can't determine, assume there might be improvements
            return True


class RefinementLoopWithValidation:
    """
    Wrapper that combines refinement loop with validation for complete refinement process.
    
    This class orchestrates the refinement process by combining the LLM refinement loop
    with validation to provide complete iterative improvement.
    """
    
    def __init__(
        self,
        refinement_loop: LLMRefinementLoop,
        validation_engine,
        model_name: Optional[str] = None
    ):
        """
        Initialize the refinement loop with validation.
        
        Args:
            refinement_loop: The LLM refinement loop instance
            validation_engine: The validation engine instance
            model_name: Optional model name for LLM calls
        """
        self.refinement_loop = refinement_loop
        self.validation_engine = validation_engine
        self.model_name = model_name
    
    async def refine_with_validation(
        self,
        original_description: str,
        current_definition: Dict[str, Any],
        max_loops: int = 3
    ) -> RefinementResult:
        """
        Perform complete refinement with validation feedback loop.
        
        Args:
            original_description: Original user description
            current_definition: Current chart definition
            max_loops: Maximum refinement iterations
            
        Returns:
            RefinementResult with final refined definition
        """
        logger.info(f"Starting refinement with validation, max loops: {max_loops}")
        
        refined_definition = current_definition.copy()
        total_iterations = 0
        improvement_achieved = False
        
        for loop_iteration in range(max_loops):
            # Validate current definition
            validation_result = self.validation_engine.validate_definition(refined_definition)
            
            if validation_result.is_valid:
                logger.info(f"Validation passed after {loop_iteration} refinement loops")
                break
            
            logger.info(f"Refinement loop {loop_iteration + 1}: {len(validation_result.errors)} validation errors")
            
            # Refine using LLM
            refinement_result = await self.refinement_loop.refine_definition(
                original_description=original_description,
                current_definition=refined_definition,
                validation_errors=validation_result.errors,
                max_loops=1  # Single iteration per validation loop
            )
            
            total_iterations += refinement_result.iterations_used
            
            if refinement_result.improvement_achieved:
                refined_definition = refinement_result.refined_definition
                improvement_achieved = True
                logger.info(f"Improvements achieved in loop {loop_iteration + 1}")
            else:
                logger.warning(f"No improvements in loop {loop_iteration + 1}, stopping refinement")
                break
        
        # Final validation
        final_validation_result = self.validation_engine.validate_definition(refined_definition)
        
        result = RefinementResult(
            refined_definition=refined_definition,
            iterations_used=total_iterations,
            final_validation_result=final_validation_result,
            improvement_achieved=improvement_achieved
        )
        
        logger.info(f"Refinement with validation completed: {total_iterations} total iterations, "
                   f"final validation: {'PASSED' if final_validation_result.is_valid else 'FAILED'}")
        
        return result