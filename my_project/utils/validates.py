import uuid
from datetime import timedelta, datetime, timezone
import jwt

import bcrypt

from core.config import setting


def encode_jwt(
    payload: dict,
    private_key: str,
    algorithm: str,
    expire_minutes: int,
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


def decode_jwt(
    token: str | bytes,
    public_key: str,
    algorithm: str,
) -> dict:
    decoded = jwt.decode(
        token,
        public_key,
        algorithms=[algorithm],
    )
    return decoded


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
