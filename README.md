# FastAPI Application

Простое REST API-приложение на FastAPI с тестированием через pytest.

## Функциональности

- CRUD операции для работы с данными
- Автоматическая документация Swagger (/docs)
- Валидация данных через Pydantic
- Тестирование с использованием pytest

## Установка и запуск

1. Клонируйте репозиторий:
```bash
git clone https://github.com/OrneysOriginal/CRUD_task_manager.git
cd CRUD_task_manager
```
2. Запустите приложение в докере
```bash
docker compose up -d
```
Или
2. Создайте виртуальное окружение и активируйте его
```bash
python -m venv venv
source venv/bin/activate  # Linux/MacOS
# или
venv\Scripts\activate.bat  # Windows
```
3. Установите зависимости
```bash
pip install -r requirements.txt
```
4. Запустите миграции
```bash
alembic upgrade head
```
5. Запустите приложение
```bash
uvicorn src.main:app --reload
```
## Тестирование
```bash
# Все тесты
pytest tests/

# С покрытием кода
pytest --cov=src tests/
```
