from django.apps import AppConfig


class BotDataConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.bot_data'
    verbose_name = 'Данные Telegram бота'
