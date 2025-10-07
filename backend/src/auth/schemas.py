"""All schemas for auth."""

from pydantic import BaseModel


class BaseUser(BaseModel):
    """Base user model."""

    username: str
    password: str


class RegisterUser(BaseUser):
    """Register new user."""

    confirm_password: str


class LoginUser(BaseUser):
    """Login user."""

    pass


class ResponseUser(BaseModel):
    """return user information."""

    username: str


class TokenResponse(BaseModel):
    """Token response."""

    access_token: str
    refresh_token: str
