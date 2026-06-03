import uuid

from pydantic import BaseModel, ConfigDict, EmailStr, Field

class UserBase(BaseModel):
    username: str = Field(..., min_length=2, max_length=255,description="The username of the user")
    email: EmailStr = Field(..., min_length=2, max_length=255,description="The email of the user")

class UserCreate(UserBase):
    password: str = Field(..., min_length=6, max_length=100, description="Пароль користувача")

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserRead(UserBase):
    id: uuid.UUID

    class Config:
        from_attributes = True

class CreateUserRequest(BaseModel):
    username: str
    email: str
    password: str