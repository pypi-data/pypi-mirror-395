"""
File type detection and validation module for Template Sense.

This module validates file inputs before they enter the extraction pipeline.
Currently supports Excel files (.xlsx, .xls) only.

Functions:
    detect_file_type: Detect the file type based on extension and MIME type
    is_excel_file: Check if a file is an Excel file
    validate_supported_file: Validate that a file is supported and readable

Usage Example:
    from pathlib import Path
    from template_sense.file_validation import validate_supported_file

    file_path = Path("template.xlsx")
    validate_supported_file(file_path)  # Raises exception if invalid
"""

from pathlib import Path

from openpyxl import load_workbook

from template_sense.constants import SUPPORTED_FILE_EXTENSIONS
from template_sense.errors import FileValidationError, UnsupportedFileTypeError

# Supported file types
SUPPORTED_EXCEL_EXTENSIONS = set(
    SUPPORTED_FILE_EXTENSIONS
)  # Convert to set for fast membership testing
SUPPORTED_MIME_TYPES = {
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",  # .xlsx
    "application/vnd.ms-excel",  # .xls
}


def detect_file_type(path: Path) -> str:
    """
    Detect the file type based on file extension.

    Args:
        path: Path to the file to detect

    Returns:
        The file extension (e.g., ".xlsx", ".xls", ".pdf", ".csv")

    Raises:
        FileValidationError: If the file path is invalid or has no extension

    Example:
        >>> from pathlib import Path
        >>> detect_file_type(Path("template.xlsx"))
        '.xlsx'
    """
    if not isinstance(path, Path):
        path = Path(path)

    # Check if file has an extension
    if not path.suffix:
        raise FileValidationError(
            reason="File has no extension",
            file_path=str(path),
        )

    # Return lowercase extension for consistency
    return path.suffix.lower()


def is_excel_file(path: Path) -> bool:
    """
    Check if a file is an Excel file based on extension.

    This function performs a quick check based on file extension only.
    For full validation including readability, use validate_supported_file().

    Args:
        path: Path to the file to check

    Returns:
        True if the file has an Excel extension (.xlsx or .xls), False otherwise

    Example:
        >>> from pathlib import Path
        >>> is_excel_file(Path("template.xlsx"))
        True
        >>> is_excel_file(Path("document.pdf"))
        False
    """
    if not isinstance(path, Path):
        path = Path(path)

    extension = path.suffix.lower()
    return extension in SUPPORTED_EXCEL_EXTENSIONS


def validate_supported_file(path: Path) -> None:
    """
    Validate that a file is supported and readable.

    Performs comprehensive validation:
    1. Checks if file exists
    2. Checks if path points to a file (not directory)
    3. Validates file extension is supported
    4. Attempts to open the file with openpyxl to verify it's readable

    Args:
        path: Path to the file to validate

    Raises:
        FileValidationError: If file doesn't exist, is not a file, or is not readable
        UnsupportedFileTypeError: If file type is not supported

    Example:
        >>> from pathlib import Path
        >>> validate_supported_file(Path("template.xlsx"))
        >>> # No exception raised - file is valid
        >>>
        >>> validate_supported_file(Path("document.pdf"))
        >>> # Raises UnsupportedFileTypeError
    """
    if not isinstance(path, Path):
        path = Path(path)

    # 1. Check if file exists
    if not path.exists():
        raise FileValidationError(
            reason="File does not exist",
            file_path=str(path),
        )

    # 2. Check if path is a file (not a directory)
    if not path.is_file():
        raise FileValidationError(
            reason="Path is not a file",
            file_path=str(path),
        )

    # 3. Detect and validate file type
    file_extension = detect_file_type(path)

    if file_extension not in SUPPORTED_EXCEL_EXTENSIONS:
        raise UnsupportedFileTypeError(
            file_extension=file_extension,
            supported_types=list(SUPPORTED_EXCEL_EXTENSIONS),
        )

    # 4. Attempt to open the file with openpyxl to verify it's readable
    try:
        # Use data_only=True to get computed values instead of formulas
        # Use read_only=True for validation to avoid loading entire file
        workbook = load_workbook(filename=path, read_only=True, data_only=True)
        workbook.close()
    except FileNotFoundError as e:
        # This should not happen as we checked existence above, but handle it
        raise FileValidationError(
            reason="File not found during validation",
            file_path=str(path),
        ) from e
    except PermissionError as e:
        raise FileValidationError(
            reason="Permission denied - cannot read file",
            file_path=str(path),
        ) from e
    except Exception as e:
        # Catch any other errors from openpyxl (corrupt file, wrong format, etc.)
        raise FileValidationError(
            reason=f"File is not a valid Excel file or is corrupted: {str(e)}",
            file_path=str(path),
        ) from e


__all__ = [
    "detect_file_type",
    "is_excel_file",
    "validate_supported_file",
    "SUPPORTED_EXCEL_EXTENSIONS",
]
