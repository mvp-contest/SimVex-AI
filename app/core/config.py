import os

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    ...

    model_config = SettingsConfigDict(
        env_file=".env.local" if os.path.exists(".env.local") else ".env"
    )


settings = Settings()
