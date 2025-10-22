# bot_data/views.py

from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Count, Q, Avg
from django.utils import timezone
from datetime import timedelta, datetime
from .models import BotUserEvent, BotCalculation, BotLead
from django.contrib.auth.decorators import login_required


@login_required
def bot_dashboard(request):
    """Дашборд статистики бота с серверным рендерингом"""
    print("🔍 Загрузка данных для дашборда...")  # Отладочное сообщение

    # Основные метрики
    total_calculations = BotCalculation.objects.count()
    total_logins = BotUserEvent.objects.filter(event_type='login').count()
    total_leads = BotLead.objects.count()
    total_events = BotUserEvent.objects.count()

    print(f"📊 Метрики: расчеты={total_calculations}, входы={total_logins}, лиды={total_leads}, события={total_events}")

    # Статистика по услугам для графиков (последние 30 дней)
    thirty_days_ago = datetime.now() - timedelta(days=30)

    services_data = BotCalculation.objects.filter(created_at__gte=thirty_days_ago) \
        .exclude(service_type__isnull=True) \
        .values('service_type') \
        .annotate(count=Count('id')) \
        .order_by('-count')

    print(f"📈 Услуги по расчетам: {list(services_data)}")

    # Статистика по лидам
    lead_services_data = BotLead.objects.filter(created_at__gte=thirty_days_ago) \
        .exclude(service_type__isnull=True) \
        .values('service_type') \
        .annotate(count=Count('id')) \
        .order_by('-count')

    print(f"👥 Услуги по лидам: {list(lead_services_data)}")

    # Активность за 7 дней
    seven_days_ago = datetime.now() - timedelta(days=7)
    activity_data = BotUserEvent.objects.filter(created_at__gte=seven_days_ago) \
        .extra({'date': "date(created_at)"}) \
        .values('date') \
        .annotate(count=Count('id')) \
        .order_by('date')

    print(f"📅 Активность: {list(activity_data)}")

    # Словарь для перевода названий услуг
    SERVICE_NAMES_RU = {
        "program_development": "Разработка программы",
        "mapping": "Геотехническое картирование",
        "core_documentation": "Документирование керна",
        "2d_ogr": "2D расчет (ОГР)",
        "2d_pgr": "2D расчет (ПГР)",
        "3d_ogr": "3D расчет (ОГР)",
        "3d_pgr": "3D расчет (ПГР)",
        "geomechanic": "Геомеханик на час",
        "georadar": "Георадарный мониторинг",
        "prism": "Призменный мониторинг",
        "geodata_collection": "Сбор геоданных",
        "stability_calculation": "Расчет устойчивости",
        "monitoring": "Мониторинг"
    }

    # Переводим названия услуг для расчетов
    services_translated = {}
    for service in services_data:
        ru_name = SERVICE_NAMES_RU.get(service['service_type'], service['service_type'])
        services_translated[ru_name] = service['count']

    # Переводим названия услуг для лидов
    lead_services_translated = {}
    for service in lead_services_data:
        ru_name = SERVICE_NAMES_RU.get(service['service_type'], service['service_type'])
        lead_services_translated[ru_name] = service['count']

    # Форматируем активность
    activity_formatted = []
    for item in activity_data:
        activity_formatted.append({
            'date': item['date'].strftime('%Y-%m-%d'),
            'count': item['count']
        })

    # Заполняем пропущенные дни
    today = datetime.now().date()
    full_activity = []
    for i in range(7):
        date = today - timedelta(days=6 - i)
        date_str = date.strftime('%Y-%m-%d')
        activity_for_date = next((item for item in activity_formatted if item['date'] == date_str), None)
        full_activity.append({
            'date': date_str,
            'count': activity_for_date['count'] if activity_for_date else 0
        })

    print(f"🎯 Final data - Services: {services_translated}")
    print(f"🎯 Final data - Leads: {lead_services_translated}")
    print(f"🎯 Final data - Activity: {full_activity}")

    context = {
        'parent': 'bot_data',
        'segment': 'bot_dashboard',
        'total_calculations': total_calculations,
        'total_logins': total_logins,
        'total_leads': total_leads,
        'total_events': total_events,
        'services_data': services_translated,
        'lead_services_data': lead_services_translated,
        'activity_data': full_activity,
    }

    return render(request, 'bot_data/dashboard.html', context)

@login_required
def bot_stats_api(request):
    """API для dashboard - возвращает JSON с данными"""

    # Период для статистики (последние 7 дней)
    seven_days_ago = datetime.now() - timedelta(days=7)

    # Общее количество расчетов
    total_calculations = BotCalculation.objects.count()

    # Количество входов (события типа 'login')
    total_logins = BotUserEvent.objects.filter(event_type='start').count()

    # Популярные услуги по расчетам
    services_data = BotCalculation.objects.exclude(service_type__isnull=True) \
        .values('service_type') \
        .annotate(count=Count('id')) \
        .order_by('-count')

    services_dict = {item['service_type']: item['count'] for item in services_data}

    # Популярные услуги по лидам
    lead_services_data = BotLead.objects.exclude(service_type__isnull=True) \
        .values('service_type') \
        .annotate(count=Count('id')) \
        .order_by('-count')

    lead_services_dict = {item['service_type']: item['count'] for item in lead_services_data}

    # Активность за 7 дней (события по дням)
    activity_data = BotUserEvent.objects.filter(created_at__gte=seven_days_ago) \
        .extra({'date': "date(created_at)"}) \
        .values('date') \
        .annotate(count=Count('id')) \
        .order_by('date')

    # Форматируем даты для графика
    activity_formatted = []
    for item in activity_data:
        activity_formatted.append({
            'date': item['date'].strftime('%Y-%m-%d'),
            'count': item['count']
        })

    # Заполняем пропущенные дни нулями
    today = datetime.now().date()
    full_activity = []
    for i in range(7):
        date = today - timedelta(days=6 - i)  # от 6 дней назад до сегодня
        date_str = date.strftime('%Y-%m-%d')

        # Ищем данные для этой даты
        activity_for_date = next((item for item in activity_formatted if item['date'] == date_str), None)
        full_activity.append({
            'date': date_str,
            'count': activity_for_date['count'] if activity_for_date else 0
        })

    response_data = {
        'total_calculations': total_calculations,
        'total_logins': total_logins,
        'services': services_dict,
        'lead_services': lead_services_dict,
        'activity_7d': full_activity,
        'total_leads': BotLead.objects.count(),
        'total_events': BotUserEvent.objects.count(),
    }

    return JsonResponse(response_data)



