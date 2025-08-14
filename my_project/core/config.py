from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel, PostgresDsn

# fmt: off
LOG_DEFAULT_FORMAT = "[%(asctime)s.%(msecs)03d] %(module)10s:%(lineno)-3d %(levelname)-7s - %(message)s"
# fmt: on


class RunConfig(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8000


class ConfigDatabase(BaseModel):
    url: PostgresDsn
    echo: bool = False


class LoggingConfig(BaseModel):
    log_level: Literal[
        "debag",
        "info",
        "warning",
        "error",
        "critical",
    ] = "info"
    log_format: str = LOG_DEFAULT_FORMAT


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(".env.template", ".env"),
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="APP_CONFIG__",
    )
    db: ConfigDatabase
    run: RunConfig = RunConfig()
    logging: LoggingConfig = LoggingConfig()


setting = Settings()
