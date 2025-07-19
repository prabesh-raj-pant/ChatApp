
from sqlmodel import Field, SQLModel 
from enum import Enum

class Role(str, Enum):
    admin = "admin"
    user = "user"
    
class User(SQLModel,table=True):
    id:int  | None=Field(default=None, primary_key=True)
    username:str =Field(index=True,unique=True)
    email:str =Field(index=True,unique=True)
    password:str 
    role: Role = Field(default=Role.user)

   
    