@login_required
def bot_leads(request):
    leads = BotLead.objects.all().order_by('-created_at')
    context = {
        'parent': 'bot_data',
        'segment': 'bot_leads',
        'leads': leads
    }
    return render(request, 'bot_data/leads.html', context)

@login_required
def bot_events(request):
    events = BotUserEvent.objects.all().order_by('-created_at')
    context = {
        'parent': 'bot_data',
        'segment': 'bot_events',
        'events': events
    }
    return render(request, 'bot_data/events.html', context)

@login_required
def bot_calculations(request):
    calculations = BotCalculation.objects.all().order_by('-created_at')
    context = {
        'parent': 'bot_data',
        'segment': 'bot_calculations',
        'calculations': calculations
    }
    return render(request, 'bot_data/calculations.html', context)

@login_required
def bot_analytics(request):
    # Аналитика по услугам
    service_stats = BotLead.objects.exclude(service_type__isnull=True)\
                                   .values('service_type')\
                                   .annotate(
                                       count=Count('id'),
                                       avg_price=Avg('calculated_price')
                                   )\
                                   .order_by('-count')
    
    # Статистика по дням
    thirty_days_ago = datetime.now() - timedelta(days=30)
    daily_leads = BotLead.objects.filter(created_at__gte=thirty_days_ago)\
                                .extra({'date': "date(created_at)"})\
                                .values('date')\
                                .annotate(count=Count('id'))\
                                .order_by('date')
    
    context = {
        'parent': 'bot_data',
        'segment': 'bot_analytics',
        'service_stats': service_stats,
        'daily_leads': daily_leads
    }
    return render(request, 'bot_data/analytics.html', context)

def bot_stats_api(request):
    """
    API эндпоинт для получения статистики бота.
    Возвращает JSON с агрегированными данными.
    """
    # Общее количество расчетов
    total_calculations = BotCalculation.objects.count()
    
    # Количество входов (события типа 'login')
    total_logins = BotUserEvent.objects.filter(event_type='login').count()
    
    # Разбивка по типам услуг (расчеты)
    service_breakdown = BotCalculation.objects.values('service_type').annotate(
        count=Count('id')
    ).order_by('-count')
    services = {item['service_type'] or 'unknown': item['count'] for item in service_breakdown}
    
    # Разбивка по типам услуг (лиды)
    leads_breakdown = BotLead.objects.values('service_type').annotate(
        count=Count('id')
    ).order_by('-count')
    lead_services = {item['service_type'] or 'unknown': item['count'] for item in leads_breakdown}
    
    # Активность за последние 7 дней
    seven_days_ago = timezone.now() - timedelta(days=6)
    activity_7d = []
    for i in range(7):
        date = seven_days_ago + timedelta(days=i)
        count = BotCalculation.objects.filter(
            created_at__date=date.date()
        ).count()
        activity_7d.append({
            'date': date.strftime('%Y-%m-%d'),
            'count': count
        })
    
    return JsonResponse({
        'total_calculations': total_calculations,
        'total_logins': total_logins,
        'services': services,
        'lead_services': lead_services,
        'activity_7d': activity_7d,
    })


# Добавьте в views.py для аналитики
@login_required
def bot_analytics(request):
    # Аналитика по услугам
    service_stats = BotLead.objects.exclude(service_type__isnull=True) \
        .values('service_type') \
        .annotate(
        count=Count('id'),
        avg_price=Avg('calculated_price')
    ) \
        .order_by('-count')

    # Статистика по дням (последние 7 дней)
    seven_days_ago = datetime.now() - timedelta(days=7)
    daily_leads = BotLead.objects.filter(created_at__gte=seven_days_ago) \
        .extra({'date': "date(created_at)"}) \
        .values('date') \
        .annotate(count=Count('id')) \
        .order_by('date')

    # Дополнительная статистика
    leads_count = BotLead.objects.count()
    events_count = BotUserEvent.objects.count()
    avg_price = BotLead.objects.exclude(calculated_price__isnull=True) \
                    .aggregate(avg=Avg('calculated_price'))['avg'] or 0

    context = {
        'parent': 'bot_data',
        'segment': 'bot_analytics',
        'service_stats': service_stats,
        'daily_leads': daily_leads,
        'daily_leads_max': max([day['count'] for day in daily_leads] or [0]),
        'leads_count': leads_count,
        'events_count': events_count,
        'avg_price': avg_price,
        'peak_hour': '14:00'  # Заглушка, можно вычислить реальное значение
    }
    return render(request, 'bot_data/analytics.html', context)

def bot_dashboard(request):
    """
    Дашборд с статистикой бота.
    """
    context = {
        'title': 'Статистика Telegram бота'
    }
    return render(request, 'bot_data/dashboard.html', context)
