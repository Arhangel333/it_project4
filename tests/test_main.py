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
    
    # ТЕСТ 1: Успешное создание задачи
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
    
    # ТЕСТ 2: Создание с минимальными данными (только title)
    minimal_task = {
        "title": "Минимальная задача"
    }
    
    response = client.post("/tasks/", json=minimal_task)
    assert response.status_code == 200
    
    data = response.json()
    assert data["title"] == "Минимальная задача"
    assert data["description"] is None  # должно быть None по умолчанию
    assert data["completed"] == False   # должно быть False по умолчанию
    
    # ТЕСТ 3: Создание выполненной задачи
    completed_task = {
        "title": "Выполненная задача",
        "completed": True
    }
    
    response = client.post("/tasks/", json=completed_task)
    assert response.status_code == 200
    
    data = response.json()
    assert data["completed"] == True
    
    # ТЕСТ 4: Проверяем что ID увеличиваются
    task1 = client.post("/tasks/", json={"title": "Задача 1"}).json()
    task2 = client.post("/tasks/", json={"title": "Задача 2"}).json()
    
    assert task2["id"] == task1["id"] + 1

def test_read_single_task_success(client):
    """Тест успешного получения одной задачи по ID"""
    # Создаём задачу
    task_data = {"title": "Тестовая задача для чтения", "description": "Описание"}
    create_response = client.post("/tasks/", json=task_data)
    task_id = create_response.json()["id"]
    
    # Читаем задачу
    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == task_id
    assert data["title"] == "Тестовая задача для чтения"
    assert data["description"] == "Описание"

def test_update_task_full(client):
    """Тест полного обновления задачи"""
    # Создаём задачу
    task = client.post("/tasks/", json={
        "title": "Старый заголовок",
        "description": "Старое описание",
        "completed": False
    }).json()
    
    # Полностью обновляем
    update_data = {
        "title": "Новый заголовок",
        "description": "Новое описание", 
        "completed": True
    }
    response = client.put(f"/tasks/{task['id']}", json=update_data)
    
    assert response.status_code == 200
    updated_task = response.json()
    assert updated_task["title"] == "Новый заголовок"
    assert updated_task["description"] == "Новое описание"
    assert updated_task["completed"] == True


def test_delete_task_verify_removed_from_list(client):
    """Тест что удалённая задача исчезает из общего списка"""
    # Получаем начальное количество задач
    initial_response = client.get("/tasks/")
    initial_tasks = initial_response.json()
    initial_count = len(initial_tasks)

    # Создаём несколько задач
    task1 = client.post("/tasks/", json={"title": "Задача 1"}).json()
    task2 = client.post("/tasks/", json={"title": "Задача 2"}).json()
    
    # Получаем начальный список
    initial_response = client.get("/tasks/")
    initial_tasks = initial_response.json()
    assert len(initial_tasks) == initial_count + 2
    
    # Удаляем одну задачу
    delete_response = client.delete(f"/tasks/{task1['id']}")
    assert delete_response.status_code == 200
    
    # Проверяем обновлённый список
    final_response = client.get("/tasks/")
    final_tasks = final_response.json()
    assert len(final_tasks) == initial_count + 1