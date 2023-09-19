from datetime import datetime
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import Boolean, Integer, String, ForeignKey, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
from base import Base

#ПОМОГИТЕЕЕЕЕЕЕЕЕЕЕЕЕЕЕЕЕЕЕЕЕЕЕЕЕЕЕЕЕЕ

class Role(Base):
    __tablename__ = "role"
    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[str] = mapped_column(String)
    user: Mapped[List["User"]] = relationship(back_populates="role")
    

class Picture(Base):
    __tablename__ = "picture"

    id: Mapped[int] = mapped_column(primary_key=True)
    path: Mapped[str] = mapped_column(String)
    user: Mapped["User"] = relationship(back_populates="picture")

class User(SQLAlchemyBaseUserTable[int], Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    given_name: Mapped[str] = mapped_column(String, nullable=False)
    surname: Mapped[str] = mapped_column(String, nullable=False)
    nickname: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[String] = mapped_column(String, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(length=1024), nullable=False)
    role_id: Mapped[int] = mapped_column(ForeignKey("role.id"))
    role: Mapped[Role] = relationship(back_populates="user")
    picture_id: Mapped[int] = mapped_column(ForeignKey("picture.id"))
    picture: Mapped[Picture] = relationship(back_populates="user")
    message: Mapped[List["Message"]] = relationship(back_populates="user")
    registration_date: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.utcnow)
    post: Mapped[List["Post"]] = relationship(back_populates="user")
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

class Track(Base):
    __tablename__ = "track"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String)
    cover_path: Mapped[str] = mapped_column(String)
    track_path: Mapped[str] = mapped_column(String)

    post: Mapped["Post"] = relationship(back_populates="track")

class Post(Base):
    __tablename__ = "post"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    user: Mapped["User"] = relationship(back_populates="post")
    like_amount: Mapped[int] = mapped_column(Integer, default=0)
    tack_id: Mapped[int] = mapped_column(ForeignKey("track.id"), nullable=False)
    track: Mapped["Track"] = relationship(back_populates="post")
    descripton: Mapped[str] = mapped_column(String)
    price: Mapped[int] = mapped_column(Integer)
    post_date: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.utcnow)

class Message(Base):
    __tablename__ = "message"

    id: Mapped[int] = mapped_column(primary_key=True)
    sender_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    room_id: Mapped[int] = mapped_column(ForeignKey("room.id"), nullable=False, unique=True)
    user: Mapped["User"] = relationship(back_populates="message")
    room: Mapped["Room"] = relationship(back_populates="message")
    text: Mapped[str] = mapped_column(String(500), nullable=False)
    attachment_id: Mapped[int] = mapped_column(ForeignKey("attachment.id"), nullable=True)
    attachment: Mapped["Attachment"] = relationship(back_populates="message")
    send_date: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.utcnow)

class Room(Base):
    __tablename__ = "room"

    id: Mapped[int] = mapped_column(primary_key=True)
    room_type_id: Mapped[int] = mapped_column(ForeignKey("room_type.id"), nullable=False)
    room_type: Mapped["RoomType"] = relationship(back_populates="room")
    message: Mapped[List["Message"]] = relationship(back_populates="room", cascade="all, delete")
    name: Mapped[str] = mapped_column(String(20), nullable=True)

class RoomType(Base):

    __tablename__ = "room_type"

    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[str] = mapped_column(String(20), nullable=False)
    room: Mapped[List["Room"]] = relationship(back_populates="room_type")

class Attachment(Base):
    __tablename__ = "attachment"

    id: Mapped[int] = mapped_column(primary_key=True)
    path: Mapped[str] = mapped_column(String, nullable=False)
    message: Mapped[List["Message"]] = relationship(back_populates="attachment")