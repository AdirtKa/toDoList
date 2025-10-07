"""All endpoints related to user authentication."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db
from src.models import User
from src.utils.database import get_user_by_username

from .security import verify_password

router: APIRouter = APIRouter(prefix='/auth', tags=['auth'])


@router.post('/login')
async def login(
    user: User,
    auth: Annotated[AuthJWT, Depends()],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> dict[str, str]:
    """Authenticate a user and return a JWT access token.

    This endpoint verifies the user's credentials against the database.
    If authentication succeeds, it issues a JWT access token that can be used
    to access protected routes.

    Args:
        user (User): The user credentials submitted in the request body.
        auth (AuthJWT): The FastAPI-JWT-Auth dependency for token creation.
        db (AsyncSession): The active SQLAlchemy asynchronous database session.

    Returns:
        dict[str, str]: A dictionary containing the generated access token.
    """
    user_in_db: User = await get_user_by_username(db, user.username)
    if not user_in_db:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User does not exist')

    if not verify_password(user.password, user_in_db.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Wrong Password')

    access_token = auth.create_access_token(subject=user.username)
    return {'access_token': access_token}


@router.get('/me')
async def get_me(
    auth: Annotated[AuthJWT, Depends()],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> None:
    """Retrieve information about the currently authenticated user.

    Args:
        auth (AuthJWT): The FastAPI-JWT-Auth dependency used to validate the token.
        db (AsyncSession): The active SQLAlchemy asynchronous database session.

    Returns:
        None: Placeholder for user information (to be implemented).
    """
    pass
