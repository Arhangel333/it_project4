import pytest
from fastapi.testclient import TestClient
from app.main import app

# ФИКСТУРА - создаёт тестового клиента
@pytest.fixture
def client():
    return TestClient(app)

