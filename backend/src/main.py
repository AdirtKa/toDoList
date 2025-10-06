"""Entrypoint file."""

from typing import Any

from fastapi import APIRouter, FastAPI

app: FastAPI = FastAPI()
router: APIRouter = APIRouter(prefix='/api')


@router.get('/healthcheck')
async def root() -> dict[str, Any]:
    """Health check endpoint."""
    return {'message': 'Hello World'}


app.include_router(router)
