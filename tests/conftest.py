import pytest
from fastapi.testclient import TestClient
from app.main import app

# 🎯 ФИКСТУРА - создаёт тестового клиента
@pytest.fixture
def client():
    return TestClient(app)

# 🎯 ФИКСТУРА - очищает базу перед каждым тестом
@pytest.fixture(autouse=True)
def clean_tasks():
    # Временное решение - пока у нас нет нормальной тестовой БД
    from app.main import tasks_db
    tasks_db.clear()
    yield
    tasks_db.clear()