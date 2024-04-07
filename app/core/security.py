from typing import Optional
from fastapi import HTTPException, Security, status, Depends, APIRouter
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
import jwt

from app.core.config import settings
from app.models import User
from app.db.session import SessionLocal, get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login", scheme_name="JWT")

# Función para verificar si el token JWT es válido
def verify_token(token: str = Security(oauth2_scheme), db: SessionLocal = Depends(get_db)) -> User:
    credentials_exception = HTTPException(
        status_code=401,
        detail="No se pudo validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        print('el token es: ', token)
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        print('el token es: ', username)
        if username is None:
            raise credentials_exception
        user = db.query(User).filter(User.username == username['username']).first()
        if user is None:
            raise credentials_exception
        return user
    except Exception as e:
        print(e)
        raise credentials_exception


