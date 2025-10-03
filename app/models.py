from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime
from sqlalchemy.sql import func
from .database import Base

class Task(Base):
    __tablename__ = "tasks"  # имя таблицы в БД

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)  # обязательное поле
    description = Column(Text)  # необязательное поле
    completed = Column(Boolean, default=False)  # по умолчанию False
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())