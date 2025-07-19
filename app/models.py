
from sqlmodel import Field, SQLModel ,Relationship
from enum import Enum
from typing import Optional,List

from datetime import datetime

class Role(str, Enum):
    admin = "admin"
    user = "user"
    
class User(SQLModel,table=True):
    id:int  | None=Field(default=None, primary_key=True)
    username:str =Field(index=True,unique=True)
    email:str =Field(index=True,unique=True)
    password:str 
    role: Role = Field(default=Role.user)
    messages: List["Message"] = Relationship(back_populates="user")

class Room(SQLModel,table=True):
    id:int  | None=Field(default=None, primary_key=True)
    name:str =Field(index=True,unique=True,nullable=False)
    description: Optional[str] = None
    
    messages: List["Message"] = Relationship(back_populates="room")


class Message(SQLModel, table=True):
    id: int  | None=Field(default=None, primary_key=True)
    content: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    user_id: int | None=Field(foreign_key="user.id")
    room_id: int | None=Field(foreign_key="room.id")

    user: Optional[User] = Relationship(back_populates="messages")
    room: Optional[Room] = Relationship(back_populates="messages")

    
    
    