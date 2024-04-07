
from fastapi import UploadFile
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List, Optional
import os
import uuid

from app.models import Task
from app.core.logger_config import logger
from app.schemas.task import TaskResponse, TaskCreate, TasksResponse, TaskDownloadResponse
from app.core.config import settings
from job.tasks import process_video


def get_all_tasks_users(db: Session, max: Optional[int] = None, order: Optional[int] = 0) -> TasksResponse:
    try:
        tasks_query = db.query(Task)
        
        # Aplicar  ordenamiento
        if order == 1:
            logger.info('Se obtendrán las tareas ordenadas de forma descendente')
            tasks_query = tasks_query.order_by(Task.id.desc())
        else:
            logger.info('Se obtendrán las tareas ordenadas de forma ascendente')
            tasks_query = tasks_query.order_by(Task.id.asc())

        # Aplicar límite
        if max is not None:
            logger.info('Se obtendrán las primeras ' + str(max) + ' tareas')
            tasks_query = tasks_query.limit(max)
        
        tasks = tasks_query.all()

        task_responses = [TaskResponse(
            id=task.id,
            fileName=task.originalFileName,
            status=task.status
        ) for task in tasks]
        logger.info('Todas las tareas obtenidas: ' + str(len(task_responses)))
        return TasksResponse(result=task_responses)
    except Exception as e:
        logger.error('Error al obtener las tareas')
        logger.error(e)
        raise e



def get_all_tasks_by_user(db: Session, user: int, max: Optional[int] = None, order: Optional[int] = 0) -> TasksResponse:
    try:
        tasks_query = db.query(Task).filter(Task.owner_id == user)
        
        # Aplicar  ordenamiento
        if order == 1:
            logger.info('Se obtendrán las tareas ordenadas de forma descendente')
            tasks_query = tasks_query.order_by(Task.id.desc())
        else:
            logger.info('Se obtendrán las tareas ordenadas de forma ascendente')
            tasks_query = tasks_query.order_by(Task.id.asc())

        # Aplicar límite
        if max is not None:
            logger.info('Se obtendrán las primeras ' + str(max) + ' tareas')
            tasks_query = tasks_query.limit(max)
        
        tasks = tasks_query.all()

        task_responses = [TaskResponse(
            id=task.id,
            fileName=task.originalFileName,
            status=task.status
        ) for task in tasks]
        logger.info('Tareas obtenidas: ' + str(len(task_responses)))
        return TasksResponse(result=task_responses)
    except Exception as e:
        logger.error('Error al obtener las tareas')
        logger.error(e)
        raise e



def get_task_by_id(db: Session, task_id: int, user_id: int) -> TaskDownloadResponse:
    task = db.query(Task).filter(Task.id == task_id, Task.owner_id == user_id).first()
    if task:
        return TaskDownloadResponse(
                id=task.id,
                timeStamp=task.timeStamp.strftime('%Y-%m-%d %H:%M:%S'),
                fileName=task.originalFileName,
                video_processed_url=task.video_processed_url if task.status == 'processed' else '',
                status=task.status
            )
    return None

def delete_task_by_id(db: Session, task_id: int, user_id: int) -> bool:
    task = db.query(Task).filter(Task.id == task_id, Task.owner_id == user_id).first()
    if task:
        # ELIMINAR ARCHIVO DE VIDEO SI ESTA DISPONIBLE
        if task.status == 'processed':
            public_folder = os.getenv("BASE_URL", "http://localhost:8080")
            # video_url = "../public/uploaded/5a0f3089-bcc0-4d13-a922-3142feddf13d_editar-tag-sin-titulo.mp4"
            if task.video_url:
                video_url_relative  = task.video_url.replace(public_folder, "").replace("\\", "/")
                video_url_local = "." + os.path.join(os.path.dirname(os.path.realpath(__file__)), video_url_relative)
                #valida si el archivo existe
                print("Ruta del archivo a eliminar 1")
                print(video_url_local)
                if os.path.exists(video_url_local):
                    os.remove(video_url_local)

            if task.video_processed_url:
                processed_url_relative  = task.video_processed_url.replace(public_folder, "").replace("\\", "/")
                processed_url_local = "." + os.path.join(os.path.dirname(os.path.realpath(__file__)), processed_url_relative)
                print("Ruta del archivo a eliminar 2")
                print(processed_url_local)
                #valida si el archivo existe
                if os.path.exists(processed_url_local):
                    os.remove(processed_url_local)

       
            
            db.delete(task)
            db.commit()
            return True
    return False

def create_task_by_user(db: Session, user: int, file: UploadFile) -> bool:
    try:
        #VALIDAR QUE SEA UN VIDEO
        if file.content_type != 'video/mp4':
            return False

        # CREAR DIRECTORIO SI NO EXISTE
        if not os.path.exists(settings.PUBLIC_DIR_NOT_PROCESSED):
            os.makedirs(settings.PUBLIC_DIR_NOT_PROCESSED)

        unique_id = uuid.uuid4()
        # GENERAR UN IDENTIFICADOR UNICO DEL ARCHIVO SIN PROCESAR
        new_file_name = str(unique_id) + '_' + file.filename

        file_path = os.path.join(settings.PUBLIC_DIR_NOT_PROCESSED, new_file_name)
        proccessed_file_path = os.path.join(settings.PUBLIC_DIR_PROCESSED, new_file_name)
        with open(file_path, 'wb') as f:
            f.write(file.file.read())
        video_url = f"{settings.BASE_URL}/{file_path}".replace("\\", "/")
        video_processed_url = f"{settings.BASE_URL}/{proccessed_file_path}".replace("\\", "/")
        print(video_url)
        new_task = Task(
            originalFileName=file.filename,
            fileName=new_file_name,
            video_url=video_url,
            video_processed_url=video_processed_url,
            owner_id=user
        )
        db.add(new_task)
        db.commit()
        logger.info('Tarea creada con id -> ' + str(new_task.id))
        process_video.delay(new_task.id)
        return True
    except Exception as e:
        logger.error('Error al crear tarea')
        logger.error(e)
        db.rollback()
        return False