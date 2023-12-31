from typing import Optional
from fastapi_users import schemas

#Это мы отправляем
class UserRead(schemas.BaseUser[int]):
    id: int
    given_name: str
    surname: str
    nickname: str
    email: str
    role_id: int
    picture_id: int
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False
    
    class Config:
        orm_mode = True

#Это мы получаем
class UserCreate(schemas.BaseUserCreate):
    given_name: str
    surname: str
    nickname: str
    email: str
    password: str
    role_id: int
    picture_id: int
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False