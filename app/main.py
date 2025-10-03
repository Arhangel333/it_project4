from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from app import crud, models, schemas
from app.database import SessionLocal, engine, get_db

# СОЗДАЁМ ТАБЛИЦЫ В БАЗЕ ДАННЫХ
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Task Manager API")

# CREATE - создание задачи
@app.post("/tasks/", response_model=schemas.Task)
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    return crud.create_task(db=db, task=task)

# READ - все задачи с фильтрацией
@app.get("/tasks/", response_model=List[schemas.Task])
def read_tasks(
    skip: int = 0,
    limit: int = 100,
    completed: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    tasks = crud.get_tasks(db, skip=skip, limit=limit)
    
    # Фильтрация по статусу
    if completed is not None:
        tasks = [task for task in tasks if task.completed == completed]
    
    return tasks

# READ - одна задача
@app.get("/tasks/{task_id}", response_model=schemas.Task)
def read_task(task_id: int, db: Session = Depends(get_db)):
    db_task = crud.get_task(db, task_id=task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task

# UPDATE - обновление задачи
@app.put("/tasks/{task_id}", response_model=schemas.Task)
def update_task(task_id: int, task: schemas.TaskUpdate, db: Session = Depends(get_db)):
    db_task = crud.get_task(db, task_id=task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return crud.update_task(db=db, task_id=task_id, task=task)

# DELETE - удаление задачи
@app.delete("/tasks/{task_id}", response_model=schemas.Task)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    db_task = crud.get_task(db, task_id=task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return crud.delete_task(db=db, task_id=task_id)

# STATS - статистика
@app.get("/stats/")
def get_stats(db: Session = Depends(get_db)):
    tasks = crud.get_tasks(db)
    total = len(tasks)
    completed = len([task for task in tasks if task.completed])
    pending = total - completed
    
    return {
        "total_tasks": total,
        "completed_tasks": completed,
        "pending_tasks": pending,
        "completion_rate": f"{(completed/total*100):.1f}%" if total > 0 else "0%"
    }

# HOME
@app.get("/")
def home():
    return {"message": "Task Manager API с PostgreSQL!"}

# HEALTH
@app.get("/health")
def health_check(db: Session = Depends(get_db)):
    tasks_count = len(crud.get_tasks(db))
    return {
        "status": "OK", 
        "tasks_count": tasks_count,
        "version": "2.0.0",
        "database": "PostgreSQL"
    }