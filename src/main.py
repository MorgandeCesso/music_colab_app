from fastapi import Depends, FastAPI
from fastapi_users import FastAPIUsers, fastapi_users
from auth.base_config import auth_backend
from auth.manager import get_user_manager
from auth.schemas import UserCreate, UserRead
from database import User
from feed.router import router as router_feed
app = FastAPI(title="Music colab app")

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(router_feed)

current_user = fastapi_users.current_user()

@app.get("/unprotected-route")
def protected_route(user: User = Depends(current_user)):
    return f"Hello, someone!"

current_active_user = fastapi_users.current_user(active=True)

@app.get("/protected-route")
def protected_route(user: User = Depends(current_active_user)):
    return f"Hello, {user.nickname}!"

