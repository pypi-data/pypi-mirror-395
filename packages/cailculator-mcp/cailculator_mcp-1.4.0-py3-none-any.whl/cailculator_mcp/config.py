"""
Configuration Management for CAILculator MCP
"""

import os
from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # API Key (set by user in MCP client config)
    api_key: str = ""

    # Auth server endpoint
    auth_endpoint: str = "https://cailculator-mcp-production.up.railway.app/validate"

    # Development/testing flags
    enable_dev_mode: bool = False
    enable_offline_fallback: bool = True  # Fallback if auth server unreachable

    # Logging
    log_level: str = "INFO"

    class Config:
        env_prefix = "CAILCULATOR_"
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance (singleton pattern)."""
    return Settings()
