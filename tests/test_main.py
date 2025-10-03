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
