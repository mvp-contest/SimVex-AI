import os

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str
    redis_url: str
    r2_endpoint: str
    r2_access_key_id: str
    r2_secret_access_key: str
    r2_public_url: str
    openai_api_key: str
    port: int = 8080

    model_config = SettingsConfigDict(
        env_file=".env.local" if os.path.exists(".env.local") else ".env"
    )


settings = Settings()
