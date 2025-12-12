"""
Unit tests for constants module.

Tests that all constants exist, have correct types, and contain expected values.
"""

from template_sense.constants import (
    AI_MODEL_ENV_VAR,
    AI_PROVIDER_ENV_VAR,
    ANTHROPIC_API_KEY_ENV_VAR,
    DEFAULT_AI_TIMEOUT_SECONDS,
    DEFAULT_AUTO_MAPPING_THRESHOLD,
    DEFAULT_CONFIDENCE_THRESHOLD,
    DEFAULT_MAX_HEADER_ROWS,
    DEFAULT_MIN_TABLE_ROWS,
    LOG_LEVEL_ENV_VAR,
    MIN_GRID_COLUMNS,
    MIN_GRID_ROWS,
    OPENAI_API_KEY_ENV_VAR,
    SUPPORTED_AI_PROVIDERS,
    SUPPORTED_FILE_EXTENSIONS,
)


class TestFileRelatedConstants:
    """Tests for file-related constants."""

    def test_supported_file_extensions_exists(self):
        """Test that SUPPORTED_FILE_EXTENSIONS constant exists."""
        assert SUPPORTED_FILE_EXTENSIONS is not None

    def test_supported_file_extensions_is_tuple(self):
        """Test that SUPPORTED_FILE_EXTENSIONS is a tuple for immutability."""
        assert isinstance(SUPPORTED_FILE_EXTENSIONS, tuple)

    def test_supported_file_extensions_contains_xlsx(self):
        """Test that .xlsx is in supported extensions."""
        assert ".xlsx" in SUPPORTED_FILE_EXTENSIONS

    def test_supported_file_extensions_contains_xls(self):
        """Test that .xls is in supported extensions."""
        assert ".xls" in SUPPORTED_FILE_EXTENSIONS

    def test_supported_file_extensions_all_lowercase(self):
        """Test that all extensions are lowercase."""
        for ext in SUPPORTED_FILE_EXTENSIONS:
            assert ext.islower()

    def test_supported_file_extensions_start_with_dot(self):
        """Test that all extensions start with a dot."""
        for ext in SUPPORTED_FILE_EXTENSIONS:
            assert ext.startswith(".")


class TestExtractionConstants:
    """Tests for extraction-related constants."""

    def test_default_max_header_rows(self):
        """Test DEFAULT_MAX_HEADER_ROWS has expected value and type."""
        assert DEFAULT_MAX_HEADER_ROWS == 50
        assert isinstance(DEFAULT_MAX_HEADER_ROWS, int)

    def test_default_min_table_rows(self):
        """Test DEFAULT_MIN_TABLE_ROWS has expected value and type."""
        assert DEFAULT_MIN_TABLE_ROWS == 3
        assert isinstance(DEFAULT_MIN_TABLE_ROWS, int)

    def test_default_confidence_threshold(self):
        """Test DEFAULT_CONFIDENCE_THRESHOLD has expected value and type."""
        assert DEFAULT_CONFIDENCE_THRESHOLD == 0.7
        assert isinstance(DEFAULT_CONFIDENCE_THRESHOLD, float)
        assert 0.0 <= DEFAULT_CONFIDENCE_THRESHOLD <= 1.0

    def test_default_auto_mapping_threshold(self):
        """Test DEFAULT_AUTO_MAPPING_THRESHOLD has expected value and type."""
        assert DEFAULT_AUTO_MAPPING_THRESHOLD == 80.0
        assert isinstance(DEFAULT_AUTO_MAPPING_THRESHOLD, float)
        assert 0.0 <= DEFAULT_AUTO_MAPPING_THRESHOLD <= 100.0

    def test_default_ai_timeout_seconds(self):
        """Test DEFAULT_AI_TIMEOUT_SECONDS has expected value and type."""
        assert DEFAULT_AI_TIMEOUT_SECONDS == 30
        assert isinstance(DEFAULT_AI_TIMEOUT_SECONDS, int)

    def test_min_grid_constraints(self):
        """Test grid validation constants have expected values."""
        assert MIN_GRID_ROWS == 1
        assert MIN_GRID_COLUMNS == 1
        assert isinstance(MIN_GRID_ROWS, int)
        assert isinstance(MIN_GRID_COLUMNS, int)


class TestAIProviderConstants:
    """Tests for AI provider-related constants."""

    def test_environment_variable_names(self):
        """Test that environment variable names are strings with expected values."""
        assert AI_PROVIDER_ENV_VAR == "TEMPLATE_SENSE_AI_PROVIDER"
        assert AI_MODEL_ENV_VAR == "TEMPLATE_SENSE_AI_MODEL"
        assert OPENAI_API_KEY_ENV_VAR == "OPENAI_API_KEY"
        assert ANTHROPIC_API_KEY_ENV_VAR == "ANTHROPIC_API_KEY"
        assert LOG_LEVEL_ENV_VAR == "TEMPLATE_SENSE_LOG_LEVEL"

        # All should be strings
        for env_var in [
            AI_PROVIDER_ENV_VAR,
            AI_MODEL_ENV_VAR,
            OPENAI_API_KEY_ENV_VAR,
            ANTHROPIC_API_KEY_ENV_VAR,
            LOG_LEVEL_ENV_VAR,
        ]:
            assert isinstance(env_var, str)

    def test_supported_ai_providers(self):
        """Test SUPPORTED_AI_PROVIDERS contains expected values."""
        assert SUPPORTED_AI_PROVIDERS == ("openai", "anthropic")
        assert isinstance(SUPPORTED_AI_PROVIDERS, tuple)

        # Each provider should be lowercase string
        for provider in SUPPORTED_AI_PROVIDERS:
            assert isinstance(provider, str)
            assert provider.islower()


class TestConstantNamingConventions:
    """Tests for consistent naming conventions."""

    def test_default_prefix_for_configurable_values(self):
        """Test that configurable values use DEFAULT_ prefix."""
        configurable_constants = [
            "DEFAULT_MAX_HEADER_ROWS",
            "DEFAULT_MIN_TABLE_ROWS",
            "DEFAULT_CONFIDENCE_THRESHOLD",
            "DEFAULT_AUTO_MAPPING_THRESHOLD",
            "DEFAULT_AI_TIMEOUT_SECONDS",
        ]

        # Import constants module to check all names
        from template_sense import constants

        for const_name in configurable_constants:
            assert hasattr(constants, const_name), f"Missing constant: {const_name}"

    def test_no_default_prefix_for_fixed_constraints(self):
        """Test that fixed constraints don't use DEFAULT_ prefix."""
        fixed_constants = [
            "SUPPORTED_FILE_EXTENSIONS",
            "SUPPORTED_AI_PROVIDERS",
            "MIN_GRID_ROWS",
            "MIN_GRID_COLUMNS",
        ]

        from template_sense import constants

        for const_name in fixed_constants:
            assert hasattr(constants, const_name), f"Missing constant: {const_name}"
            assert not const_name.startswith(
                "DEFAULT_"
            ), f"Fixed constant should not have DEFAULT_ prefix: {const_name}"
