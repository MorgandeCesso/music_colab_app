from fastapi import Depends, FastAPI
from fastapi_users import FastAPIUsers, fastapi_users
from auth.base_config import auth_backend
from auth.manager import get_user_manager
from auth.schemas import UserCreate, UserRead
from database import User
from feed.router import router as router_feed
from chat.router import router as router_chat
app = FastAPI(title="Music colab app")

#Святая святых авторизации
fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

#Логин и логаут в одном лице
app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

#Регистрируемся тут
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

#Тут тратим своё драгоценное время (лента)
app.include_router(router_feed)

#Тут тратим чужое драгоценное время (чат)
app.include_router(router_chat)

#######################################

#Тут тестируем защиту (TBI)
current_user = fastapi_users.current_user()

@app.get("/unprotected-route")
def protected_route(user: User = Depends(current_user)):
    return f"Hello, someone!"

current_active_user = fastapi_users.current_user(active=True)

@app.get("/protected-route")
def protected_route(user: User = Depends(current_active_user)):
    return f"Hello, {user.nickname}!"

