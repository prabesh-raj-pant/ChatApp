from fastapi import FastAPI,Depends
from typing import Annotated
import uvicorn
from sqlmodel import  Session, SQLModel
from . import schemas, models
from app.database import engine


app = FastAPI()
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]



@app.on_event("startup")
def on_startup():
    create_db_and_tables()

 



@app.post('/user')
def createUser(request: schemas.UserCreate ):
    return request






if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
