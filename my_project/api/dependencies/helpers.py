from datetime import datetime, timezone, timedelta

from core.config import setting
from core.model import User
from utils.validates import encode_jwt


def create_token(
    type_payload: str,
    payload: dict,
    private_key: str = setting.auth_jwt.private_key_path.read_text(),
    algorithm: str = setting.auth_jwt.algorithm,
    expire_minutes: int = setting.auth_jwt.access_token_expire_minutes,
    expire_timedelta: timedelta | None = None,
):
    type_token = setting.auth_jwt.type_payload
    type_payload = {type_token: type_payload}
    type_payload.update(payload)
    return encode_jwt(
        payload=type_payload,
        private_key=private_key,
        algorithm=algorithm,
        expire_minutes=expire_minutes,
        expire_timedelta=expire_timedelta,
    )


def create_access_token(user: User):
    now = datetime.now(timezone.utc)
    jwt_payload = {
        "sub": user.email,
        "email": user.email,
        "name": user.name,
        "logged_in_at": now.isoformat(),
    }
    type_payload = setting.auth_jwt.type_access
    return create_token(
        type_payload=type_payload,
        payload=jwt_payload,
    )


def create_refresh_token(user: User):
    jwt_payload = {
        "sub": user.email,
    }
    type_payload = setting.auth_jwt.type_refresh
    expire_timedelta = timedelta(days=setting.auth_jwt.refresh_token_expire_days)
    return create_token(
        type_payload=type_payload,
        payload=jwt_payload,
        expire_timedelta=expire_timedelta,
    )
