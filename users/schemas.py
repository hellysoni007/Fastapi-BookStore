from pydantic import BaseModel
from pydantic import EmailStr


class RoleIn(BaseModel):
    name: str


class RoleOut(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    email: EmailStr
    last_name: str
    first_name: str
    password: str
    role_id: int


class User(BaseModel):
    email: EmailStr
    last_name: str
    first_name: str
    role_id: int

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str or None

class ChangePassWord(BaseModel):
    password: str
    new_password: str
    confirm_password: str