from app.main import app
from app.database import SessionLocal
from sqlalchemy import text

def test_app_exists():
    """Проверяем что приложение создано"""
    assert app is not None

def test_app_title():
    """Проверяем заголовок приложения"""
    assert app.title == "Task Manager API"

def test_database_connection():
    """Проверяем подключение к БД"""
    db = SessionLocal()
    try:
        # Простая проверка что сессия работает
        result = db.execute(text("SELECT 1"))
        assert result.scalar() == 1
    finally:
        db.close()


def test_create_task_comprehensive(client):
    """
    Комплексный тест создания задачи:
    - Проверяем успешное создание
    - Проверяем обязательные поля
    - Проверяем значения по умолчанию
    - Проверяем возвращаемую структуру
    """
    
    # 🟢 ТЕСТ 1: Успешное создание задачи
    task_data = {
        "title": "Новая задача для тестирования",
        "description": "Подробное описание задачи",
        "completed": False
    }
    
    response = client.post("/tasks/", json=task_data)
    
    # Проверяем статус
    assert response.status_code == 200
    
    # Проверяем структуру ответа
    data = response.json()
    assert "id" in data
    assert data["title"] == "Новая задача для тестирования"
    assert data["description"] == "Подробное описание задачи"
    assert data["completed"] == False
    assert "created_at" in data
    assert data["updated_at"] is None
    
    # 🟢 ТЕСТ 2: Создание с минимальными данными (только title)
    minimal_task = {
        "title": "Минимальная задача"
    }
    
    response = client.post("/tasks/", json=minimal_task)
    assert response.status_code == 200
    
    data = response.json()
    assert data["title"] == "Минимальная задача"
    assert data["description"] is None  # должно быть None по умолчанию
    assert data["completed"] == False   # должно быть False по умолчанию
    
    # 🟢 ТЕСТ 3: Создание выполненной задачи
    completed_task = {
        "title": "Выполненная задача",
        "completed": True
    }
    
    response = client.post("/tasks/", json=completed_task)
    assert response.status_code == 200
    
    data = response.json()
    assert data["completed"] == True
    
    # 🟢 ТЕСТ 4: Проверяем что ID увеличиваются
    task1 = client.post("/tasks/", json={"title": "Задача 1"}).json()
    task2 = client.post("/tasks/", json={"title": "Задача 2"}).json()
    
    assert task2["id"] == task1["id"] + 1