import asyncio
import os
import sys

# Добавляем путь к проекту для импортов
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from sqlalchemy.ext.asyncio import create_async_engine
from app.database.models import Base
from app.config import settings


async def init_database():
    """Создание таблиц для бота"""
    engine = create_async_engine(settings.DATABASE_URL, echo=True)

    async with engine.begin() as conn:
        print("Создание таблиц для бота...")
        await conn.run_sync(Base.metadata.create_all)
        print("Таблицы успешно созданы!")


if __name__ == "__main__":
    asyncio.run(init_database())