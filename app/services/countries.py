from sqlalchemy.orm import Session
from typing import List, Optional
from app.models import Country

from app.models import Country

def get_countries_service(db: Session):
    countries = db.query(Country).all()
    return countries

def get_country_by_id_service(country_id: int, db: Session):
    country = db.query(Country).filter(Country.id == country_id).first()
    return country
