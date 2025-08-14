from pydantic_settings import BaseSettings
from pydantic import BaseModel, PostgresDsn


class ConfigDatabase(BaseModel):
    url: PostgresDsn
    echo: bool = False


class Settings(BaseSettings):
    db: ConfigDatabase


setting = Settings()
