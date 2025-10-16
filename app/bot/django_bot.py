import os
import sys
import django
import asyncio
import logging
from pathlib import Path

# Добавляем корневую директорию проекта в Python path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(PROJECT_ROOT))

# Теперь добавляем путь к папке rocket-django-main, чтобы Django мог найти приложения в папке apps
ROCKET_DJANGO_ROOT = PROJECT_ROOT / "app" / "admin"
sys.path.append(str(ROCKET_DJANGO_ROOT))

# Настраиваем Django с правильным модулем настроек
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

try:
    django.setup()
    print("✅ Django успешно настроен с модулем: config.settings")
except Exception as e:
    print(f"❌ Ошибка настройки Django: {e}")
    import traceback

    traceback.print_exc()
    sys.exit(1)

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage

# Импортируем после настройки Django
from app.config import settings
from app.bot.handlers import start, qualification, contacts, common
from app.bot.middlewares.django_middleware import DjangoMiddleware
from app.database.redis_client import redis_client

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def main():
    # Инициализация бота
    storage = RedisStorage(redis=redis_client)
    bot = Bot(token=settings.BOT_TOKEN)
    dp = Dispatcher(storage=storage)

    # Middleware для Django
    dp.update.middleware(DjangoMiddleware())

    # Регистрация роутеров
    dp.include_router(start.router)
    dp.include_router(qualification.router)
    dp.include_router(contacts.router)
    dp.include_router(common.router)

    # Запуск бота
    try:
        logger.info("🚀 Starting Telegram Bot with Django ORM...")
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"❌ Bot error: {e}")
    finally:
        await bot.session.close()
        await redis_client.close()


if __name__ == "__main__":
    asyncio.run(main())