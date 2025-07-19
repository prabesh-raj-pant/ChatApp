from fastapi import Depends
from sqlmodel import  Session, SQLModel
from typing import Annotated
from sqlmodel import  create_engine

from dotenv import load_dotenv
import os

load_dotenv()
 
db_url =os.getenv('DATABASE_URL',123)
 
engine = create_engine(db_url )

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
