from typing import Optional

from redis.asyncio import Redis

from app.config import settings


"""
Клиент Redis для использования хранилища состояний aiogram и кэширования.

Основано на официальной документации библиотеки `redis-py` (redis.asyncio)
и рекомендациях aiogram 3 по использованию `RedisStorage`.

Назначение:
- Предоставить единый экземпляр `Redis` для всего приложения.
- Подключение происходит по URL из переменной окружения `REDIS_URL`.

Формат URL (пример):
- redis://localhost:6379/0
- redis://:password@host:6379/1

Экспортируемые объекты:
- redis_client: асинхронный клиент Redis, готовый к использованию.
"""


def create_redis_client(url: Optional[str] = None) -> Redis:
    """
    Создаёт и настраивает асинхронный клиент Redis.

    Параметры:
    - url: строка подключения. Если не указана, используется `settings.REDIS_URL`.

    Возвращает:
    - Экземпляр `redis.asyncio.Redis` с включённой декодировкой ответов.
    """
    return Redis.from_url(url or settings.REDIS_URL, decode_responses=True)


redis_client: Redis = create_redis_client()

__all__ = ["redis_client", "create_redis_client"]


