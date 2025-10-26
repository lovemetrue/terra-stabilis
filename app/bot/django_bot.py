import os
import sys
import django
import asyncio
import logging
from pathlib import Path

# Для бота используем путь доступный botuser, для админки - общий путь
if os.getenv('SERVICE_TYPE') == 'bot':
    SSL_CERT_PATH = '/app/.cloud-certs/root.crt'
else:
    SSL_CERT_PATH = '/app/.cloud-certs/root.crt'  # Единый путь для всех

print(f"🔍 Checking SSL certificate at: {SSL_CERT_PATH}")

try:
    if not Path(SSL_CERT_PATH).exists():
        print(f"❌ SSL certificate not found at: {SSL_CERT_PATH}")
        print("Available files in /app:")
        for item in Path('/app').rglob('*'):
            if item.is_file():
                print(f"  - {item}")
        sys.exit(1)
    else:
        print(f"✅ SSL certificate found: {SSL_CERT_PATH}")
        # Проверяем права доступа
        stat_info = Path(SSL_CERT_PATH).stat()
        print(f"✅ Certificate permissions: {oct(stat_info.st_mode)}")
        print(f"✅ Certificate owner: {stat_info.st_uid}")

except PermissionError as e:
    print(f"❌ Permission denied for SSL certificate: {e}")
    print(f"Current user: {os.getuid()}")
    print("Trying to list /app/.cloud-certs/ directory:")
    try:
        for item in Path('/app/.cloud-certs').iterdir():
            print(f"  - {item}")
    except Exception as list_error:
        print(f"  Cannot list directory: {list_error}")
    sys.exit(1)

# Добавляем корневую директорию проекта в Python path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(PROJECT_ROOT))

# Теперь добавляем путь к папке admin, чтобы Django мог найти приложения в папке apps
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