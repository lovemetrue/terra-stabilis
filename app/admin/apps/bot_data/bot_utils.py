import os
import django
from django.utils import timezone
from django.db import transaction
import re

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from asgiref.sync import sync_to_async
from apps.bot_data.models import BotUser, BotUserEvent, BotCalculation, BotLead


def validate_email(email: str) -> bool:
    """Проверка email адреса"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def format_user_data_for_confirmation(user_data: dict) -> str:
    """Форматирование данных пользователя для подтверждения"""
    lines = []

    if user_data.get('name'):
        lines.append(f"👤 Имя: {user_data['name']}")

    if user_data.get('phone'):
        lines.append(f"📱 Телефон: {user_data['phone']}")

    if user_data.get('email'):
        lines.append(f"📧 Email: {user_data['email']}")
    else:
        lines.append("📧 Email: не указан")

    if user_data.get('organization'):
        lines.append(f"🏢 Организация: {user_data['organization']}")
    else:
        lines.append("🏢 Организация: не указана")

    return "\n".join(lines)


@sync_to_async
def get_or_create_bot_user(user_id: int, username: str = None, first_name: str = None, last_name: str = None):
    """Создает или получает пользователя"""
    with transaction.atomic():
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
def save_user_event(user_id: int, event_type: str, event_data: dict = None, username: str = None,
                    first_name: str = None, last_name: str = None):
    """Сохраняет событие пользователя"""
    with transaction.atomic():
        # Сначала получаем или создаем пользователя
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

        # Создаем событие
        return BotUserEvent.objects.create(
            user=user,
            event_type=event_type,
            event_data=event_data or {}
        )


@sync_to_async
def save_calculation(user_id: int, service_type: str, parameters: dict, result: str, price: float, username: str = None,
                     first_name: str = None, last_name: str = None):
    """Сохраняет расчет"""
    with transaction.atomic():
        # Сначала получаем или создаем пользователя
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

        # Создаем расчет
        return BotCalculation.objects.create(
            user=user,
            service_type=service_type,
            parameters=parameters,
            result=result,
            price=price
        )


@sync_to_async
def save_contact(user_id: int, phone: str = None, name: str = None, email: str = None, organization: str = None,
                 username: str = None, first_name: str = None, last_name: str = None):
    """Сохраняет контакт пользователя с email и организацией"""
    with transaction.atomic():
        # Сначала получаем или создаем пользователя
        user, created = BotUser.objects.get_or_create(
            user_id=user_id,
            defaults={
                'username': username,
                'first_name': first_name,
                'last_name': last_name,
            }
        )

        # Обновляем данные пользователя
        update_fields = []

        # Обновляем основные данные
        if username and user.username != username:
            user.username = username
            update_fields.append('username')
        if first_name and user.first_name != first_name:
            user.first_name = first_name
            update_fields.append('first_name')
        if last_name and user.last_name != last_name:
            user.last_name = last_name
            update_fields.append('last_name')

        # Обновляем контактные данные
        if phone:
            user.phone = phone
            user.has_shared_contact = True
            update_fields.extend(['phone', 'has_shared_contact'])

        if email:
            user.email = email
            user.has_provided_email = True
            update_fields.extend(['email', 'has_provided_email'])

        if organization:
            user.organization = organization
            user.has_provided_organization = True
            update_fields.extend(['organization', 'has_provided_organization'])

        # Если передано полное имя, разбиваем его
        if name and not (first_name or last_name):
            name_parts = name.split(' ', 1)
            user.first_name = name_parts[0]
            update_fields.append('first_name')
            if len(name_parts) > 1:
                user.last_name = name_parts[1]
                update_fields.append('last_name')

        if update_fields:
            user.save(update_fields=update_fields)

        return user


@sync_to_async
def update_user_contact_info(user_id: int, **kwargs):
    """Обновляет контактную информацию пользователя"""
    with transaction.atomic():
        try:
            user = BotUser.objects.get(user_id=user_id)
            update_fields = []

            for field, value in kwargs.items():
                if value is not None and hasattr(user, field):
                    setattr(user, field, value)
                    update_fields.append(field)

                    # Устанавливаем соответствующие флаги
                    if field == 'phone' and value:
                        user.has_shared_contact = True
                        update_fields.append('has_shared_contact')
                    elif field == 'email' and value:
                        user.has_provided_email = True
                        update_fields.append('has_provided_email')
                    elif field == 'organization' and value:
                        user.has_provided_organization = True
                        update_fields.append('has_provided_organization')

            if update_fields:
                user.save(update_fields=update_fields)

            return user
        except BotUser.DoesNotExist:
            return None


@sync_to_async
def save_lead(user_id: int, service_type: str, calculated_price: float, username: str = None, first_name: str = None,
              last_name: str = None):
    """Сохраняет лид"""
    with transaction.atomic():
        # Сначала получаем или создаем пользователя
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

        # Создаем лид
        return BotLead.objects.create(
            user=user,
            service_type=service_type,
            calculated_price=calculated_price
        )


@sync_to_async
def get_user_completion_status(user_id: int):
    """Получает статус заполнения профиля пользователя"""
    try:
        user = BotUser.objects.get(user_id=user_id)
        completed = 0
        total = 3  # телефон, email, организация

        if user.phone:
            completed += 1
        if user.email:
            completed += 1
        if user.organization:
            completed += 1

        return {
            'completed': completed,
            'total': total,
            'percentage': int((completed / total) * 100) if total > 0 else 0,
            'has_phone': bool(user.phone),
            'has_email': bool(user.email),
            'has_organization': bool(user.organization)
        }
    except BotUser.DoesNotExist:
        return {
            'completed': 0,
            'total': 3,
            'percentage': 0,
            'has_phone': False,
            'has_email': False,
            'has_organization': False
        }


@sync_to_async
def get_user_stats():
    """Получает статистику пользователей"""
    total_users = BotUser.objects.count()
    users_with_contact = BotUser.objects.filter(has_shared_contact=True).count()
    users_with_email = BotUser.objects.filter(has_provided_email=True).count()
    users_with_organization = BotUser.objects.filter(has_provided_organization=True).count()
    total_events = BotUserEvent.objects.count()
    total_calculations = BotCalculation.objects.count()
    total_leads = BotLead.objects.count()
    converted_leads = BotLead.objects.filter(is_converted=True).count()

    return {
        'total_users': total_users,
        'users_with_contact': users_with_contact,
        'users_with_email': users_with_email,
        'users_with_organization': users_with_organization,
        'total_events': total_events,
        'total_calculations': total_calculations,
        'total_leads': total_leads,
        'converted_leads': converted_leads,
    }


@sync_to_async
def get_service_stats():
    """Получает статистику по услугам"""
    from django.db.models import Count, Avg

    # Популярные услуги по расчетам
    calculation_services = BotCalculation.objects.values('service_type').annotate(
        count=Count('id'),
        avg_price=Avg('price')
    ).order_by('-count')

    # Популярные услуги по лидам
    lead_services = BotLead.objects.values('service_type').annotate(
        count=Count('id'),
        avg_price=Avg('calculated_price')
    ).order_by('-count')

    return {
        'calculation_services': list(calculation_services),
        'lead_services': list(lead_services),
    }


@sync_to_async
def get_user_by_id(user_id: int):
    """Получает пользователя по ID"""
    try:
        return BotUser.objects.get(user_id=user_id)
    except BotUser.DoesNotExist:
        return None