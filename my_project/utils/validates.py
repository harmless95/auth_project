import uuid
from datetime import timedelta, datetime, timezone
import jwt

import bcrypt

from core.config import setting


def encode_jwt(
    payload: dict,
    private_key: str = setting.auth_jwt.private_key_path.read_text(),
    algorithm: str = setting.auth_jwt.algorithm,
    expire_minutes: int = setting.auth_jwt.access_token_expire_minutes,
    expire_timedelta: timedelta | None = None,
) -> str:
    to_encode = payload.copy()
    now = datetime.now(timezone.utc)
    if expire_timedelta:
        expire = now + expire_timedelta
    else:
        expire = now + timedelta(minutes=expire_minutes)
    to_encode.update(
        exp=expire,
        iat=now,
        jti=str(uuid.uuid4()),
    )
    encoded = jwt.encode(
        to_encode,
        private_key,
        algorithm=algorithm,
    )
    return encoded


def hash_password(password: str) -> bytes:
    salt = bcrypt.gensalt()
    pwd_bites: bytes = password.encode()
    return bcrypt.hashpw(pwd_bites, salt)


def validates_password(
    password: str,
    password_hash: str,
) -> bool:
    password_hash = bytes.fromhex(password_hash)
    return bcrypt.checkpw(
        password=password.encode(),
        hashed_password=password_hash,
    )
