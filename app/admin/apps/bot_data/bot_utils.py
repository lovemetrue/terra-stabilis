import os
import django
from django.utils import timezone

# Настройка Django для использования в боте
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from asgiref.sync import sync_to_async
from admin.apps.bot_data.models import BotUser, BotUserEvent, BotCalculation, BotPotentialLead, BotLead


@sync_to_async
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


@sync_to_async
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


@sync_to_async
def save_calculation(user_id: int, service_type: str, parameters: dict,
                     result: str, price: float, user_data: dict = None):
    """
    Сохранить расчет и создать потенциального лида
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

    # Создаем потенциального лида (даже если контакт не отправлен)
    # Формируем tg_name для уникальности
    tg_name_parts = []
    if user_data and user_data.get('first_name'):
        tg_name_parts.append(user_data['first_name'])
    if user_data and user_data.get('last_name'):
        tg_name_parts.append(user_data['last_name'])
    if user_data and user_data.get('username'):
        tg_name_parts.append(f"(@{user_data['username']})")

    tg_name = " ".join(tg_name_parts) if tg_name_parts else f"User {user_id}"

    # Проверяем, нет ли уже такого потенциального лида
    potential_lead_exists = BotPotentialLead.objects.filter(
        tg_name=tg_name,
        service_type=service_type
    ).exists()

    if not potential_lead_exists:
        BotPotentialLead.objects.create(
            tg_name=tg_name,
            first_name=user_data.get('first_name') if user_data else None,
            last_name=user_data.get('last_name') if user_data else None,
            service_type=service_type,
            calculated_price=price,
            source="telegram"
        )

    return calculation


@sync_to_async
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

    # Обновляем дополнительные данные если переданы
    if user_data.get('contact_name'):
        # Разделяем имя и фамилию если нужно
        name_parts = user_data['contact_name'].split(' ', 1)
        user.first_name = name_parts[0]
        if len(name_parts) > 1:
            user.last_name = name_parts[1]

    user.save()

    return user


@sync_to_async
def save_full_lead(user_id: int, service_type: str, calculated_price: float,
                   contact_data: dict, user_data: dict = None):
    """
    Сохранить полный лид с контактами
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

    # Обновляем контактные данные пользователя
    if contact_data.get('phone'):
        user.phone = contact_data['phone']
        user.has_shared_contact = True

    if contact_data.get('name'):
        name_parts = contact_data['name'].split(' ', 1)
        user.first_name = name_parts[0]
        if len(name_parts) > 1:
            user.last_name = name_parts[1]

    user.save()

    # Создаем запись лида
    lead = BotLead.objects.create(
        user=user,
        service_type=service_type,
        calculated_price=calculated_price
    )

    return lead


@sync_to_async
def get_user_potential_leads_count(tg_name: str) -> int:
    """
    Получить количество потенциальных лидов для пользователя
    """
    return BotPotentialLead.objects.filter(tg_name=tg_name).count()