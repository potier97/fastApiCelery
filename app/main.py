from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import inspect
import os
import shutil
# CONFIG
from app.core.config import settings
from app.db.session import engine
from app.db.base import Base
from app.core.logger_config import logger
#RUTAS DEL API
from app.api.routers import auth, tasks
from app.models import Country, User, Task
# Crea una instancia de FastAPI
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description=settings.APP_DESCRIPTION,
    debug=settings.DEBUG
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_HOSTS or ["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)


# Montar el directorio estático en la aplicación
app.mount('/' + settings.PUBLIC_DIR, StaticFiles(directory=settings.PUBLIC_DIR), name="public")

# Conexión a la base de datos
@app.on_event("startup")
async def startup():
    # Ejemplo de uso del logger
    logger.info('Levantando la aplicación en el puerto 8000')
    logger.info('Estado debug: ' + str(settings.DEBUG))
    inspector = inspect(engine)
    existing_tables = inspector.get_table_names()
    if not existing_tables:
        Base.metadata.create_all(bind=engine)
    else:
        logger.info('Las tablas ya existen en la base de datos.')

# # desconexión de la base de datos  
@app.on_event("shutdown")
async def shutdown():
    logger.info('Apagando la aplicación')
    #DESCOMENTAR EN PRUEBAS
    if settings.DEBUG:
        Base.metadata.drop_all(bind=engine)
        logger.info('Tablas eliminadas de la base de datos')
        if os.path.exists(settings.PUBLIC_DIR_NOT_PROCESSED):
            for filename in os.listdir(settings.PUBLIC_DIR_NOT_PROCESSED):
                file_path = os.path.join(settings.PUBLIC_DIR_NOT_PROCESSED, filename)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                except Exception as e:
                    print(f"No se pudo eliminar {file_path}. Error: {e}")

        if os.path.exists(settings.PUBLIC_DIR_PROCESSED):
            for filename in os.listdir(settings.PUBLIC_DIR_PROCESSED):
                file_path = os.path.join(settings.PUBLIC_DIR_PROCESSED, filename)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                except Exception as e:
                    print(f"No se pudo eliminar {file_path}. Error: {e}")


# Health Check
@app.get("/")
def read_root():
    return {"hello": "world"}
    
app.include_router(tasks.router)
app.include_router(auth.router)
