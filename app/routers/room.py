from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from app.models import Room, User
from app.schemas import RoomCreate, RoomRead
from app.database import get_session
from app.oauth2 import get_current_user

router = APIRouter(prefix="/rooms", tags=["Room"])


@router.post("/", response_model=RoomRead, status_code=201)
def create_room(room_data: RoomCreate, db: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    # Only admin can create room
    if current_user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only admin can create chat rooms")

    # Check if room already exists
    existing_room = db.query(Room).filter(Room.name == room_data.name).first()
    # existing_room = db.exec(select(Room).where(Room.name == room_data.name)).first()
    if existing_room:
        raise HTTPException(status_code=409, detail="Room with this name already exists")

    room = Room(name=room_data.name, description=room_data.description)
    db.add(room)
    db.commit()
    db.refresh(room)
    return room
