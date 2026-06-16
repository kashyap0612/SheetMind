from functools import lru_cache
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "SheetMind API"
    environment: str = "development"
    api_prefix: str = "/api/v1"
    frontend_url: str = "http://localhost:3000"
    database_url: str = "postgresql+psycopg://sheetmind:sheetmind@postgres:5432/sheetmind"
    clerk_issuer: str = ""
    clerk_jwks_url: str = ""
    encryption_key: str = Field(..., description="Base64 encoded 32-byte AES key")
    r2_endpoint_url: str = ""
    r2_access_key_id: str = ""
    r2_secret_access_key: str = ""
    r2_bucket: str = "sheetmind"
    r2_region: str = "auto"
    max_upload_mb: int = 50
    free_query_limit: int = 10
    rate_limit: str = "120/minute"
    openai_api_key: str = ""
    gemini_api_key: str = ""
    anthropic_api_key: str = ""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    @field_validator("encryption_key")
    @classmethod
    def require_key(cls, value: str) -> str:
        if not value:
            raise ValueError("ENCRYPTION_KEY is required")
        return value


@lru_cache
def get_settings() -> Settings:
    return Settings()
