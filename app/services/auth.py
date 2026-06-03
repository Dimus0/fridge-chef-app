from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordRequestForm
from pwdlib import PasswordHash
from jose import JWTError, jwt

from app.schemas.user import CreateUserRequest
from app.models.user import User

# Глобальні конфігурації залишаються на рівні модуля (або виносяться в .env)
SECRET_KEY = "4f6d8c2b91a7e53fd4c1b8e9f2a76b4d9c3e1f8a5b7c2d6e9f1a4b8c7d3e5f2"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
password_hash = PasswordHash.recommended()


class AuthService:
    def __init__(self, db: AsyncSession):
        self.db = db

    def _create_access_token(self, username: str, user_id: str, expires_delta: timedelta) -> str:
        encode = {"sub": username, "id": user_id}
        expires = datetime.now(timezone.utc) + expires_delta
        encode.update({"exp": expires})
        return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

    async def create_user(self, user_request: CreateUserRequest) -> dict:
        if len(user_request.password.encode("utf-8")) > 72:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="Password must be at most 72 characters long"
            )
        
        hashed_password = password_hash.hash(user_request.password)

        create_user_model = User(
            username=user_request.username,
            email=user_request.email,
            password=hashed_password,
        )

        self.db.add(create_user_model)
        await self.db.commit()
        await self.db.refresh(create_user_model)

        return {"status": "User created successfully"}

    async def login_for_access_token(self, form_data: OAuth2PasswordRequestForm) -> dict:
        result = await self.db.execute(select(User).where(User.username == form_data.username))
        user = result.scalars().first()

        if not user or not password_hash.verify(form_data.password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail="Incorrect username or password"
            )

        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = self._create_access_token(
            username=user.username, 
            user_id=str(user.id), 
            expires_delta=access_token_expires
        )

        return {"access_token": access_token, "token_type": "bearer"}

    async def get_current_user(self, token: str) -> User:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username: str = payload.get("sub")
            user_id: str = payload.get("id")
            if username is None or user_id is None:
                raise credentials_exception
        except JWTError:
            raise credentials_exception
        
        result = await self.db.execute(select(User).where(User.id == user_id))
        user = result.scalars().first()

        if user is None:
            raise credentials_exception
        return user