
# 🚀 Task Manager API

FastAPI приложение для управления задачами с PostgreSQL, Docker, тестами и CI/CD.

## 📋 О проекте

REST API для управления задачами с полным набором CRUD операций, валидацией данных и автоматическим тестированием.

## 🛠 Технологии

- **FastAPI** - современный Python фреймворк для API
- **PostgreSQL** - реляционная база данных
- **SQLAlchemy 2.0** - ORM для работы с БД
- **Docker** - контейнеризация приложения
- **Pytest** - модульное тестирование
- **Pydantic** - валидация данных
- **GitHub/GitLab** - CI/CD пайплайны

## 🚀 Быстрый старт

### Предварительные требования
- Docker
- Docker Compose

### Запуск проекта

```bash
# Клонируйте репозиторий
git clone https://github.com/Arhangel333/it_project4.git
cd it_project4

# Запустите приложение
docker-compose up -d
```
Приложение будет доступно по адресу: http://localhost:8000

📚 API Документация

После запуска доступны:

· Swagger UI: http://localhost:8000/docs  
· ReDoc: http://localhost:8000/redoc

🎯 API Эндпоинты

Задачи (Tasks)

Метод URL Описание
GET /tasks/ Получить список задач
GET /tasks/{id} Получить задачу по ID
POST /tasks/ Создать новую задачу
PUT /tasks/{id} Обновить задачу
DELETE /tasks/{id} Удалить задачу

Дополнительные эндпоинты

Метод URL Описание
GET /stats/ Статистика по задачам
GET /health Проверка здоровья приложения

📊 Примеры запросов

Создание задачи

```bash
curl -X POST "http://localhost:8000/tasks/" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Изучить FastAPI",
    "description": "Освоить создание REST API",
    "completed": false
  }'
```

Получение всех задач

```bash
curl "http://localhost:8000/tasks/"
```

Фильтрация задач

```bash
# Только выполненные задачи
curl "http://localhost:8000/tasks/?completed=true"

# Поиск по названию
curl "http://localhost:8000/tasks/?search=FastAPI"
```

🗄 Структура проекта

```
it_project4/
├── 🐳 Dockerfile              # Конфигурация Docker
├── 🐳 docker-compose.yml      # Оркестрация контейнеров
├── 📋 requirements.txt        # Зависимости Python
├── 📁 app/                    # Исходный код приложения
│   ├── __init__.py
│   ├── main.py               # Основное приложение FastAPI
│   ├── schemas.py            # Pydantic схемы
│   ├── database.py           # Подключение к БД
│   ├── models.py             # SQLAlchemy модели
│   └── crud.py               # CRUD операции
├── 📁 tests/                  # Тесты
│   ├── __init__.py
│   ├── conftest.py           # Конфигурация pytest
│   └── test_main.py          # Модульные тесты API
└── 📄 README.md              # Документация
```

🧪 Тестирование

Запуск тестов

```bash
# Запуск всех тестов
docker-compose exec web pytest tests/ -v

# Запуск с покрытием кода
docker-compose exec web pytest tests/ --cov=app

# Запуск конкретного теста
docker-compose exec web pytest tests/test_main.py::test_create_task -v
```

Статистика тестов

· ✅ 10+ unit тестов
· ✅ Покрытие CRUD операций
· ✅ Тесты валидации данных
· ✅ Тесты граничных случаев

🔧 Разработка

Локальная разработка

```bash
# Установка зависимостей
pip install -r requirements.txt

# Запуск в режиме разработки
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Работа с базой данных

```bash
# Подключение к PostgreSQL
docker-compose exec db psql -U user -d taskdb

# Просмотр таблиц
\dt

# Просмотр данных
SELECT * FROM tasks;
```

🐳 Docker

Сборка образа

```bash
docker build -t task-manager-api .
```

Запуск контейнера

```bash
docker run -p 8000:8000 task-manager-api
```

📈 Мониторинг

Health check

```bash
curl http://localhost:8000/health
```

Ответ:

```json
{
  "status": "OK",
  "tasks_count": 5,
  "version": "1.0.0",
  "database": "PostgreSQL"
}
```

Статистика

```bash
curl http://localhost:8000/stats/
```

🤝 Участие в разработке

1. Форкните репозиторий
2. Создайте ветку для фичи (git checkout -b feature/amazing-feature)
3. Закоммитьте изменения (git commit -m 'Add amazing feature')
4. Запушите ветку (git push origin feature/amazing-feature)
5. Создайте Pull Request

📄 Лицензия

Этот проект является учебным и распространяется бесплатно.

👨‍💻 Автор

Max Kar

· GitHub: @Arhangel333

---

⭐ Не забудьте поставить звезду репозиторию, если проект был полезен!

```

## 🚀 **Как добавить README в проект:**

### **1. Создай файл:**
```bash
cat > README.md << 'EOF'
[вставь содержимое README выше]
EOF
```

2. Добавь и закоммить:

```bash
git add README.md
git commit -m "docs: Add comprehensive README.md"
```

3. Запуши:

```bash
git push origin main
```

🎯 Что даст README:

· ✅ Профессиональный вид проекта
· ✅ Понятную документацию для других разработчиков
· ✅ Инструкции по запуску и использованию
· ✅ Примеры API запросов
· ✅ Описание архитектуры

Добавляй README - это сделает проект завершённым и профессиональным! 🚀
