"""Entrypoint file."""

from typing import Any

from fastapi import APIRouter, FastAPI

from src.auth import router as auth_router

app: FastAPI = FastAPI(
    title='ToDoList API',
    version='1.0.0',
    docs_url='/api/docs',  # Swagger UI
    redoc_url='/api/redoc',  # ReDoc (альтернативная документация)
    openapi_url='/api/openapi.json',  # JSON-схема OpenAPI
)
router: APIRouter = APIRouter(prefix='/api')
router.include_router(auth_router)


@router.get('/healthcheck')
async def root() -> dict[str, Any]:
    """Health check endpoint."""
    return {'message': 'Hello World'}


app.include_router(router)
