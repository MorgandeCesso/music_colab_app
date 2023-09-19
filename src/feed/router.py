from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import insert, select, delete
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_async_session
from auth.models import Post, User
from feed.schemas import PostCreate

#Непосредственно роутер
router = APIRouter(
    prefix="/feed",
    tags=["Feed"]
)

#Хочу конкретный пост
@router.get("/{post_id}")
async def get_post(post_id: int, session: AsyncSession = Depends(get_async_session)):
    query = select(Post).where(Post.id == post_id).options(joinedload(Post.track), joinedload(Post.user).load_only(User.nickname))
    print(query)
    post = await session.execute(query)
    return post.mappings().all()

#Хочу запостить
@router.post("/create_post")
async def create_post(new_post: PostCreate, session: AsyncSession = Depends(get_async_session)):
    statement = insert(Post).values(**new_post.model_dump())
    await session.execute(statement)
    await session.commit()
    return {"status": "success"}

#Хочу N постов
@router.get("/")
async def get_posts(upper_limit: int, lower_limit: int, session: AsyncSession = Depends(get_async_session)):
    if (lower_limit == None):
        lower_limit = select(Post.id).order_by(Post.id.desc())[-1]
    if (lower_limit < upper_limit):
        raise HTTPException(status_code=500, detail="Lower limit cannot be smaller than upper!")
    if (upper_limit <= 0) or (lower_limit <= 0):
        raise HTTPException(status_code=500, detail="Limits cannot be below zero or equal to it!")
    query = select(Post).where(Post.id < lower_limit, Post.id >= upper_limit)\
        .options(joinedload(Post.track), joinedload(Post.user).load_only(User.nickname)).order_by(Post.post_date)
    print(query)
    posts = await session.execute(query)
    return posts.mappings().all()

#Хочу снести
@router.delete("/delete_post/{post_id}")
async def delete_post(post_id: int, session: AsyncSession = Depends(get_async_session)):
    statement = delete(Post).where(Post.id == post_id)
    print(statement)
    await session.execute(statement)
    await session.commit()
    return {"status": "success"}