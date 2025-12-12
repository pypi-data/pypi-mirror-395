"""Runtime settings loaded from environment or .env."""

from __future__ import annotations

from functools import lru_cache
from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configuration required by the CLI and backend clients."""

    google_ai_studio_api_key: Optional[str] = Field(
        default=None,
        description="Primary credential for Gemini 3 access",
        validation_alias="GOOGLE_AI_STUDIO_API_KEY",
    )
    google_ai_studio_project: Optional[str] = Field(
        default=None,
        description="Project or workspace identifier",
        validation_alias="GOOGLE_AI_STUDIO_PROJECT",
    )
    telemetry_opt_in: bool = Field(
        default=False, validation_alias="DEPRECAT_TELEMETRY_OPT_IN"
    )

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return cached settings instance to avoid re-reading the file."""
    return Settings()
