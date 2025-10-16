#!/bin/bash

# create_project.sh

set -e

PROJECT_NAME="geo-engineering-bot"

echo "Создание структуры проекта: $PROJECT_NAME"

# Создание основной структуры директорий
mkdir -p $PROJECT_NAME/{app/{bot/{handlers,middlewares,keyboards},database,admin/{templates,static/{css,js}},services,web},migrations/versions,tests/{unit,integration}}

# Создание файлов
cd $PROJECT_NAME

# Основные файлы
touch app/__init__.py
touch app/main.py
touch app/config.py

# Бот
touch app/bot/__init__.py
touch app/bot/states.py
touch app/bot/utils.py

touch app/bot/handlers/__init__.py
touch app/bot/handlers/start.py
touch app/bot/handlers/qualification.py
touch app/bot/handlers/contacts.py
touch app/bot/handlers/common.py

touch app/bot/middlewares/__init__.py
touch app/bot/middlewares/database.py

touch app/bot/keyboards/__init__.py
touch app/bot/keyboards/main_menu.py

# База данных
touch app/database/__init__.py
touch app/database/base.py
touch app/database/models.py
touch app/database/crud.py
touch app/database/session.py
touch app/database/redis_client.py

# Админ-панель
touch app/admin/__init__.py
touch app/admin/panel.py
touch app/admin/routes.py

# Шаблоны админ-панели
touch app/admin/templates/base.html
touch app/admin/templates/leads.html
touch app/admin/templates/stats.html
touch app/admin/templates/dialogs.html

# Сервисы
touch app/services/__init__.py
touch app/services/lead_service.py
touch app/services/analytics.py

# Веб
touch app/web/__init__.py
touch app/web/server.py

# Миграции
touch migrations/env.py
touch migrations/script.py.mako

# Тесты
touch tests/__init__.py
touch tests/unit/__init__.py
touch tests/unit/test_handlers.py
touch tests/unit/test_services.py
touch tests/integration/__init__.py
touch tests/integration/test_bot_flow.py

# Конфигурационные файлы
touch docker-compose.yml
touch Dockerfile
touch .env.example
touch requirements.txt
touch alembic.ini

# Создание базового содержимого для ключевых файлов

# main.py
cat > app/main.py << 'EOF'
import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage

from app.config import settings
from app.bot.handlers import start, qualification, contacts, common
from app.bot.middlewares.database import DatabaseMiddleware
from app.database.session import async_session
from app.database.redis_client import redis_client
from app.web.server import start_web_server

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def main():
    # Инициализация бота
    storage = RedisStorage(redis=redis_client)
    bot = Bot(token=settings.BOT_TOKEN)
    dp = Dispatcher(storage=storage)
    
    # Middleware
    dp.update.middleware(DatabaseMiddleware(async_session))
    
    # Регистрация роутеров
    dp.include_router(start.router)
    dp.include_router(qualification.router)
    dp.include_router(contacts.router)
    dp.include_router(common.router)
    
    # Запуск веб-сервера для админ-панели
    web_task = asyncio.create_task(start_web_server())
    
    # Запуск бота
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()
        web_task.cancel()

if __name__ == "__main__":
    asyncio.run(main())
EOF

# config.py
cat > app/config.py << 'EOF'
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    BOT_TOKEN: str
    DATABASE_URL: str
    REDIS_URL: str = "redis://redis:6379/0"
    ADMIN_PORT: int = 8000
    ADMIN_USERNAME: str = "admin"
    ADMIN_PASSWORD: str = "admin123"
    
    class Config:
        env_file = ".env"

settings = Settings()
EOF

# docker-compose.yml
cat > docker-compose.yml << 'EOF'
version: '3.8'

services:
  app:
    build: .
    ports:
      - "8000:8000"  # Админ-панель
    depends_on:
      - redis
    environment:
      - DATABASE_URL=${DATABASE_URL}
      - REDIS_URL=redis://redis:6379/0
      - BOT_TOKEN=${BOT_TOKEN}
    restart: unless-stopped
    volumes:
      - ./logs:/app/logs

  redis:
    image: redis:7-alpine
    command: redis-server --appendonly yes
    volumes:
      - redis_data:/data
    restart: unless-stopped

volumes:
  redis_data:
EOF

# requirements.txt
cat > requirements.txt << 'EOF'
aiogram==3.10.0
sqlalchemy==2.0.23
alembic==1.13.1
asyncpg==0.29.0
redis==5.0.1
pydantic==2.5.3
pydantic-settings==2.1.0
python-dotenv==1.0.0
aiohttp==3.9.1
jinja2==3.1.3
uvicorn==0.24.0
fastapi==0.104.1

# Dev
pytest==7.4.3
pytest-asyncio==0.21.1
pytest-cov==4.1.0
black==23.11.0
isort==5.13.2
EOF

# .env.example
cat > .env.example << 'EOF'
BOT_TOKEN=your_telegram_bot_token_here
DATABASE_URL=postgresql+asyncpg://user:password@host:5432/database
REDIS_URL=redis://redis:6379/0
ADMIN_PORT=8000
ADMIN_USERNAME=admin
ADMIN_PASSWORD=admin123
EOF

echo "Структура проекта создана успешно!"
echo "Не забудьте:"
echo "1. Создать виртуальное окружение"
echo "2. Установить зависимости: pip install -r requirements.txt"
echo "3. Создать файл .env и заполнить переменные"
echo "4. Запустить миграции: alembic upgrade head"
echo "5. Запустить проект: docker-compose up"
