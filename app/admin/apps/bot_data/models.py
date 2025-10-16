from django.db import models
from django.utils import timezone


class BotUserEvent(models.Model):
    """
    События пользователей в Telegram боте.
    Соответствует модели UserEvent из SQLAlchemy.
    """
    user_id = models.BigIntegerField(help_text="ID пользователя в Telegram")
    event_type = models.CharField(max_length=100, db_index=True, help_text="Тип события")
    event_data = models.JSONField(default=dict, help_text="Данные события в JSON")
    created_at = models.DateTimeField(default=timezone.now, help_text="Время создания")

    class Meta:
        db_table = 'bot_user_events'
        ordering = ['-created_at']

    def __str__(self):
        return f"User {self.user_id}: {self.event_type}"


class BotCalculation(models.Model):
    """
    Расчеты услуг в боте.
    Соответствует модели Calculation из SQLAlchemy.
    """
    user_id = models.BigIntegerField(help_text="ID пользователя в Telegram")
    service_type = models.CharField(max_length=200, help_text="Тип услуги")
    parameters = models.JSONField(default=dict, help_text="Параметры расчета")
    result = models.TextField(help_text="Результат расчета")
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Цена")
    created_at = models.DateTimeField(default=timezone.now, help_text="Время создания")

    class Meta:
        db_table = 'bot_calculations'
        ordering = ['-created_at']

    def __str__(self):
        return f"Calculation {self.id}: {self.service_type} - {self.price} руб."


class BotLead(models.Model):
    """
    Лиды (потенциальные клиенты) из бота.
    Соответствует модели Lead из SQLAlchemy.
    """
    name = models.CharField(max_length=200, help_text="Имя клиента")
    phone = models.CharField(max_length=50, help_text="Телефон")
    email = models.EmailField(blank=True, null=True, help_text="Email")
    company = models.CharField(max_length=200, blank=True, null=True, help_text="Компания")
    service_type = models.CharField(max_length=200, blank=True, null=True, help_text="Тип услуги")
    calculated_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, help_text="Рассчитанная цена")
    source = models.CharField(max_length=50, default="telegram", help_text="Источник")
    created_at = models.DateTimeField(default=timezone.now, help_text="Время создания")

    class Meta:
        db_table = 'bot_leads'
        ordering = ['-created_at']

    def __str__(self):
        return f"Lead: {self.name} - {self.service_type}"
