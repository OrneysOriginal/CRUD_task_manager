from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="allow"
    )
    POSTGRES_DB: str
    POSTGRES_PORT: str
    POSTGRES_HOST: str
    POSTGRES_PASSWORD: str
    POSTGRES_USER: str


config = Settings()
