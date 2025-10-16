import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage

from app.config import settings
from app.bot.handlers import start
from app.bot.middlewares.django_middleware import DatabaseMiddleware
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
    
    # Регистрация единственного роутера с обработчиками
    dp.include_router(start.router)
    
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
