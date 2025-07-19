from pydantic import BaseModel, EmailStr
from enum import Enum
from typing import Optional
from datetime import datetime

# user schema
class Role(str, Enum):
    admin = "admin"
    user = "user"
    
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: Role = Role.user

class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: Role

    model_config = {"from_attributes": True}
    
class Login(BaseModel):
    email:EmailStr
    password:str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: EmailStr | None = None



# room schema
class RoomCreate(BaseModel):
    name: str
    description: Optional[str] = None


class RoomRead(BaseModel):
    id: int
    name: str
    description: Optional[str]

    model_config = {"from_attributes": True}


# message schema
class MessageCreate(BaseModel):
    content: str
    room_id:int


class MessageRead(BaseModel):
    id:int
    content: str
    timestamp: datetime
    user_id:int
    room_id:int

    class Config:
        orm_mode = True

