# admin/config/database.py
import os
import asyncpg
from django.conf import settings


async def create_pool():
    """Создает пул подключений для aiogram"""
    db_config = settings.DATABASES['default']

    ssl = None
    if db_config.get('OPTIONS', {}).get('sslmode') != 'disable':
        ssl = {
            'ssl': True,
            'sslmode': db_config['OPTIONS'].get('sslmode', 'require'),
        }

        # Добавляем сертификаты если есть
        for cert_type in ['sslrootcert', 'sslcert', 'sslkey']:
            if cert_type in db_config.get('OPTIONS', {}):
                ssl[cert_type] = db_config['OPTIONS'][cert_type]

    return await asyncpg.create_pool(
        user=db_config['USER'],
        password=db_config['PASSWORD'],
        database=db_config['NAME'],
        host=db_config['HOST'],
        port=db_config['PORT'],
        ssl=ssl
    )