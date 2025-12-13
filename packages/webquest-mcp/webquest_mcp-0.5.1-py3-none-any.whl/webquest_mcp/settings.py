from typing import Literal

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
        cli_parse_args=True,
    )
    auth_secret: SecretStr | None = Field(default=None)
    auth_audience: str | None = Field(default="webquest-mcp")
    openai_api_key: SecretStr | None = Field(default=None)
    hyperbrowser_api_key: SecretStr | None = Field(default=None)
    transport: Literal[
        "stdio",
        "http",
        "sse",
        "streamable-http",
    ] = Field(default="streamable-http")
    port: int | None = Field(default=None)


_settings = Settings()


def get_settings() -> Settings:
    global _settings
    return _settings
