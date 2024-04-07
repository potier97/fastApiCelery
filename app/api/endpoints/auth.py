from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session


from app.models import User
from app.db.session import get_db 
from app.schemas.auth import SignupRequest, LoginRequest
from app.core.logger_config import logger
from app.services.auth import signup_service, login_service

router = APIRouter()


@router.post("/signup")
async def signup(request: SignupRequest, db: Session = Depends(get_db)):
    errorExeption = {
        "status_code": 500,
        "detail": "Error al procesar la solicitud de registro"
    }
    try:
        logger.info('Creando cuenta de usuario con correo -> ' + request.email)
        result = await signup_service(request, db)
        return dict({"message": "La cuenta ha sido creada exitosamente", "result": result})
    except ValueError as ve:
        logger.error('Error al procesar la solicitud de registro: ' + str(ve))
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        logger.error('Error al procesar la solicitud de registro')
        logger.error(e)
        raise HTTPException(errorExeption["status_code"], detail=errorExeption["detail"])

@router.post("/login")
async def login(request: LoginRequest, db: Session = Depends(get_db)):
    errorExeption = {
        "status_code": 500,
        "detail": "Error al ingresar"
    }
    try:
        logger.info('Ingresando con correo -> ' + request.email)
        result = await login_service(request, db)
        return dict({"message": "ha ingresado correctamente", "jwt": result, "user": request.email})
    except ValueError as ve:
        logger.error('Credenciales incorrectas: ' + str(ve))
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")
    except Exception as e:
        logger.error('Error al ingresar')
        logger.error(e)
        raise HTTPException(errorExeption["status_code"], detail=errorExeption["detail"])