from pydantic import BaseModel, EmailStr


class User(BaseModel):
    email: EmailStr


class UserInDB(User):
    hashed_password: str


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    email: EmailStr | None = None
