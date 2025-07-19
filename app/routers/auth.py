from fastapi import APIRouter, Depends, HTTPException,status
from sqlmodel import Session,select
from app.models import User
from .hashing import Hash
from app.schemas import UserCreate, Login
from app.database import get_session
from app.schemas import UserCreate
from app.jwttoken import *
import os
from dotenv import load_dotenv
load_dotenv()

router = APIRouter(prefix="/auth", tags=['Authentication'])


@router.post('/signup')
def createUser(user_data: UserCreate, db: Session = Depends(get_session)):
    user = db.query(User).filter(User.username == user_data.username).first()
    if user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User Already Exists")
    
    new_user=User(username=user_data.username, email=user_data.email, password=Hash.bcrypt(user_data.password), role=user_data.role)
    db.add(new_user)
    db.commit()
    db.refresh(new_user) 
    return new_user
 
 
  
@router.post('/login')
def login(request:Login,db: Session = Depends(get_session)) :
    user = db.query(User).filter(User.email == request.email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Credentials")
    if not Hash.verify(user.password, request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Incorrect Password")
    
    # generating  a jwt token 
    access_token_expires = timedelta(minutes=os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES'))
    access_token = create_access_token(data={"sub": user.username},expires_delta=access_token_expires)
    return Token(access_token=access_token, token_type="bearer")
    
    

# @router.get('/user/{id}',response_model=UserResponse)
# def get_user(id:int,db: Session = Depends(get_session)):
#     user = db.get(User, id)  
#     if not user:
#          raise HTTPException(status_code=404, detail="User not found")
     
#     return user
