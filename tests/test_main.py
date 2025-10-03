from app.main import app
from app.database import SessionLocal

def test_app_exists():
    """Проверяем что приложение создано"""
    assert app is not None

def test_app_title():
    """Проверяем заголовок приложения"""
    assert app.title == "FastAPI"  # или ваше название

def test_database_connection():
    """Проверяем подключение к БД"""
    db = SessionLocal()
    try:
        # Простая проверка что сессия работает
        result = db.execute("SELECT 1")
        assert result.scalar() == 1
    finally:
        db.close()
