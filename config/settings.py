from pathlib import Path
from pydantic_settings import BaseSettings
from pydantic import Field
from functools import lru_cache


class Settings(BaseSettings):
    """
    Project settings loaded from environment variables or .env file.
    """

    # General
    ENVIRONMENT: str = Field("dev", description="Environment name: dev/staging/prod")

    # Langchain / Langsmith
    OPENAI_API_KEY: str
    LANGSMITH_API_KEY: str
    LANGCHAIN_TRACING_V2: bool
    LANGCHAIN_PROJECT: str
    LANGCHAIN_ENDPOINT: str

    # Database
    DATABASE_URI: str

    # Qdrant (Vector DB)
    QDRANT_HOST: str = "localhost"
    QDRANT_PORT: int = 6333

    BASE_URLS: dict = {
        "dev": "http://localhost:8000",
        "staging": "https://staging.example.com",
        "prod": "https://example.com"
    }

    @property
    def BASE_URL(self) -> str:
        return self.BASE_URLS.get(self.ENVIRONMENT, self.BASE_URLS["dev"])

    class Config:
        env_file = Path(__file__).parent.parent / ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    """
    Cached settings instance to be reused across the app.
    """
    return Settings()


settings = get_settings()
