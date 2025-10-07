"""All endpoints for auth."""

from fastapi import APIRouter

router: APIRouter = APIRouter(prefix='/auth', tags=['auth'])
