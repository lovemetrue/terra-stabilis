import os
import django
from django.utils import timezone
from django.db import transaction

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from asgiref.sync import sync_to_async
from apps.bot_data.models import BotUser, BotUserEvent, BotCalculation, BotLead


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
def save_contact(user_id: int, phone: str, name: str = None, username: str = None, first_name: str = None,
                 last_name: str = None):
    """Сохраняет контакт пользователя"""
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
        user.phone = phone
        user.has_shared_contact = True

        # Если передано полное имя, разбиваем его
        if name:
            name_parts = name.split(' ', 1)
            user.first_name = name_parts[0]
            if len(name_parts) > 1:
                user.last_name = name_parts[1]
        # Или используем отдельные поля
        elif first_name:
            user.first_name = first_name
        elif last_name:
            user.last_name = last_name

        user.save()
        return user


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
def get_user_stats():
    """Получает статистику пользователей"""
    total_users = BotUser.objects.count()
    users_with_contact = BotUser.objects.filter(has_shared_contact=True).count()
    total_events = BotUserEvent.objects.count()
    total_calculations = BotCalculation.objects.count()
    total_leads = BotLead.objects.count()
    converted_leads = BotLead.objects.filter(is_converted=True).count()

    return {
        'total_users': total_users,
        'users_with_contact': users_with_contact,
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