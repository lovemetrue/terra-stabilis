import os
import django
from django.utils import timezone

# Настройка Django для использования в боте
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from admin.apps.bot_data.models import BotUser, BotUserEvent, BotCalculation, BotLead


def get_or_create_bot_user(user_id: int, username: str = None,
                           first_name: str = None, last_name: str = None) -> BotUser:
    """
    Получить или создать пользователя бота
    """
    user, created = BotUser.objects.get_or_create(
        user_id=user_id,
        defaults={
            'username': username,
            'first_name': first_name,
            'last_name': last_name,
        }
    )

    # Обновляем данные, если они изменились
    if not created:
        update_fields = []
        if username and user.username != username:
            user.username = username
            update_fields.append('username')
        if first_name and user.first_name != first_name:
            user.first_name = first_name
            update_fields.append('first_name')
        if last_name and user.last_name != last_name:
            user.last_name = last_name
            update_fields.append('last_name')

        if update_fields:
            user.save(update_fields=update_fields)

    return user


def save_user_event(user_id: int, event_type: str, event_data: dict = None,
                    username: str = None, first_name: str = None, last_name: str = None):
    """
    Сохранить событие пользователя
    """
    user = get_or_create_bot_user(user_id, username, first_name, last_name)

    BotUserEvent.objects.create(
        user=user,
        event_type=event_type,
        event_data=event_data or {}
    )


def save_calculation(user_id: int, service_type: str, parameters: dict,
                     result: str, price: float, user_data: dict = None):
    """
    Сохранить расчет и создать лид
    """
    if user_data:
        user = get_or_create_bot_user(
            user_id=user_id,
            username=user_data.get('username'),
            first_name=user_data.get('first_name'),
            last_name=user_data.get('last_name')
        )
    else:
        user = BotUser.objects.get(user_id=user_id)

    # Сохраняем расчет
    calculation = BotCalculation.objects.create(
        user=user,
        service_type=service_type,
        parameters=parameters,
        result=result,
        price=price
    )

    # Создаем лид (даже если контакт не отправлен)
    lead, created = BotLead.objects.get_or_create(
        user=user,
        service_type=service_type,
        calculated_price=price,
        defaults={'created_at': timezone.now()}
    )

    return calculation


def save_contact(user_id: int, phone: str, user_data: dict):
    """
    Сохранить контакт пользователя
    """
    user = get_or_create_bot_user(
        user_id=user_id,
        username=user_data.get('username'),
        first_name=user_data.get('first_name'),
        last_name=user_data.get('last_name')
    )

    user.phone = phone
    user.has_shared_contact = True
    user.save()

    return user