

from pydantic import BaseModel


class PostCreate(BaseModel):
    user_id: int
    tack_id: int
    descripton: str
    price: int
