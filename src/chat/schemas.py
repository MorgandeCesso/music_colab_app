from datetime import datetime
from pydantic import BaseModel

#Создание сообщения (без комментариев)
class CreateMessage(BaseModel):
    sender_id: int
    room_id: int
    text: str
    attachment_id: int

class CreateRoom(BaseModel):
    room_type_id: int
    name: str