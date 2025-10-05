from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

# Базовая схема (общие поля для всех)
class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False

# Для создания задачи
class TaskCreate(TaskBase):
    pass

# Для обновления задачи
class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None

# Для чтения задачи
class Task(TaskBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)  # ← ИСПРАВЛЕНО!