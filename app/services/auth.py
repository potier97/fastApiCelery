from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta
import re
import bcrypt
from jose import jwt

from app.core.logger_config import logger
from app.models import User
from app.models import User
from app.schemas.auth import SignupRequest, LoginRequest
from app.core.config import settings

async def signup_service(request: SignupRequest, db: Session) -> bool:
    if not request.username:
        logger.error('El nombre de usuario no puede estar vacío')
        #devolver solo mensaje de error
        raise ValueError("El nombre de usuario no puede estar vacío")

    # Verificar que las contraseñas coincidan
    if request.password1 != request.password2:
        logger.error('Las contraseñas no coinciden')
        raise ValueError("Las contraseñas no coinciden")    

    if not is_secure_password(request.password1):
        error_message = 'La contraseña no cumple con los requisitos mínimos de seguridad'
        logger.error(error_message)
        raise ValueError(error_message)

    if not isValidEmail(request.email):
        error_message = 'El correo electrónico no es válido'
        logger.error(error_message)
        raise ValueError(error_message)

    if user_exists_in_database(request.username, db):
        error_message = 'El nombre de usuario ya existe'
        logger.error(error_message)
        raise ValueError(error_message)

    if email_exists_in_database(request.email, db):
        error_message = 'El correo electrónico ya está registrado'
        logger.error(error_message)
        raise ValueError(error_message)

    # Encriptar la contraseña
    hashed_password = hash_password(request.password1)

    # Crear el usuario
    new_user = User(username=request.username, email=request.email, hashed_password=hashed_password)

    logger.info('Creando usuario en la base de datos')

    # Asignar la contraseña encriptada
    db.add(new_user)

    # Confirmar
    db.commit()

    logger.info('Usuario creado exitosamente')

    return True

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')
    

def isValidEmail(email: str) -> bool:
    email_validate_pattern = r"^\S+@\S+\.\S+$"
    return re.match(email_validate_pattern, email)

def user_exists_in_database(username: str, db: Session) -> bool:
    db_user = db.query(User).filter(User.username == username).first()
    if db_user:
        return True
    return False

def email_exists_in_database(email: str, db: Session) -> bool:
    db_user = db.query(User).filter(User.email == email).first()
    if db_user:
        return True
    return False  # Simulado, siempre devuelve falso

def is_secure_password(password: str) -> bool:
    isSecure = True
    #mínimo 8 caracteres
    isSecure = len(password) >= 8
    # verifiar regex si tiene numero
    isSecure = re.search(r"\d", password) is not None
    # verifiar regex si tiene mayuscula
    isSecure = re.search(r"[A-Z]", password) is not None
    # verifiar regex si tiene minuscula
    isSecure = re.search(r"[a-z]", password) is not None
    return isSecure


## ================================================
## =================== LOGIN SERVICE ==============
## ================================================


async def login_service(request: LoginRequest, db: Session) -> str:
    db_user = db.query(User).filter(User.email == request.email).first()
    if not db_user:
        logger.error("Credenciales inválidas")
        raise ValueError("Credenciales inválidas")    

    if not db_user.check_password(request.password) or db_user.email != request.email:
        logger.error("Credenciales inválidas")
        raise ValueError("Credenciales inválidas")    

    logger.info("Usuario autenticado")
    
    # Generar el token de acceso
    access_token = create_access_token({ "id": db_user.id, "username": db_user.username})
        
    return access_token

def create_access_token(data: dict) -> str:
    data = {"sub": data }
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = data.copy()
    to_encode.update({"exp": datetime.utcnow() + access_token_expires})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt