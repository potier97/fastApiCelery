import logging
import time
import subprocess
from job.celery_app import celery
from job.converter_test import ejecutar_script_sh


logger = logging.getLogger(__name__)

@celery.task
def add():
    logger.info('Adding two numbers')
    print('Adding two numbers')

@celery.task(max_retries=3)
def process_video(taks_id):
    logger.info('Processing video with id: ' + str(taks_id))
    time.sleep(0.5)
    ejecutar_script_sh(taks_id)
    

