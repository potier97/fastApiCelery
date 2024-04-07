from fastapi import APIRouter
from app.api.endpoints import tasks

router = APIRouter()

router.include_router(tasks.router, prefix="/api/tasks", tags=["Tasks"], responses={404: {"description": "Not found"}})