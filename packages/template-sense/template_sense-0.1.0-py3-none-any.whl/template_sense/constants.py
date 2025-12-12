"""
Central configuration constants for the template_sense package.

This module defines all shared configuration values used across the package.
Constants should be imported and used directly - never redefined in other modules.

Usage:
    from template_sense.constants import DEFAULT_CONFIDENCE_THRESHOLD, SUPPORTED_FILE_EXTENSIONS
"""

# ============================================================
# File-related Constants
# ============================================================

SUPPORTED_FILE_EXTENSIONS = (".xlsx", ".xls")  # Canonical source - tuple for immutability

# ============================================================
# Extraction-related Constants
# ============================================================

# Extraction limits
DEFAULT_MAX_HEADER_ROWS = 50  # Maximum rows to scan for headers
DEFAULT_MIN_TABLE_ROWS = 3  # Minimum consecutive rows to qualify as a table

# Confidence thresholds
DEFAULT_CONFIDENCE_THRESHOLD = 0.7  # Heuristic/AI confidence (0.0-1.0)
DEFAULT_AUTO_MAPPING_THRESHOLD = 80.0  # Fuzzy match score for auto-mapping (0.0-100.0)

# Table detection thresholds
DEFAULT_TABLE_MIN_SCORE = 0.5  # Minimum score for table candidate rows (0.0-1.0)
DEFAULT_TABLE_HEADER_MIN_SCORE = 0.6  # Minimum score for table header row detection (0.0-1.0)

# AI timeouts
DEFAULT_AI_TIMEOUT_SECONDS = 30  # Timeout per AI request

# AI payload configuration
DEFAULT_AI_SAMPLE_ROWS = 5  # Number of sample data rows to include in AI payload
DEFAULT_ADJACENT_CELL_RADIUS = 3  # Number of adjacent cells in each direction for header context

# Grid validation
MIN_GRID_ROWS = 1
MIN_GRID_COLUMNS = 1

# ============================================================
# AI Provider Constants
# ============================================================

# AI Provider Configuration
AI_PROVIDER_ENV_VAR = "TEMPLATE_SENSE_AI_PROVIDER"
AI_MODEL_ENV_VAR = "TEMPLATE_SENSE_AI_MODEL"
OPENAI_API_KEY_ENV_VAR = "OPENAI_API_KEY"
ANTHROPIC_API_KEY_ENV_VAR = "ANTHROPIC_API_KEY"
LOG_LEVEL_ENV_VAR = "TEMPLATE_SENSE_LOG_LEVEL"

# Supported providers
SUPPORTED_AI_PROVIDERS = ("openai", "anthropic")

# Default AI models
DEFAULT_OPENAI_MODEL = "gpt-4"
DEFAULT_ANTHROPIC_MODEL = "claude-3-sonnet-20240229"

# AI temperature settings
AI_CLASSIFICATION_TEMPERATURE = 0.0  # Deterministic for classification
AI_TRANSLATION_TEMPERATURE = 0.3  # Slight creativity for natural translations

# Anthropic-specific limits
ANTHROPIC_CLASSIFICATION_MAX_TOKENS = 4096
ANTHROPIC_TRANSLATION_MAX_TOKENS = 2048

# ============================================================
# Translation Constants
# ============================================================

DEFAULT_TARGET_LANGUAGE = "en"  # Default target language for translation
TRANSLATION_TIMEOUT_SECONDS = 30  # Timeout for translation requests

# ============================================================
# Mapping/Normalization Constants
# ============================================================

# AI Semantic Matching Configuration
ENABLE_AI_SEMANTIC_MATCHING = False  # Feature flag for AI-powered semantic field matching
SEMANTIC_MATCHING_CONFIDENCE_THRESHOLD = (
    0.7  # Minimum AI confidence to accept semantic match (0.0-1.0)
)
SEMANTIC_MATCHING_FUZZY_FLOOR = 30.0  # Minimum fuzzy score to attempt semantic matching (0.0-100.0)
SEMANTIC_MATCHING_TIMEOUT_SECONDS = 10  # Timeout for semantic matching AI requests
SEMANTIC_MATCHING_MAX_TOKENS = 150  # Maximum tokens for semantic matching AI responses
SEMANTIC_MATCHING_TEMPERATURE = 0.0  # Deterministic temperature for semantic matching

