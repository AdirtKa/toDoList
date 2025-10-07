"""All endpoints related to user authentication."""

from datetime import timedelta
from typing import TYPE_CHECKING, Annotated, Any

from fastapi import APIRouter, Depends, HTTPException, Response, Security, status
from fastapi_jwt import JwtAccessBearerCookie, JwtAuthorizationCredentials, JwtRefreshBearerCookie
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db
from src.utils.database import create_user, get_user_by_username

from ..config import settings
from .schemas import LoginUser, RegisterUser, ResponseUser, TokenResponse
from .security import hash_password, verify_password

if TYPE_CHECKING:
    from src.models.user import User

router: APIRouter = APIRouter(prefix='/auth', tags=['auth'])

access_security = JwtAccessBearerCookie(
    secret_key=settings.jwt_secret_key.get_secret_value(),
    algorithm=settings.jwt_algorithm,
    access_expires_delta=timedelta(seconds=settings.jwt_access_expires),
)

refresh_security = JwtRefreshBearerCookie(
    secret_key=settings.jwt_secret_key.get_secret_value(),
    algorithm=settings.jwt_algorithm,
    refresh_expires_delta=timedelta(seconds=settings.jwt_refresh_expires),
)


@router.post('/register', response_model=TokenResponse)
async def register(
    user: RegisterUser, db: Annotated[AsyncSession, Depends(get_db)], response: Response
) -> dict[str, Any]:
    """Register a new user and issue authentication tokens.

    This endpoint creates a new user account after verifying that:
    - The provided passwords match.
    - The username is not already registered.

    Upon successful registration, it returns both access and refresh JWT tokens
    and sets them as HTTP cookies in the response.

    Args:
        user (RegisterUser): The registration data provided by the client.
        db (AsyncSession): The active asynchronous SQLAlchemy database session.
        response (Response): The FastAPI response object used to set cookies.

    Returns:
        dict[str, Any]: A dictionary containing the issued access and refresh tokens.

    Raises:
        HTTPException: If the passwords do not match or the username is already registered.
    """
    if user.password != user.confirm_password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Passwords do not match',
        )

    user_in_db: User = await get_user_by_username(db, user.username)
    if user_in_db:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Username already registered')

    password_hash: str = hash_password(user.password)
    user = await create_user(db, user.username, password_hash)

    subject: dict[str, Any] = {'username': user.username}

    access_token = access_security.create_access_token(subject=subject)
    refresh_token = refresh_security.create_refresh_token(subject=subject)

    access_security.set_access_cookie(response, access_token)
    refresh_security.set_refresh_cookie(response, refresh_token)

    return {'access_token': access_token, 'refresh_token': refresh_token}


@router.post('/login', response_model=TokenResponse)
async def login(user: LoginUser, db: Annotated[AsyncSession, Depends(get_db)], response: Response) -> dict[str, str]:
    """Authenticate a user and return a JWT access token.

    This endpoint verifies the user's credentials against the database.
    If authentication succeeds, it issues a JWT access token that can be used
    to access protected routes.

    Args:
        user (User): The user credentials submitted in the request body.
        db (AsyncSession): The active SQLAlchemy asynchronous database session.
        response (Response): The response returned by the endpoint.

    Returns:
        dict[str, str]: A dictionary containing the generated access token.
    """
    user_in_db: User = await get_user_by_username(db, user.username)
    if not user_in_db:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User does not exist')

    if not verify_password(user.password, user_in_db.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Wrong Password')

    subject: dict[str, Any] = {'username': user.username}

    access_token = access_security.create_access_token(subject=subject)
    refresh_token = refresh_security.create_refresh_token(subject=subject)

    access_security.set_access_cookie(response, access_token)
    refresh_security.set_refresh_cookie(response, refresh_token)

    return {'access_token': access_token, 'refresh_token': refresh_token}


@router.get('/me', response_model=ResponseUser)
async def me(
    credentials: Annotated[JwtAuthorizationCredentials, Security(access_security)],
) -> dict[str, Any]:
    """Retrieve information about the currently authenticated user.

    Args:
        credentials (JwtAuthorizationCredentials): The user credentials submitted in the request body.

    Returns:
        None: Placeholder for user information (to be implemented).
    """
    if not credentials:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid credentials')

    subject = credentials.subject

    return {'username': subject.get('username')}
