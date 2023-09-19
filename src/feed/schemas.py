from pydantic import BaseModel
from typing import Optional

#Чисто для создания поста, "самое важное, самое нужное"
class PostCreate(BaseModel):
    user_id: int
    tack_id: int
    descripton: str
    price: Optional[int] = None
