from celery.schedules import crontab

beat_conf = {
    "task_1": {
        "task": "job.tasks.add",
        "schedule": crontab(minute="*/1"),
    }
}