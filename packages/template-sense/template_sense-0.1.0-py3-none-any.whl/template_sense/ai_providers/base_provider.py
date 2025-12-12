"""
Base AI provider implementation for Template Sense.

This module provides the base class that implements shared functionality
across all AI provider implementations (OpenAI, Anthropic, etc.). It follows
the Template Method pattern, where common logic is implemented in the base
class and provider-specific operations are delegated to abstract methods.

The BaseAIProvider eliminates code duplication by providing:
- Shared prompt building logic
- Common context validation
- Unified response parsing and validation
- Consolidated error handling

Classes:
    BaseAIProvider: Abstract base class with shared provider logic
"""

import json
import logging
from abc import abstractmethod
from typing import Any

from template_sense.ai_providers.interface import AIProvider
from template_sense.errors import AIProviderError

logger = logging.getLogger(__name__)


class BaseAIProvider(AIProvider):
    """
    Base implementation of AIProvider with shared logic.

    This class implements the Template Method pattern to provide common
    functionality across all AI providers. Provider-specific operations
    (API calls) are delegated to abstract methods that subclasses must implement.

    Shared functionality includes:
    - Prompt building for classification and translation
    - Context validation
    - JSON response parsing and validation
    - Error handling and exception mapping

    Subclasses must implement:
    - _call_classify_api(): Provider-specific classification API call
    - _call_translate_api(): Provider-specific translation API call
    - provider_name property: Provider identifier
    - model property: Model name

    Example:
        >>> class OpenAIProvider(BaseAIProvider):
        ...     def _call_classify_api(self, system, user):
        ...         # OpenAI-specific API call
        ...         return response.choices[0].message.content
    """

    def classify_fields(self, payload: dict[str, Any], context: str = "headers") -> dict[str, Any]:
        """
        Classify header fields and table columns using AI.

        This template method orchestrates the classification process:
        1. Validates the context parameter
        2. Builds context-aware prompts
        3. Calls provider-specific API (delegated to subclass)
        4. Parses and validates the response

        Args:
            payload: AI payload dict from build_ai_payload()
            context: Classification context - "headers", "columns", or "line_items"

        Returns:
            Dict with classification results (structure depends on context)

        Raises:
            AIProviderError: On API errors, timeouts, or invalid responses
            ValueError: If context is not a supported value
        """
        # Validate context
        self._validate_context(context)

        try:
            # Build context-aware prompts (shared logic)
            system_message = self._build_system_prompt(context)
            user_message = self._build_user_prompt(payload, context)

            logger.debug(
                "Sending classify_fields request (provider=%s, model=%s, context=%s)",
                self.provider_name,
                self.model,
                context,
            )

            # Call provider-specific API (delegated to subclass)
            response_text = self._call_classify_api(system_message, user_message)

            # Parse and validate response (shared logic)
            return self._parse_and_validate_response(response_text, context, "classify_fields")

        except AIProviderError:
            # Re-raise our own errors
            raise
        except ValueError:
            # Re-raise validation errors
            raise
        except Exception as e:
            # Wrap provider-specific exceptions
            raise self._wrap_api_error(e, "classify_fields") from e

    def translate_text(self, text: str, source_lang: str, target_lang: str = "en") -> str:
        """
        Translate text using AI.

        This template method orchestrates the translation process:
        1. Builds translation prompt
        2. Calls provider-specific API (delegated to subclass)
        3. Validates and returns the response

        Args:
            text: Text to translate
            source_lang: Source language code (e.g., "ja", "zh")
            target_lang: Target language code (default: "en")

        Returns:
            Translated text

        Raises:
            AIProviderError: On API errors, timeouts, or invalid responses
        """
        try:
            # Build translation prompt (shared logic)
            system_message = (
                f"You are a professional translator. Translate the given text "
                f"from {source_lang} to {target_lang}. "
                f"Return only the translated text, nothing else."
            )
            user_message = text

            logger.debug(
                "Sending translate_text request (provider=%s, model=%s, %s→%s)",
                self.provider_name,
                self.model,
                source_lang,
                target_lang,
            )

            # Call provider-specific API (delegated to subclass)
            translated = self._call_translate_api(system_message, user_message)

            if not translated:
                raise AIProviderError(
                    provider_name=self.provider_name,
                    error_details="Empty translation response from API",
                    request_type="translate_text",
                )

            logger.debug("Successfully translated text")
            return translated.strip()

        except AIProviderError:
            # Re-raise our own errors
            raise
        except Exception as e:
            # Wrap provider-specific exceptions
            raise self._wrap_api_error(e, "translate_text") from e

    def generate_text(
        self,
        prompt: str,
        system_message: str | None = None,
        max_tokens: int = 150,
        temperature: float = 0.0,
        json_mode: bool = True,
    ) -> str:
        """
        Generate text response using AI.

        This template method orchestrates the text generation process:
        1. Validates the prompt
        2. Calls provider-specific API (delegated to subclass)
        3. Validates and returns the response

        Args:
            prompt: The user prompt/question to send to the AI
            system_message: Optional system instruction to guide behavior
            max_tokens: Maximum tokens in response (default: 150)
            temperature: Sampling temperature - 0.0 for deterministic (default: 0.0)
            json_mode: Whether to request JSON-formatted response (default: True)

        Returns:
            Generated text response from the AI provider

        Raises:
            AIProviderError: On API errors, timeouts, or invalid responses
            ValueError: If prompt is empty or invalid
        """
        # Validate prompt
        if not prompt or not prompt.strip():
            raise ValueError("Prompt cannot be empty")

        try:
            logger.debug(
                "Sending generate_text request (provider=%s, model=%s)",
                self.provider_name,
                self.model,
            )

            # Call provider-specific API (delegated to subclass)
            response_text = self._call_generate_api(
                prompt=prompt,
                system_message=system_message,
                max_tokens=max_tokens,
                temperature=temperature,
                json_mode=json_mode,
            )

            if not response_text:
                raise AIProviderError(
                    provider_name=self.provider_name,
                    error_details="Empty response from API",
                    request_type="generate_text",
                )

            logger.debug("Successfully generated text response")
            return response_text

        except AIProviderError:
            # Re-raise our own errors
            raise
        except ValueError:
            # Re-raise validation errors
            raise
        except Exception as e:
            # Wrap provider-specific exceptions
            raise self._wrap_api_error(e, "generate_text") from e

    @abstractmethod
    def _call_classify_api(self, system_message: str, user_message: str) -> str:
        """
        Execute provider-specific classification API call.

        Subclasses must implement this method to call their specific API
        (OpenAI, Anthropic, etc.) and return the raw response text.

        Args:
            system_message: System prompt for classification
            user_message: User prompt with payload data

        Returns:
            Raw response text from the API

        Raises:
            Provider-specific exceptions (will be wrapped by BaseAIProvider)
        """
        raise NotImplementedError

    @abstractmethod
    def _call_translate_api(self, system_message: str, user_message: str) -> str:
        """
        Execute provider-specific translation API call.

        Subclasses must implement this method to call their specific API
        (OpenAI, Anthropic, etc.) and return the raw response text.

        Args:
            system_message: System prompt for translation
            user_message: Text to translate

        Returns:
            Translated text from the API

        Raises:
            Provider-specific exceptions (will be wrapped by BaseAIProvider)
        """
        raise NotImplementedError

    @abstractmethod
    def _call_generate_api(
        self,
        prompt: str,
        system_message: str | None,
        max_tokens: int,
        temperature: float,
        json_mode: bool,
    ) -> str:
        """
        Execute provider-specific text generation API call.

        Subclasses must implement this method to call their specific API
        (OpenAI, Anthropic, etc.) and return the raw response text.

        Args:
            prompt: User prompt/question
            system_message: Optional system instruction
            max_tokens: Maximum tokens in response
            temperature: Sampling temperature (0.0-1.0)
            json_mode: Whether to request JSON-formatted response

        Returns:
            Generated text from the API

        Raises:
            Provider-specific exceptions (will be wrapped by BaseAIProvider)
        """
        raise NotImplementedError

    def _validate_context(self, context: str) -> None:
        """
        Validate classification context parameter.

        Args:
            context: Context to validate

        Raises:
            ValueError: If context is not a supported value
        """
        if context not in ["headers", "columns", "line_items"]:
            raise ValueError(
                f"Invalid context: {context}. Must be 'headers', 'columns', or 'line_items'"
            )

    def _build_system_prompt(self, context: str) -> str:
        """
        Build context-aware system prompt.

        Args:
            context: Classification context

        Returns:
            System prompt string tailored to the context
        """
        if context == "headers":
            return (
                "You are a field classification assistant for invoice templates. "
                "Analyze the provided header fields and classify each field "
                "semantically based on common invoice terminology.\n\n"
                "PATTERN DETECTION:\n"
                "1. Multi-cell patterns: Label in one cell, value in adjacent cell\n"
                "   - Check adjacent_cells to find related values\n"
                "   - Common patterns: label on left, value on right (or above/below)\n"
                '   - Example: "Invoice:" in col 1, "12345" in col 3 (right_2)\n'
                "2. Same-cell patterns: Label and value in same cell with delimiter\n"
                '   - Common delimiters: ":", "-", "=", "|"\n'
                '   - Example: "Invoice Number: INV-12345"\n\n'
                "When you detect these patterns, populate both raw_label and raw_value fields. "
                "Set label_col_offset and value_col_offset to indicate where label/value are "
                "relative to the main cell (0 = same cell, positive = cells to the right).\n\n"
                "Return your response as valid JSON matching this exact schema:\n"
                "{\n"
                '  "headers": [\n'
                "    {\n"
                '      "raw_label": "Invoice Number",  // The label text (or null)\n'
                '      "raw_value": "INV-12345",       // The value text (or null)\n'
                '      "block_index": 0,               // Header block index (integer)\n'
                '      "row_index": 1,                 // Row position (integer)\n'
                '      "col_index": 1,                 // Column position (integer)\n'
                '      "label_col_offset": 0,          // Offset from main cell to label (optional, default 0)\n'
                '      "value_col_offset": 2,          // Offset from main cell to value (optional, default 0)\n'
                '      "pattern_type": "multi_cell",   // "multi_cell", "same_cell", or null (optional)\n'
                '      "model_confidence": 0.95        // Confidence 0.0-1.0 (optional)\n'
                "    }\n"
                "  ]\n"
                "}\n\n"
                "Required fields: raw_label, raw_value, block_index, row_index, col_index.\n"
                "Optional fields: label_col_offset, value_col_offset, pattern_type, model_confidence."
            )
        if context == "columns":
            return (
                "You are a table column classification assistant for invoice templates. "
                "Analyze the provided table columns and classify each column "
                "semantically based on common invoice table structures.\n\n"
                "Return your response as valid JSON matching this exact schema:\n"
                "{\n"
                '  "columns": [\n'
                "    {\n"
                '      "raw_label": "Item Code",        // Column header text (or null)\n'
                '      "raw_position": 0,               // Column position in table (integer)\n'
                '      "table_block_index": 0,          // Table block index (integer)\n'
                '      "row_index": 5,                  // Header row position (integer)\n'
                '      "col_index": 2,                  // Column position in sheet (integer)\n'
                '      "sample_values": ["A", "B"],     // Sample values from column (array)\n'
                '      "model_confidence": 0.95         // Confidence 0.0-1.0 (optional)\n'
                "    }\n"
                "  ]\n"
                "}\n\n"
                "All fields except model_confidence are required. sample_values must be an array."
            )
        if context == "line_items":
            return (
                "You are a line item extraction assistant for invoice templates. "
                "Analyze the provided table rows and extract individual line items.\n\n"
                "Return your response as valid JSON matching this exact schema:\n"
                "{\n"
                '  "line_items": [\n'
                "    {\n"
                '      "table_index": 0,                // Table index (integer)\n'
                '      "row_index": 6,                  // Row position (integer)\n'
                '      "is_subtotal": false,            // True if subtotal row (boolean)\n'
                '      "columns": {"item": "Widget"},   // Column values (object)\n'
                '      "model_confidence": 0.90         // Confidence 0.0-1.0 (optional)\n'
                "    }\n"
                "  ]\n"
                "}\n\n"
                "All fields except model_confidence are required."
            )
        return ""

    def _build_user_prompt(self, payload: dict[str, Any], context: str) -> str:
        """
        Build context-aware user prompt.

        Args:
            payload: AI payload data
            context: Classification context

        Returns:
            User prompt string tailored to the context
        """
        context_descriptions = {
            "headers": "invoice template header fields",
            "columns": "invoice table columns",
            "line_items": "invoice table line items",
        }

        description = context_descriptions.get(context, "invoice template fields")

        return (
            f"Please classify the following {description}:\n\n"
            f"{json.dumps(payload, indent=2)}\n\n"
            "Respond with a JSON object containing your classifications."
        )

    def _get_expected_response_key(self, context: str) -> str:
        """
        Get expected response key for context.

        Args:
            context: Classification context

        Returns:
            Expected top-level key in response JSON
        """
        mapping = {
            "headers": "headers",
            "columns": "columns",
            "line_items": "line_items",
        }
        return mapping[context]

    def _parse_and_validate_response(
        self, content: str, context: str, request_type: str
    ) -> dict[str, Any]:
        """
        Parse and validate JSON response from API.

        Args:
            content: Raw response text from API
            context: Classification context
            request_type: Type of request (for error messages)

        Returns:
            Parsed and validated JSON dict

        Raises:
            AIProviderError: If response is empty, invalid JSON, or missing expected key
        """
        if not content:
            raise AIProviderError(
                provider_name=self.provider_name,
                error_details="Empty response from API",
                request_type=request_type,
            )

        try:
            # Try parsing directly first
            result = json.loads(content)
            logger.debug("Successfully parsed JSON response")

            # Validate expected response key
            expected_key = self._get_expected_response_key(context)
            if expected_key not in result:
                raise AIProviderError(
                    provider_name=self.provider_name,
                    error_details=f"Response missing '{expected_key}' key for context '{context}'",
                    request_type=request_type,
                )

            return result
        except json.JSONDecodeError as e:
            # If direct parsing fails, try to extract JSON from text with preamble
            # (Anthropic sometimes adds text before the JSON)
            json_start = content.find("{")
            if json_start > 0:
                try:
                    result = json.loads(content[json_start:])
                    logger.debug("Successfully parsed JSON after stripping preamble")

                    # Validate expected response key
                    expected_key = self._get_expected_response_key(context)
                    if expected_key not in result:
                        raise AIProviderError(
                            provider_name=self.provider_name,
                            error_details=f"Response missing '{expected_key}' key for context '{context}'",
                            request_type=request_type,
                        )

                    return result
                except json.JSONDecodeError:
                    pass  # Fall through to original error

            raise AIProviderError(
                provider_name=self.provider_name,
                error_details=f"Invalid JSON in response: {str(e)}",
                request_type=request_type,
            ) from e

    def _wrap_api_error(self, e: Exception, request_type: str) -> AIProviderError:
        """
        Map provider-specific exceptions to AIProviderError.

        This method consolidates error handling across all providers by mapping
        common exception types (authentication, timeout, API errors) to our
        unified AIProviderError.

        Args:
            e: Exception from provider API
            request_type: Type of request (for error context)

        Returns:
            AIProviderError with appropriate details
        """
        # Check exception type by class name to avoid import issues
        exception_class_name = type(e).__name__

        # Authentication errors
        if exception_class_name == "AuthenticationError":
            return AIProviderError(
                provider_name=self.provider_name,
                error_details=f"Authentication failed: {str(e)}",
                request_type=request_type,
            )

        # Timeout errors
        if exception_class_name == "APITimeoutError":
            return AIProviderError(
                provider_name=self.provider_name,
                error_details=f"Request timed out: {str(e)}",
                request_type=request_type,
            )

        # API errors
        if exception_class_name == "APIError":
            return AIProviderError(
                provider_name=self.provider_name,
                error_details=f"API error: {str(e)}",
                request_type=request_type,
            )

        # Unexpected errors
        return AIProviderError(
            provider_name=self.provider_name,
            error_details=f"Unexpected error: {str(e)}",
            request_type=request_type,
        )


__all__ = ["BaseAIProvider"]
