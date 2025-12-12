from pydantic_settings import BaseSettings
from pydantic import AnyUrl, ConfigDict, Field


class Settings(BaseSettings):
    database_url: str = "sqlite:///./etl.db"
    # Real CoinGecko API for cryptocurrency market data
    api_source_url: AnyUrl | str = Field(
        default="https://api.coingecko.com/api/v3/coins/markets",
        description="CoinGecko API endpoint for cryptocurrency market data"
    )
    api_key: str = Field(
        ...,  # Required field - must be set in environment
        description="API key for authentication (if needed)"
    )

    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )


settings = Settings()
