from typing import Annotated
from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_async_session
from app.schemas.user import CreateUserRequest
from app.schemas.token import Token
from app.services.auth import AuthService

router = APIRouter(
    prefix="/auth", 
    tags=["auth"]
)

db_dependency = Annotated[AsyncSession, Depends(get_async_session)]
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/login")


def get_auth_service(db: db_dependency) -> AuthService:
    return AuthService(db)

auth_service_dependency = Annotated[AuthService, Depends(get_auth_service)]

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(user_request: CreateUserRequest, auth_service: auth_service_dependency):
    return await auth_service.create_user(user_request)


@router.post("/login", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], 
    auth_service: auth_service_dependency
):
    return await auth_service.login_for_access_token(form_data)


async def get_current_user_dependency(
    token: Annotated[str, Depends(oauth2_bearer)], 
    auth_service: auth_service_dependency
):
    return await auth_service.get_current_user(token)