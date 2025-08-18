from pydantic import BaseModel, ConfigDict

from core.config import setting


class TokenBase(BaseModel):
    access_token: str
    refresh_token: str | None = None
    token_type: str = setting.auth_jwt.type_token

    model_config = ConfigDict(from_attributes=True)