from datetime import datetime
import uuid
from pydantic import BaseModel, Field
from typing import List, Optional

class RecipeBase(BaseModel):
    title: str = Field(..., min_length=3, max_length=150)
    ingredients: str  
    instruction: str 
    prep_time: int = Field(..., ge=1) 

class RecipeCreate(RecipeBase):
    pass

class RecipeUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=3, max_length=150)
    ingredients: Optional[str] = None
    instruction: Optional[str] = None
    prep_time: Optional[int] = Field(default=None, ge=1)

class RecipeRead(RecipeBase):
    id: uuid.UUID
    user_id: uuid.UUID 
    created_at: datetime
    
    class Config:
        from_attributes = True

class RecipeGenerateRequest(BaseModel):
    ingredients: List[str] = Field(..., min_length=1)


class RecipeGenerateResponse(RecipeBase):
    pass