# ============================================================
# Error Recovery Thresholds
# ============================================================

# AI confidence threshold for warnings (0.0-1.0 scale)
MIN_AI_CONFIDENCE_WARNING: float = 0.5

# Fuzzy match score threshold for warnings (0.0-100.0 scale)
MIN_FUZZY_MATCH_WARNING: float = 70.0

# Maximum acceptable field failure rate (0.0-1.0 scale, e.g., 0.3 = 30%)
MAX_FIELD_FAILURE_RATE: float = 0.3

# ============================================================
# Table Header Detection Thresholds
# ============================================================

# Text density threshold for table header rows (0.0-1.0 scale)
# Rows with >70% text cells are likely column labels
DEFAULT_HEADER_TEXT_DENSITY_THRESHOLD: float = 0.7

# Cell density threshold for table header rows (0.0-1.0 scale)
# Rows with >50% non-empty cells are likely headers
DEFAULT_HEADER_CELL_DENSITY_THRESHOLD: float = 0.5

# Maximum numeric density for table header rows (0.0-1.0 scale)
# Rows with <30% numeric cells are likely text-based headers
DEFAULT_HEADER_NUMERIC_DENSITY_MAX: float = 0.3

# ============================================================
# Output Constants
# ============================================================

OUTPUT_SCHEMA_VERSION = "1.0"  # Default version for normalized output schema
PIPELINE_VERSION = "1.0"  # Pipeline orchestration version


__all__ = [
    "SUPPORTED_FILE_EXTENSIONS",
    "DEFAULT_MAX_HEADER_ROWS",
    "DEFAULT_MIN_TABLE_ROWS",
    "DEFAULT_CONFIDENCE_THRESHOLD",
    "DEFAULT_AUTO_MAPPING_THRESHOLD",
    "DEFAULT_TABLE_MIN_SCORE",
    "DEFAULT_TABLE_HEADER_MIN_SCORE",
    "DEFAULT_AI_TIMEOUT_SECONDS",
    "DEFAULT_AI_SAMPLE_ROWS",
    "DEFAULT_ADJACENT_CELL_RADIUS",
    "MIN_GRID_ROWS",
    "MIN_GRID_COLUMNS",
    "AI_PROVIDER_ENV_VAR",
    "AI_MODEL_ENV_VAR",
    "OPENAI_API_KEY_ENV_VAR",
    "ANTHROPIC_API_KEY_ENV_VAR",
    "LOG_LEVEL_ENV_VAR",
    "SUPPORTED_AI_PROVIDERS",
    "DEFAULT_OPENAI_MODEL",
    "DEFAULT_ANTHROPIC_MODEL",
    "AI_CLASSIFICATION_TEMPERATURE",
    "AI_TRANSLATION_TEMPERATURE",
    "ANTHROPIC_CLASSIFICATION_MAX_TOKENS",
    "ANTHROPIC_TRANSLATION_MAX_TOKENS",
    "DEFAULT_TARGET_LANGUAGE",
    "TRANSLATION_TIMEOUT_SECONDS",
    "ENABLE_AI_SEMANTIC_MATCHING",
    "SEMANTIC_MATCHING_CONFIDENCE_THRESHOLD",
    "SEMANTIC_MATCHING_FUZZY_FLOOR",
    "SEMANTIC_MATCHING_TIMEOUT_SECONDS",
    "SEMANTIC_MATCHING_MAX_TOKENS",
    "SEMANTIC_MATCHING_TEMPERATURE",
    "MIN_AI_CONFIDENCE_WARNING",
    "MIN_FUZZY_MATCH_WARNING",
    "MAX_FIELD_FAILURE_RATE",
    "DEFAULT_HEADER_TEXT_DENSITY_THRESHOLD",
    "DEFAULT_HEADER_CELL_DENSITY_THRESHOLD",
    "DEFAULT_HEADER_NUMERIC_DENSITY_MAX",
    "OUTPUT_SCHEMA_VERSION",
    "PIPELINE_VERSION",
]
