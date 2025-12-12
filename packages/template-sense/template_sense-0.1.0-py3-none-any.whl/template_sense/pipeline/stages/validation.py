"""
ValidationStage: Validates pipeline inputs early.

This stage performs validation of file path and field dictionary before
any expensive operations are performed.
"""

import logging
from pathlib import Path

from template_sense.constants import SUPPORTED_FILE_EXTENSIONS
from template_sense.errors import FileValidationError, InvalidFieldDictionaryError
from template_sense.pipeline.stages.base import PipelineContext, PipelineStage

logger = logging.getLogger(__name__)


class ValidationStage(PipelineStage):
    """
    Stage 1: Validate pipeline inputs.

    Validates:
    - File path exists and has supported extension
    - Field dictionary is well-formed (non-empty dict with string keys/list values)

    Raises:
        FileValidationError: If file is invalid or not found
        InvalidFieldDictionaryError: If field dictionary is malformed
    """

    def execute(self, context: PipelineContext) -> PipelineContext:
        """Execute validation stage."""
        logger.info("Stage 1: Validating inputs...")

        # Validate file path
        self._validate_file_path(context.file_path)

        # Validate field dictionary and transform to internal format
        header_dict, column_dict = self._validate_field_dictionary(context.field_dictionary)

        # Populate internal dictionaries in context
        context.header_field_dictionary = header_dict
        context.column_field_dictionary = column_dict

        logger.debug(
            "Input validation passed: file=%s, headers=%d, columns=%d",
            context.file_path,
            len(header_dict),
            len(column_dict),
        )
        logger.info("Stage 1: Validation complete")

        return context

    def _validate_file_path(self, file_path: Path) -> None:
        """
        Validate file path.

        Args:
            file_path: Path to validate

        Raises:
            FileValidationError: If file is invalid or not found
        """
        # Check file exists
        if not file_path.exists():
            raise FileValidationError(
                reason=f"File not found: {file_path}",
                file_path=str(file_path),
            )

        # Check file extension
        if file_path.suffix.lower() not in SUPPORTED_FILE_EXTENSIONS:
            raise FileValidationError(
                reason=f"Unsupported file format: {file_path.suffix}. "
                f"Supported formats: {SUPPORTED_FILE_EXTENSIONS}",
                file_path=str(file_path),
            )

    def _validate_field_dictionary(
        self, field_dictionary: dict[str, dict[str, str]]
    ) -> tuple[dict[str, list[str]], dict[str, list[str]]]:
        """
        Validate structured field dictionary and transform to internal format.

        Args:
            field_dictionary: Structured dict with 'headers' and 'columns' sections

        Returns:
            Tuple of (header_dict, column_dict) in dict[str, list[str]] format

        Raises:
            InvalidFieldDictionaryError: If dictionary is malformed
        """
        # 1. Type check
        if not isinstance(field_dictionary, dict):
            raise InvalidFieldDictionaryError(
                reason="Field dictionary must be a dict",
                field_dictionary=field_dictionary,
            )

        # 2. Check for required keys
        if "headers" not in field_dictionary:
            raise InvalidFieldDictionaryError(
                reason="Field dictionary must contain 'headers' key",
                field_dictionary=field_dictionary,
            )
        if "columns" not in field_dictionary:
            raise InvalidFieldDictionaryError(
                reason="Field dictionary must contain 'columns' key",
                field_dictionary=field_dictionary,
            )

        # 3. Validate headers section
        headers = field_dictionary["headers"]
        if not isinstance(headers, dict):
            raise InvalidFieldDictionaryError(
                reason="'headers' must be a dict[str, str]",
                field_dictionary=field_dictionary,
            )

        for key, value in headers.items():
            if not isinstance(key, str):
                raise InvalidFieldDictionaryError(
                    reason=f"Header key must be string, got {type(key).__name__}",
                    field_dictionary=field_dictionary,
                )
            if not isinstance(value, str):
                raise InvalidFieldDictionaryError(
                    reason=f"Header value for '{key}' must be string, got {type(value).__name__}",
                    field_dictionary=field_dictionary,
                )

        # 4. Validate columns section
        columns = field_dictionary["columns"]
        if not isinstance(columns, dict):
            raise InvalidFieldDictionaryError(
                reason="'columns' must be a dict[str, str]",
                field_dictionary=field_dictionary,
            )

        for key, value in columns.items():
            if not isinstance(key, str):
                raise InvalidFieldDictionaryError(
                    reason=f"Column key must be string, got {type(key).__name__}",
                    field_dictionary=field_dictionary,
                )
            if not isinstance(value, str):
                raise InvalidFieldDictionaryError(
                    reason=f"Column value for '{key}' must be string, got {type(value).__name__}",
                    field_dictionary=field_dictionary,
                )

        # 5. Transform to internal format: dict[str, list[str]]
        # Wrap single string values in lists for compatibility with fuzzy matching
        header_dict = {k: [v] for k, v in headers.items()}
        column_dict = {k: [v] for k, v in columns.items()}

        logger.debug(
            "Field dictionary validated: %d headers, %d columns (empty sections allowed)",
            len(header_dict),
            len(column_dict),
        )

        return header_dict, column_dict


__all__ = ["ValidationStage"]
