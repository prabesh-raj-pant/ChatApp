from fastapi import Depends,HTTPException,status
from typing import Annotated 
from fastapi.security import OAuth2PasswordBearer
import os
from .database import Session,get_session
from .models import User
from dotenv import load_dotenv
load_dotenv() 
from .jwttoken import verify_token

SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM') 


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_session)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    ) 
    token_data = verify_token(token, credentials_exception)
    user = db.query(User).filter(User.email == token_data.email).first()
    if not user:
        raise credentials_exception
    return user 
