"""Application configuration.

Centralized configuration management for Unconditional API.
"""

import os
from enum import Enum


class Environment(str, Enum):
    """Application environment."""

    DEVELOPMENT = "development"
    PRODUCTION = "production"
    TEST = "test"


class Settings:
    """Application settings."""

    def __init__(self):
        self.environment = Environment(os.getenv("ENVIRONMENT", "development"))
        self.log_level = os.getenv("LOG_LEVEL", "info")

        # LLM configuration
        self.llm_provider = os.getenv("LLM_PROVIDER", "openai")
        self.openai_api_key = os.getenv("OPENAI_API_KEY")

        # API configuration
        self.api_host = os.getenv("API_HOST", "0.0.0.0")
        self.api_port = int(os.getenv("PORT", 8000))

    @property
    def is_development(self) -> bool:
        """Check if running in development mode."""
        return self.environment == Environment.DEVELOPMENT

    @property
    def is_production(self) -> bool:
        """Check if running in production mode."""
        return self.environment == Environment.PRODUCTION


# Global settings instance
settings = Settings()
