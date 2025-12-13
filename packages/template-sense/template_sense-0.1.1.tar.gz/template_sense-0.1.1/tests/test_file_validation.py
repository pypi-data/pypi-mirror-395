"""
Unit tests for file_validation module.

Tests file type detection, validation, and error handling.
"""

from pathlib import Path

import pytest

from template_sense.errors import FileValidationError, UnsupportedFileTypeError
from template_sense.file_validation import (
    SUPPORTED_EXCEL_EXTENSIONS,
    detect_file_type,
    is_excel_file,
    validate_supported_file,
)

# Path to test fixtures
FIXTURES_DIR = Path(__file__).parent / "fixtures"


class TestDetectFileType:
    """Tests for detect_file_type() function."""

    def test_detect_xlsx_extension(self):
        """Test detection of .xlsx files."""
        path = Path("template.xlsx")
        assert detect_file_type(path) == ".xlsx"

    def test_detect_xls_extension(self):
        """Test detection of .xls files."""
        path = Path("template.xls")
        assert detect_file_type(path) == ".xls"

    def test_detect_csv_extension(self):
        """Test detection of .csv files."""
        path = Path("data.csv")
        assert detect_file_type(path) == ".csv"

    def test_detect_pdf_extension(self):
        """Test detection of .pdf files."""
        path = Path("document.pdf")
        assert detect_file_type(path) == ".pdf"

    def test_detect_uppercase_extension(self):
        """Test that uppercase extensions are normalized to lowercase."""
        path = Path("template.XLSX")
        assert detect_file_type(path) == ".xlsx"

    def test_detect_mixed_case_extension(self):
        """Test that mixed case extensions are normalized to lowercase."""
        path = Path("template.XlSx")
        assert detect_file_type(path) == ".xlsx"

    def test_no_extension_raises_error(self):
        """Test that files with no extension raise FileValidationError."""
        path = Path("no_extension_file")
        with pytest.raises(FileValidationError) as exc_info:
            detect_file_type(path)

        assert "File has no extension" in str(exc_info.value)
        assert exc_info.value.filename == "no_extension_file"

    def test_accepts_string_path(self):
        """Test that string paths are converted to Path objects."""
        result = detect_file_type("template.xlsx")
        assert result == ".xlsx"


class TestIsExcelFile:
    """Tests for is_excel_file() function."""

    def test_xlsx_is_excel_file(self):
        """Test that .xlsx files are recognized as Excel files."""
        path = Path("template.xlsx")
        assert is_excel_file(path) is True

    def test_xls_is_excel_file(self):
        """Test that .xls files are recognized as Excel files."""
        path = Path("template.xls")
        assert is_excel_file(path) is True

    def test_csv_is_not_excel_file(self):
        """Test that .csv files are not recognized as Excel files."""
        path = Path("data.csv")
        assert is_excel_file(path) is False

    def test_pdf_is_not_excel_file(self):
        """Test that .pdf files are not recognized as Excel files."""
        path = Path("document.pdf")
        assert is_excel_file(path) is False

    def test_txt_is_not_excel_file(self):
        """Test that .txt files are not recognized as Excel files."""
        path = Path("document.txt")
        assert is_excel_file(path) is False

    def test_uppercase_xlsx_is_excel_file(self):
        """Test that uppercase .XLSX extensions are recognized."""
        path = Path("template.XLSX")
        assert is_excel_file(path) is True

    def test_accepts_string_path(self):
        """Test that string paths are converted to Path objects."""
        assert is_excel_file("template.xlsx") is True
        assert is_excel_file("data.csv") is False


