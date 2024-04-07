from sqlalchemy import Column, Integer, String, ForeignKey, BigInteger, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from app.db.base import Base

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    fileName = Column(String(250))
    originalFileName = Column(String(250))
    timeStamp = Column(DateTime, default=datetime.utcnow)
    video_url = Column(String)
    video_processed_url = Column(String)
    owner_id = Column(Integer, ForeignKey("users.id"))
    # uploaded -> El video ha sido subido
    # processed -> El video ha sido aprobado
    status = Column(String, default="uploaded")

    # Relación con el propietario del video
    owner = relationship("User", back_populates="tareas")

    # Contador de votos
    # votes = Column(BigInteger, default=0)
