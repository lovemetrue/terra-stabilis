from django.db import models
from django.utils import timezone


class BotUser(models.Model):
    """Пользователи бота - все, кто взаимодействовал с ботом"""
    user_id = models.BigIntegerField(
        unique=True,
        db_index=True,
        help_text="ID пользователя в Telegram"
    )
    username = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        db_index=True,
        help_text="@username в Telegram"
    )
    first_name = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Имя"
    )
    last_name = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Фамилия"
    )
    phone = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        db_index=True,
        help_text="Телефон"
    )
    has_shared_contact = models.BooleanField(
        default=False,
        help_text="Поделился контактом"
    )
    created_at = models.DateTimeField(
        default=timezone.now,
        help_text="Время первого взаимодействия"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Время последнего обновления"
    )

    class Meta:
        db_table = 'bot_users'
        ordering = ['-created_at']
        verbose_name = 'Пользователь бота'
        verbose_name_plural = 'Пользователи бота'

    def __str__(self):
        name_parts = []
        if self.first_name:
            name_parts.append(self.first_name)
        if self.last_name:
            name_parts.append(self.last_name)
        if self.username:
            name_parts.append(f"(@{self.username})")

        name = " ".join(name_parts) if name_parts else f"User {self.user_id}"
        return name

    def save(self, *args, **kwargs):
        """Переопределяем save для логики обновления контакта"""
        if self.phone and not self.has_shared_contact:
            self.has_shared_contact = True
        super().save(*args, **kwargs)


class BotUserEvent(models.Model):
    """События пользователей в Telegram боте"""
    user = models.ForeignKey(
        BotUser,
        on_delete=models.CASCADE,
        related_name='events',
        db_index=True
    )
    event_type = models.CharField(
        max_length=100,
        db_index=True,
        help_text="Тип события"
    )
    event_data = models.JSONField(
        default=dict,
        help_text="Данные события в JSON"
    )
    created_at = models.DateTimeField(
        default=timezone.now,
        help_text="Время создания"
    )

    class Meta:
        db_table = 'bot_user_events'
        ordering = ['-created_at']
        verbose_name = 'Событие бота'
        verbose_name_plural = 'События бота'

    def __str__(self):
        return f"Event {self.event_type} for {self.user}"


class BotCalculation(models.Model):
    """Расчеты услуг в боте"""
    user = models.ForeignKey(
        BotUser,
        on_delete=models.CASCADE,
        related_name='calculations',
        db_index=True
    )
    service_type = models.CharField(
        max_length=200,
        db_index=True,
        help_text="Тип услуги"
    )
    parameters = models.JSONField(
        default=dict,
        help_text="Параметры расчета"
    )
    result = models.TextField(
        help_text="Результат расчета"
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Цена"
    )
    created_at = models.DateTimeField(
        default=timezone.now,
        help_text="Время создания"
    )

    class Meta:
        db_table = 'bot_calculations'
        ordering = ['-created_at']
        verbose_name = 'Расчет бота'
        verbose_name_plural = 'Расчеты бота'

    def __str__(self):
        return f"Calculation {self.id}: {self.service_type} - {self.price} руб."


class BotLead(models.Model):
    """Лиды (клиенты) из бота"""
    user = models.ForeignKey(
        BotUser,
        on_delete=models.CASCADE,
        related_name='leads',
        db_index=True
    )
    service_type = models.CharField(
        max_length=200,
        db_index=True,
        help_text="Тип услуги"
    )
    calculated_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Рассчитанная цена"
    )
    is_converted = models.BooleanField(
        default=False,
        db_index=True,
        help_text="Стал клиентом"
    )
    notes = models.TextField(
        blank=True,
        null=True,
        help_text="Заметки менеджера"
    )
    created_at = models.DateTimeField(
        default=timezone.now,
        help_text="Время создания"
    )

    class Meta:
        db_table = 'bot_leads'
        ordering = ['-created_at']
        verbose_name = 'Лид бота'
        verbose_name_plural = 'Лиды бота'

    def __str__(self):
        status = "Converted" if self.is_converted else "Lead"
        return f"{status}: {self.user} - {self.service_type}"

    @property
    def has_contact(self):
        return self.user.has_shared_contact

    @property
    def phone(self):
        return self.user.phone

    @property
    def username(self):
        return self.user.username

    @property
    def first_name(self):
        return self.user.first_name

    @property
    def last_name(self):
        return self.user.last_name