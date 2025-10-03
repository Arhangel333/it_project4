import pytest
from app.main import tasks_db

# 🧪 ТЕСТ 1: Главная страница
def test_read_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Task Manager API с улучшениями!"}

# 🧪 ТЕСТ 2: Создание задачи
def test_create_task(client):
    task_data = {
        "title": "Тестовая задача",
        "description": "Это тест",
        "completed": False
    }
    
    response = client.post("/tasks/", json=task_data)
    
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Тестовая задача"
    assert data["description"] == "Это тест"
    assert data["completed"] == False
    assert "id" in data
    assert data["id"] == 1  # Первая задача

# 🧪 ТЕСТ 3: Получение всех задач
def test_get_tasks(client):
    # Сначала создаём задачу
    client.post("/tasks/", json={"title": "Задача 1"})
    client.post("/tasks/", json={"title": "Задача 2"})
    
    response = client.get("/tasks/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["title"] == "Задача 1"
    assert data[1]["title"] == "Задача 2"

# 🧪 ТЕСТ 4: Получение одной задачи
def test_get_task(client):
    # Создаём задачу
    create_response = client.post("/tasks/", json={"title": "Одна задача"})
    task_id = create_response.json()["id"]
    
    # Получаем её по ID
    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 200
    assert response.json()["title"] == "Одна задача"

# 🧪 ТЕСТ 5: Получение несуществующей задачи
def test_get_nonexistent_task(client):
    response = client.get("/tasks/999")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()

# 🧪 ТЕСТ 6: Обновление задачи
def test_update_task(client):
    # Создаём задачу
    create_response = client.post("/tasks/", json={"title": "Старое название"})
    task_id = create_response.json()["id"]
    
    # Обновляем
    update_data = {"title": "Новое название", "completed": True}
    response = client.put(f"/tasks/{task_id}", json=update_data)
    
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Новое название"
    assert data["completed"] == True

# 🧪 ТЕСТ 7: Удаление задачи
def test_delete_task(client):
    # Создаём задачу
    create_response = client.post("/tasks/", json={"title": "Для удаления"})
    task_id = create_response.json()["id"]
    
    # Удаляем
    response = client.delete(f"/tasks/{task_id}")
    assert response.status_code == 200
    
    # Проверяем что удалилась
    get_response = client.get(f"/tasks/{task_id}")
    assert get_response.status_code == 404

# 🧪 ТЕСТ 8: Статистика
def test_get_stats(client):
    # Создаём несколько задач
    client.post("/tasks/", json={"title": "Задача 1", "completed": True})
    client.post("/tasks/", json={"title": "Задача 2", "completed": False})
    
    response = client.get("/stats/")
    assert response.status_code == 200
    data = response.json()
    assert data["total_tasks"] == 2
    assert data["completed_tasks"] == 1
    assert data["pending_tasks"] == 1
    assert data["completion_rate"] == "50.0%"

# 🧪 ТЕСТ 9: Валидация данных (ошибка)
def test_create_task_validation_error(client):
    # Неправильные данные - нет title
    invalid_data = {
        "description": "Нет заголовка"  # нет обязательного title!
    }
    
    response = client.post("/tasks/", json=invalid_data)
    assert response.status_code == 422  # Ошибка валидации

# 🧪 ТЕСТ 10: Фильтрация задач
def test_filter_tasks(client):
    client.post("/tasks/", json={"title": "Выполненная", "completed": True})
    client.post("/tasks/", json={"title": "Невыполненная", "completed": False})
    
    # Только выполненные
    response = client.get("/tasks/?completed=true")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["title"] == "Выполненная"
    
    # Только невыполненные
    response = client.get("/tasks/?completed=false")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["title"] == "Невыполненная"