"""
AIProviderSetupStage: Initializes the AI provider.

This stage initializes the AI provider based on the provided configuration
or environment variables.
"""

import logging

from template_sense.ai_providers.factory import get_ai_provider
from template_sense.errors import AIProviderError
from template_sense.pipeline.stages.base import PipelineContext, PipelineStage

logger = logging.getLogger(__name__)


class AIProviderSetupStage(PipelineStage):
    """
    Stage 4: Initialize AI provider.

    Initializes the AI provider using the provided configuration or defaults
    from environment. Sets context.ai_provider.

    Raises:
        AIProviderError: If AI provider initialization fails
    """

    def execute(self, context: PipelineContext) -> PipelineContext:
        """Execute AI provider setup stage."""
        logger.info("Stage 4: Initializing AI provider")

        try:
            context.ai_provider = get_ai_provider(context.ai_config)
            logger.info(
                "AI provider initialized: provider=%s, model=%s",
                context.ai_provider.config.provider,
                context.ai_provider.config.model or "default",
            )
        except AIProviderError:
            logger.error("AI provider initialization failed")
            if context.workbook:
                context.workbook.close()
            raise

        logger.info("Stage 4: AI provider setup complete")
        return context


__all__ = ["AIProviderSetupStage"]
