from pydantic import BaseModel
from typing import List


class TaskCreate(BaseModel):
    filename: str


class TaskResponse(BaseModel):
    id: int
    fileName: str
    status: str

class TaskDownloadResponse(BaseModel):
    id: int
    timeStamp: str
    fileName: str
    video_processed_url: str
    status: str


class TasksResponse(BaseModel):
    result: List[TaskResponse]
