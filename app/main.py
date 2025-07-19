from fastapi import FastAPI,Depends,HTTPException
from typing import Annotated
import uvicorn
from sqlmodel import  Session, SQLModel
from . import schemas, models
from .routers.hashing import Hash
from .routers import auth,chat,room
from .database import create_db_and_tables

app = FastAPI() 


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


app.include_router(auth.router) 
app.include_router(chat.router)
app.include_router(room.router)

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
