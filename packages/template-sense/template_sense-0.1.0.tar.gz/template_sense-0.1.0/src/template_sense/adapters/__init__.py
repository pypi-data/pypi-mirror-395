"""
Adapters package for Template Sense.

This package provides abstraction layers for different file formats.
Adapters shield the extraction pipeline from format-specific implementation details.

Modules:
    excel_adapter: Excel workbook abstraction using openpyxl
"""

from template_sense.adapters.excel_adapter import ExcelWorkbook

__all__ = ["ExcelWorkbook"]
