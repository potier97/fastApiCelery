from celery import Celery
from job import celeryconfig

# # Configuración de Celery
celery = Celery('celery_app')
celery.config_from_object('job.celeryconfig')