from fastapi import FastAPI,Depends
from typing import Annotated
import uvicorn
from sqlmodel import  Session, SQLModel
from . import schemas, models,hashing
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

 

# authentication

SECRET_KEY = "73c34e01da25038628d56de7e9a649d370944a667cf9b7c7f66155ba7e0e6e37"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30



@app.post('/user')
def createUser(user_data: schemas.UserCreate, db: Session = Depends(get_session)):
    
    new_user=models.User(username=user_data.username, email=user_data.email, password=hashing.Hash.bcrypt(user_data.password), role=user_data.role)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user






if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
