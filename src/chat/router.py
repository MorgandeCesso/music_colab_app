from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import insert, select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from chat.schemas import CreateMessage, CreateRoom
from database import get_async_session
from auth.models import Room, Message
from datetime import datetime
from sqlalchemy.orm import joinedload
 
#Непосредственно роутер
router = APIRouter(
    prefix="/room",
    tags=["Messages"]
)

#Полковнику кто-то пишет?
@router.get("/{room_id}")
async def get_messages(room_id: int, upper_time_limit: datetime, lower_time_limit: datetime, session: AsyncSession = Depends(get_async_session)):
    if (lower_time_limit == None) or (room_id == None):
        lower_time_limit = select(Message.send_date).order_by(Message.send_date.desc())[-1]
    if (lower_time_limit < upper_time_limit):
        raise HTTPException(status_code=500, detail="Lower limit cannot be smaller than upper!")
    if (room_id <= 0):
        raise HTTPException(status_code=500, detail="Limits or room_id cannot be below zero or equal to it!")
    query = select(Message).where(Message.send_date < lower_time_limit, Message.send_date >= upper_time_limit).where(Message.room_id == room_id).order_by(Message.send_date)
    print(query)
    messages = await session.execute(query)
    return messages.mappings().all()

#Когда полковнику писали в последний раз?
@router.get("/{room_id}/last")
async def get_last_message(room_id: int, session: AsyncSession = Depends(get_async_session)):
    if (room_id <= 0):
        raise HTTPException(status_code=500, detail="Room_id cannot be below zero or equal to it!")
    query = select(Message.text).where(Message.room_id == room_id).order_by(Message.send_date.desc()).limit(1)
    print(query)
    last_message = await session.execute(query)
    return last_message.mappings().all() 

#F.R.I.E.N.D.S.
@router.get("/")
async def get_rooms(upper_limit: int, lower_limit: int, session: AsyncSession = Depends(get_async_session)):
    if (lower_limit == None):
        lower_limit = select(Room.id).where(select(Message.send_date).order_by).order_by(Room.id.desc())[-1]
    if (lower_limit < upper_limit):
        raise HTTPException(status_code=500, detail="Lower limit cannot be smaller than upper!")
    if (upper_limit <= 0) or (lower_limit <= 0):
        raise HTTPException(status_code=500, detail="Limits cannot be below zero or equal to it!")
    query = select(Room).where(Room.id < lower_limit, Room.id >= upper_limit)\
        .options(joinedload(Room.room_type))
    print(query)
    posts = await session.execute(query)
    return posts.mappings().all()

#Новая беседа с батюшкой
@router.post("/create_room")
async def create_room(new_room: CreateRoom, session: AsyncSession = Depends(get_async_session)):
    statement = insert(Room).values(**new_room.model_dump())
    await session.execute(statement)
    await session.commit()
    return {"status": "success"}

#Напиши батюшке
@router.post("/{room_id}/new_message")
async def create_message(new_message: CreateMessage, session: AsyncSession = Depends(get_async_session)):
    statement = insert(Message).values(**new_message.model_dump())
    await session.execute(statement)
    await session.commit()
    return {"status": "success"}

#Беседа зашла в тупик
@router.delete("/delete/{room_id}")
async def delete_room(room_id: int, session: AsyncSession = Depends(get_async_session)):
    statement = delete(Room).where(Room.id == room_id)
    print(statement)
    await session.execute(statement)
    await session.commit()
    return {"status": "success"}

#Когда скинул не то фото
@router.delete("/{room_id}/delete_message/{message_id}")
async def delete_message(message_id: int, session: AsyncSession = Depends(get_async_session)):
    statement = delete(Message).where(Message.id == message_id)
    print(statement)
    await session.execute(statement)
    await session.commit()
    return {"status": "success"}


##########################################

#Члены? Пробовал