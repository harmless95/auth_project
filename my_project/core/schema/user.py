from pydantic import BaseModel, EmailStr, ConfigDict


class UserBase(BaseModel):
    email: EmailStr
    password: str
    name: str
    model_config = ConfigDict(from_attributes=True)


class UserCreate(UserBase):
    pass


class UserRead(BaseModel):
    id: int
    email: EmailStr
    name: str
    model_config = ConfigDict(from_attributes=True)

class UserUpdate(BaseModel):
    email: EmailStr | None = None
    password: str | None = None
    name: str | None = None

    model_config = ConfigDict(from_attributes=True)

class UserLogin(BaseModel):
    model_config = ConfigDict(strict=True)
    email: EmailStr
    password_hash: str
    name: str

class UserReadLogin(BaseModel):
    email: EmailStr
    password: str
    model_config = ConfigDict(from_attributes=True)