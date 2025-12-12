from functools import lru_cache
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="AGENTGEAR_", env_file=".env", env_file_encoding="utf-8")

    database_url: str = "sqlite:///./agentgear.db"
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    secret_key: str = "agentgear-dev-secret"
    allow_origins: list[str] = ["*"]
    local_mode: bool = False
    admin_username: str | None = None
    admin_password: str | None = None


class VersionInfo(BaseModel):
    version: str = "0.1.4"
    name: str = "AgentGear"


@lru_cache
def get_settings() -> Settings:
    return Settings()
