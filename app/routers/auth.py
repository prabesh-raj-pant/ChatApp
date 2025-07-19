from fastapi import APIRouter, Depends, HTTPException,status
from sqlmodel import Session,select
from app.models import User
from .hashing import Hash
from app.schemas import UserCreate, Login
from app.database import get_session
from app.schemas import UserCreate


router = APIRouter(prefix="/auth", tags=['Authentication'])
SECRET_KEY = "73c34e01da25038628d56de7e9a649d370944a667cf9b7c7f66155ba7e0e6e37"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30



@router.post('/signup')
def createUser(user_data: UserCreate, db: Session = Depends(get_session)):
    user = db.query(User).filter(User.username == user_data.username).first()
    if user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username Already taken")
    
    new_user=User(username=user_data.username, email=user_data.email, password=Hash.bcrypt(user_data.password), role=user_data.role)
    db.add(new_user)
    db.commit()
    db.refresh(new_user) 
    return new_user
 
 
  
@router.post('/login')
def login(request:Login,db: Session = Depends(get_session)) :
    user = db.query(User).filter(User.username == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Credentials")
    if not Hash.verify(user.password, request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Incorrect Password")
    
    # generating  a jwt token
    return user
    
    
    

# @router.get('/user/{id}',response_model=UserResponse)
# def get_user(id:int,db: Session = Depends(get_session)):
#     user = db.get(User, id)  
#     if not user:
#          raise HTTPException(status_code=404, detail="User not found")
     
#     return user