class TestValidateSupportedFile:
    """Tests for validate_supported_file() function."""

    def test_valid_xlsx_file(self):
        """Test that a valid .xlsx file passes validation."""
        path = FIXTURES_DIR / "valid_template.xlsx"
        # Should not raise any exception
        validate_supported_file(path)

    def test_nonexistent_file_raises_error(self):
        """Test that a non-existent file raises FileValidationError."""
        path = Path("nonexistent_file.xlsx")
        with pytest.raises(FileValidationError) as exc_info:
            validate_supported_file(path)

        assert "File does not exist" in str(exc_info.value)
        assert exc_info.value.filename == "nonexistent_file.xlsx"

    def test_directory_raises_error(self):
        """Test that a directory (not a file) raises FileValidationError."""
        path = FIXTURES_DIR  # This is a directory
        with pytest.raises(FileValidationError) as exc_info:
            validate_supported_file(path)

        assert "Path is not a file" in str(exc_info.value)

    def test_csv_file_raises_unsupported_error(self):
        """Test that a .csv file raises UnsupportedFileTypeError."""
        path = FIXTURES_DIR / "invalid_format.csv"
        with pytest.raises(UnsupportedFileTypeError) as exc_info:
            validate_supported_file(path)

        assert exc_info.value.file_extension == ".csv"
        assert ".xlsx" in str(exc_info.value)
        assert exc_info.value.supported_types == list(SUPPORTED_EXCEL_EXTENSIONS)

    def test_pdf_file_raises_unsupported_error(self):
        """Test that a .pdf file raises UnsupportedFileTypeError."""
        path = FIXTURES_DIR / "invalid_format.pdf"
        with pytest.raises(UnsupportedFileTypeError) as exc_info:
            validate_supported_file(path)

        assert exc_info.value.file_extension == ".pdf"

    def test_txt_file_raises_unsupported_error(self):
        """Test that a .txt file raises UnsupportedFileTypeError."""
        path = FIXTURES_DIR / "invalid_format.txt"
        with pytest.raises(UnsupportedFileTypeError) as exc_info:
            validate_supported_file(path)

        assert exc_info.value.file_extension == ".txt"

    def test_no_extension_file_raises_error(self):
        """Test that a file with no extension raises FileValidationError."""
        path = FIXTURES_DIR / "no_extension"
        with pytest.raises(FileValidationError) as exc_info:
            validate_supported_file(path)

        assert "File has no extension" in str(exc_info.value)

    def test_corrupted_xlsx_file_raises_error(self):
        """Test that a corrupted .xlsx file raises FileValidationError."""
        path = FIXTURES_DIR / "corrupted.xlsx"
        with pytest.raises(FileValidationError) as exc_info:
            validate_supported_file(path)

        assert "not a valid Excel file or is corrupted" in str(exc_info.value)

    def test_accepts_string_path(self):
        """Test that string paths are converted to Path objects."""
        path = str(FIXTURES_DIR / "valid_template.xlsx")
        # Should not raise any exception
        validate_supported_file(path)


class TestSupportedExcelExtensions:
    """Tests for SUPPORTED_EXCEL_EXTENSIONS constant."""

    def test_contains_xlsx(self):
        """Test that .xlsx is in supported extensions."""
        assert ".xlsx" in SUPPORTED_EXCEL_EXTENSIONS

    def test_contains_xls(self):
        """Test that .xls is in supported extensions."""
        assert ".xls" in SUPPORTED_EXCEL_EXTENSIONS

    def test_extensions_are_lowercase(self):
        """Test that all extensions are lowercase."""
        for ext in SUPPORTED_EXCEL_EXTENSIONS:
            assert ext.islower()

    def test_extensions_start_with_dot(self):
        """Test that all extensions start with a dot."""
        for ext in SUPPORTED_EXCEL_EXTENSIONS:
            assert ext.startswith(".")


class TestErrorMessageSecurity:
    """Tests to ensure error messages don't leak sensitive information."""

    def test_file_validation_error_sanitizes_path(self):
        """Test that FileValidationError only shows filename, not full path."""
        full_path = "/Users/secret/documents/sensitive/file.xlsx"
        with pytest.raises(FileValidationError) as exc_info:
            validate_supported_file(Path(full_path))

        error_message = str(exc_info.value)
        # Should contain filename
        assert "file.xlsx" in error_message
        # Should NOT contain full path
        assert "/Users/secret" not in error_message
        assert "sensitive" not in error_message

    def test_unsupported_file_type_error_format(self):
        """Test that UnsupportedFileTypeError has proper format."""
        path = FIXTURES_DIR / "invalid_format.csv"
        with pytest.raises(UnsupportedFileTypeError) as exc_info:
            validate_supported_file(path)

        error_message = str(exc_info.value)
        # Should contain extension
        assert ".csv" in error_message
        # Should contain supported types
        assert ".xlsx" in error_message


class TestEdgeCases:
    """Tests for edge cases and unusual inputs."""

    def test_hidden_file_with_xlsx_extension(self):
        """Test that hidden files (.file.xlsx) with valid extensions work."""
        # This test would need a fixture, but we can test the logic
        path = Path(".hidden_template.xlsx")
        extension = detect_file_type(path)
        assert extension == ".xlsx"
        assert is_excel_file(path) is True

    def test_file_with_multiple_dots(self):
        """Test files with multiple dots in the name."""
        path = Path("my.template.file.xlsx")
        extension = detect_file_type(path)
        assert extension == ".xlsx"
        assert is_excel_file(path) is True

    def test_very_long_filename(self):
        """Test that very long filenames are handled correctly."""
        long_name = "a" * 200 + ".xlsx"
        path = Path(long_name)
        extension = detect_file_type(path)
        assert extension == ".xlsx"
        assert is_excel_file(path) is True
