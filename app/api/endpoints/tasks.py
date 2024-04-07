from fastapi import APIRouter, HTTPException, Depends, UploadFile, File
from datetime import datetime, timedelta
from typing import List, Optional
from sqlalchemy.orm import Session

from app.core.logger_config import logger
from app.models import User, Task
from app.schemas.task import TaskResponse, TaskCreate, TasksResponse, TaskDownloadResponse
from app.db.session import get_db 
from app.core.security import verify_token
from app.services.tasks import get_all_tasks_by_user, get_task_by_id, delete_task_by_id, create_task_by_user, get_all_tasks_users


router = APIRouter()

@router.get("/all", response_model=TasksResponse)
async def get_all_tasks(max: Optional[int] = None, order: Optional[int] = 0, db: Session = Depends(get_db), current_user: User = Depends(verify_token)):
    try:
        logger.info('Obteniendo todas las tareas existentes')
        tasks = get_all_tasks_users(db, max, order)
        return tasks
    except Exception as e:
        logger.error('Error al obtener las tareas')
        logger.error(e)
        raise HTTPException(status_code=500, detail="Error al obtener las tareas")



@router.get("/", response_model=TasksResponse)
async def get_all_our_tasks(max: Optional[int] = None, order: Optional[int] = 0, db: Session = Depends(get_db), current_user: User = Depends(verify_token)):
    try:
        logger.info('Obteniendo tareas del usuario -> ' + current_user.username)
        tasks = get_all_tasks_by_user(db, current_user.id, max, order)
        return tasks
    except Exception as e:
        logger.error('Error al obtener las tareas')
        logger.error(e)
        raise HTTPException(status_code=500, detail="Error al obtener las tareas")



@router.post("/", response_model=dict)
async def create_task(file: UploadFile = File(), db: Session = Depends(get_db), current_user: User = Depends(verify_token)):
    errorExeption = {
        "status_code": 500,
        "detail": "Error al crear la tarea"
    }
    try:
        #print(file)
        logger.info('Creando tarea para usuario -> ' + current_user.username)
        result = create_task_by_user(db, current_user.id, file)
        #print('result ' + str(result))
        if not result:
            logger.error('Error al crear tarea')
            errorExeption["status_code"] = 400
            errorExeption["detail"] = "No se pudo crear la tarea"
            raise ValueError('No se pudo crear la tarea')
        return {"message": "Tarea en proceso", "result": True}
    except Exception as e:
        logger.error('Error al crear tarea')
        logger.error(e)
        raise HTTPException(errorExeption["status_code"], detail=errorExeption["detail"])



@router.get("/{id_task}", response_model=TaskDownloadResponse)
def get_task(id_task: int, db: Session = Depends(get_db), current_user: User = Depends(verify_token)):
    errorExeption = {
        "status_code": 500,
        "detail": "Error al obtener una tarea"
    }
    try:
        logger.info('Obteniendo tarea por id -> ' + str(id_task))
        task = get_task_by_id(db, id_task, current_user.id)
        if task is None:
            logger.error('Tarea no encontrada')
            errorExeption["status_code"] = 404
            errorExeption["detail"] = "Tarea no encontrada"
            raise ValueError('Tarea no encontrada')
        return task
    except Exception as e:
        logger.error('Error al obtener tarea')
        logger.error(e)
        raise HTTPException(errorExeption["status_code"], detail=errorExeption["detail"])



@router.delete("/{id_task}")
async def delete_task_endpoint(id_task: int, db: Session = Depends(get_db), current_user: User = Depends(verify_token)):
    errorExeption = {
        "status_code": 500,
        "detail": "Error al eliminar la tarea"
    }
    try:
        logger.info('Eliminando tarea por id -> ' + str(id_task))
        deleted = delete_task_by_id(db, id_task, current_user.id)
        if deleted:
            logger.info('Tarea eliminada correctamente')
        else:
            logger.error('Tarea no encontrada')
            errorExeption["status_code"] = 404
            errorExeption["detail"] = "Tarea no encontrada"
            raise ValueError('Tarea no encontrada')
    except Exception as e:
        logger.error('Error al eliminar tarea')
        logger.error(e)
        raise HTTPException(errorExeption["status_code"], detail=errorExeption["detail"])