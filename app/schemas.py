from pydantic import BaseModel, EmailStr
from enum import Enum


class Role(str, Enum):
    admin = "admin"
    user = "user"
    
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: Role = Role.user

class Login(BaseModel):
    email:EmailStr
    password:str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: EmailStr | None = None


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: Role

    model_config = {"from_attributes": True}