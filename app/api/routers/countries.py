from fastapi import APIRouter
from app.api.endpoints import countries

router = APIRouter()

router.include_router(countries.router, prefix="/api/countries", tags=["Countries"], responses={404: {"description": "Not found"}})