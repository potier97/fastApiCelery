from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, BigInteger
from sqlalchemy.orm import relationship
import bcrypt

from app.db.base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    email = Column(String(100), unique=True, index=True)
    hashed_password = Column(String)
    # country_id = Column(Integer, ForeignKey("countries.id"))
    
    # Relación con el pais del usuario
    # country = relationship("Country", back_populates="users")

    # Relación con los videos subidos por el usuario
    tareas = relationship("Task", back_populates="owner")
    # Contador de votos
    # votes = Column(BigInteger, default=0)

    def check_password(self, password: str) -> bool:
        """
        Verifica si la contraseña proporcionada coincide con la contraseña almacenada
        """
        return bcrypt.checkpw(password.encode('utf-8'), self.hashed_password.encode('utf-8'))

