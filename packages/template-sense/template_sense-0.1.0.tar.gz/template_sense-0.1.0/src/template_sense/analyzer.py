"""
Public API entry point for template-sense package.

This module provides the official interface that Tako's engineering team
will use to extract structured metadata from Excel invoice templates.
"""

import logging
from pathlib import Path
from typing import Any

from template_sense.ai_providers.config import AIConfig
from template_sense.errors import (
    AIProviderError,
    ExtractionError,
    FileValidationError,
    InvalidFieldDictionaryError,
    UnsupportedFileTypeError,
)
from template_sense.pipeline.extraction_pipeline import run_extraction_pipeline

logger = logging.getLogger(__name__)

# Type alias for flexible path input
PathLike = str | Path


def extract_template_structure(
    file_path: PathLike,
    field_dictionary: dict[str, dict[str, str]],
    ai_config: AIConfig | None = None,
) -> dict[str, Any]:
    """
    Extract structured metadata from Excel invoice template.

    This is the official entrypoint for the template-sense package.
    Validates inputs, invokes the extraction pipeline, and returns
    normalized JSON-serializable results.

    Args:
        file_path: Path to Excel file (.xlsx or .xls). Can be string or Path object.
        field_dictionary: Structured canonical field dictionary with separate
                         "headers" and "columns" sections. For example:
                         {
                             "headers": {
                                 "invoice_number": "Invoice number",
                                 "shipper": "Shipper",
                             },
                             "columns": {
                                 "product_name": "Product name",
                                 "quantity": "Quantity",
                             }
                         }
        ai_config: Optional AI provider configuration. If not provided, defaults
                  to environment variable configuration (TEMPLATE_SENSE_AI_PROVIDER,
                  OPENAI_API_KEY or ANTHROPIC_API_KEY).

    Returns:
        dict with three keys:
        - normalized_output: Extracted template structure containing:
          - header_fields: List of identified header fields with canonical mappings
          - table_columns: List of identified table columns with canonical mappings
          - line_items: List of extracted line item rows (if applicable)
        - recovery_events: List of recovery/warning events that occurred during
                          extraction (e.g., low confidence scores, translation
                          failures, fuzzy matching issues)
        - metadata: Pipeline execution metadata including:
          - sheet_name: Name of the Excel sheet analyzed

    Raises:
        FileValidationError: File doesn't exist, is unreadable, or has invalid format
        InvalidFieldDictionaryError: Field dictionary has invalid structure
        ExtractionError: Pipeline extraction failures (e.g., no sheets found,
                        no extractable data)
        AIProviderError: AI provider failures (e.g., API errors, authentication issues)

    Example:
        >>> from template_sense.analyzer import extract_template_structure
        >>> field_dict = {
        ...     "headers": {
        ...         "invoice_number": "Invoice number",
        ...         "shipper": "Shipper",
        ...         "invoice_date": "Invoice date",
        ...     },
        ...     "columns": {
        ...         "product_name": "Product name",
        ...         "quantity": "Quantity",
        ...         "price": "Price",
        ...     }
        ... }
        >>> result = extract_template_structure("invoice.xlsx", field_dict)
        >>> print(result["normalized_output"]["headers"]["matched"])
        [
            {
                "canonical_key": "invoice_number",
                "original_label": "請求書番号",
                "translated_label": "Invoice Number",
                "value": "INV-12345",
                "location": {"row": 2, "col": 1}
            },
            ...
        ]
    """
    logger.info(
        "Starting template structure extraction for file: %s",
        file_path,
    )

    # Normalize path input to Path object
    path = Path(file_path) if isinstance(file_path, str) else file_path

    try:
        # Invoke extraction pipeline
        # Pipeline handles all validation, extraction, AI analysis, and output building
        result = run_extraction_pipeline(
            file_path=path,
            field_dictionary=field_dictionary,
            ai_config=ai_config,
        )

        logger.info(
            "Template structure extraction completed successfully for file: %s",
            file_path,
        )

        return result

    except (
        FileValidationError,
        UnsupportedFileTypeError,
        InvalidFieldDictionaryError,
        ExtractionError,
        AIProviderError,
    ) as e:
        # Re-raise known errors unchanged
        logger.error(
            "Template structure extraction failed for file %s: %s",
            file_path,
            str(e),
        )
        raise

    except Exception as e:
        # Wrap unexpected exceptions in ExtractionError
        logger.error(
            "Unexpected error during template structure extraction for file %s: %s",
            file_path,
            str(e),
        )
        raise ExtractionError(
            extraction_type="template_analysis",
            reason=f"Unexpected error during template analysis: {str(e)}",
        ) from e
