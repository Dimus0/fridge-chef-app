from datetime import datetime,date
import uuid
from pydantic import BaseModel, Field
from typing import List, Optional

class ProductBase(BaseModel):
    product_name: str = Field(..., min_length=3, max_length=30)
    expiration_date: date

class ProductCreate(ProductBase):
    pass

class ProductRead(ProductBase):
    id: uuid.UUID
    user_id: uuid.UUID 

    class Config:
        from_attributes = True

class FridgeStatusResponse(BaseModel):
    expired: List[ProductRead]
    spoiling_soon: List[ProductRead]
    fresh: List[ProductRead]