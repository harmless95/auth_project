from pathlib import Path
from typing import Literal, ClassVar

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel, PostgresDsn
from fastapi.security import OAuth2PasswordBearer

BASEDIR = Path(__file__).resolve().parent.parent

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


class AuthJWT(BaseModel):
    private_key_path: Path = BASEDIR / "certs" / "jwt-private.pem"
    public_key_path: Path = BASEDIR / "certs" / "jwt-public.pem"
    algorithm: str = "RS256"
    access_token_expire_minutes: int = 15
    refresh_token_expire_days: int = 30

    type_token: str = "Bearer"
    type_payload: str = "type"
    type_access: str = "access"
    type_refresh: str = "refresh"

    oauth2_scheme: ClassVar[OAuth2PasswordBearer] = OAuth2PasswordBearer(
        tokenUrl="/auth/login/",
    )


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
    auth_jwt: AuthJWT = AuthJWT()


setting = Settings()
