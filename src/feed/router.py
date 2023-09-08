from fastapi import APIRouter, Depends
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_async_session
from auth.models import Post
from feed.schemas import PostCreate

router = APIRouter(
    prefix="/feed",
    tags=["Feed"]
)


@router.get("/posts/{post_id}")
async def get_post(post_id: int, session: AsyncSession = Depends(get_async_session)):
    query = select(Post).where(Post.id == post_id)
    print(query)
    post = await session.execute(query)
    return post.mappings().all()

@router.post("/create_post")
async def create_post(new_post: PostCreate, session: AsyncSession = Depends(get_async_session)):
    statement = insert(Post).values(**new_post.model_dump())
    await session.execute(statement)
    await session.commit()
    return {"status": "success"}

@router.get("/posts")
async def get_posts(upper_limit: int, lower_limit: int, session: AsyncSession = Depends(get_async_session)):
    if lower_limit == None:
        lower_limit = select(Post.id).order_by(Post.id.desc())[-1]
    if lower_limit < upper_limit:
        raise {"status": "lower limit cannot be smaller than upper!"}
    if upper_limit <= 0 or lower_limit <= 0:
        raise {"status": "limits cannot be below zero or equal to it!"}
    query = select(Post).where(Post.id <= lower_limit, Post.id > upper_limit).order_by(Post.post_date)
    print(query)
    posts = await session.execute(query)
    return posts.mappings().all()