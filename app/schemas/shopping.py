import uuid
from pydantic import BaseModel, Field

class ShopingItemBase(BaseModel):
    item_name: str = Field(..., min_length=3, max_length=100, description="Назва товару")

class ShoppingItemCreate(ShopingItemBase):
    pass

class ShoppingItemRead(ShopingItemBase):
    id: uuid.UUID
    user_id: uuid.UUID
    is_bought: bool

    class Config:
        from_attribuets = True