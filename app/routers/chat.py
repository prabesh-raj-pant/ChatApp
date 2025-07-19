from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, Query, HTTPException
from sqlmodel import Session, select
from typing import Dict, List, Optional
from datetime import datetime

from app.database import get_session
from app.models import Message, User, Room
from app.oauth2 import get_current_user
 
router = APIRouter(prefix="/chat", tags=['chat-app']) 
active_connections: Dict[int, List[WebSocket]] = {}
 


async def get_recent_messages(session: Session, room_id: int, cursor: Optional[int] = None, limit: int = 10):
    query = select(Message).where(Message.room_id == room_id)
    if cursor:
        query = query.where(Message.id < cursor)
    query = query.order_by(Message.id.desc()).limit(limit)
    messages = session.exec(query).all()
    return list(reversed(messages))


@router.websocket("/ws/{room_id}")
async def websocket_endpoint( websocket: WebSocket,room_id: int,token: str = Query(...),db: Session = Depends(get_session)):
    await websocket.accept()

    user = await get_current_user(token, db)

    # tract active connection available
    if room_id not in active_connections:
        active_connections[room_id] = []
    active_connections[room_id].append(websocket)

    # send  messages  
    recent_messages = await get_recent_messages(db, room_id)
    for msg in recent_messages:
        await websocket.send_json({
            "id": msg.id,
            "user_id": msg.user_id,
            "content": msg.content,
            "timestamp": msg.timestamp.isoformat()
        })

    try:
        while True:
            data = await websocket.receive_json()
            content = data.get("content")

            if not content:
                await websocket.send_json({"error": "Empty message!"})
                continue

          
            message = Message(
                content=content,
                room_id=room_id,
                user_id=user.id,
                timestamp=datetime.utcnow()
            )
            db.add(message)
            db.commit()
            db.refresh(message)

            response = {
                "id": message.id,
                "user_id": user.id,
                "content": message.content,
                "timestamp": message.timestamp.isoformat()
            }

            #  all clients in the room ma laune
            for conn in active_connections[room_id]:
                await conn.send_json(response)

    except WebSocketDisconnect:
        active_connections[room_id].remove(websocket)
    except Exception as e:
        print(f"WebSocket Error: {e}")
        await websocket.close()
        active_connections[room_id].remove(websocket)
