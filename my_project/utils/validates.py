import bcrypt


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
