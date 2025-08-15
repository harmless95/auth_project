import bcrypt


def hash_password(password: str) -> bytes:
    salt = bcrypt.gensalt()
    pwd_bites: bytes = password.encode()
    return bcrypt.hashpw(pwd_bites, salt)
