from fastapi import APIRouter, HTTPException, Path, Depends
from typing import List, Optional
from sqlalchemy.orm import Session
from app.core.logger_config import logger

from app.models import Country
from app.db.session import get_db
from app.services.countries import get_countries_service, get_country_by_id_service

router = APIRouter()

@router.post("/")
def get_countries(db: Session = Depends(get_db)):
    try:
        logger.info('Obteniendo todos los países')
        countries = get_countries_service(db)
        return countries
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Error al obtener los países")

@router.get("/{country_id}")
def get_country(country_id: int, db: Session = Depends(get_db)):
    logger.info('Buscando país por id ' + str(country_id))
    country = get_country_by_id_service(country_id, db)
    if country is None:
        logger.error('País no encontrado')
        raise HTTPException(status_code=404, detail="País no encontrado")
    return country

