from django.contrib import admin
from .models import BotUser, BotUserEvent, BotCalculation, BotPotentialLead, BotLead


@admin.register(BotUser)
class BotUserAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'username', 'first_name', 'last_name', 'has_shared_contact', 'created_at']
    list_filter = ['has_shared_contact', 'created_at']
    search_fields = ['user_id', 'username', 'first_name', 'last_name', 'phone']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'created_at'
    list_per_page = 20


@admin.register(BotUserEvent)
class BotUserEventAdmin(admin.ModelAdmin):
    list_display = ['user', 'event_type', 'created_at']
    list_filter = ['event_type', 'created_at']
    search_fields = ['user__user_id', 'user__username', 'user__first_name', 'event_type']
    readonly_fields = ['created_at']
    date_hierarchy = 'created_at'
    list_per_page = 20


@admin.register(BotCalculation)
class BotCalculationAdmin(admin.ModelAdmin):
    list_display = ['user', 'service_type', 'price', 'created_at']
    list_filter = ['service_type', 'created_at']
    search_fields = ['user__user_id', 'user__username', 'service_type']
    readonly_fields = ['created_at']
    date_hierarchy = 'created_at'
    list_per_page = 20


@admin.register(BotPotentialLead)
class BotPotentialLeadAdmin(admin.ModelAdmin):
    list_display = ['tg_name', 'first_name', 'last_name', 'service_type', 'calculated_price', 'created_at']
    list_filter = ['service_type', 'created_at']
    search_fields = ['tg_name', 'first_name', 'last_name', 'service_type']
    readonly_fields = ['created_at']
    date_hierarchy = 'created_at'
    list_per_page = 20

    def has_add_permission(self, request):
        """Запрещаем ручное добавление потенциальных лидов"""
        return False

    def has_change_permission(self, request, obj=None):
        """Запрещаем изменение потенциальных лидов"""
        return False


@admin.register(BotLead)
class BotLeadAdmin(admin.ModelAdmin):
    list_display = ['user', 'service_type', 'calculated_price', 'has_contact', 'is_converted', 'created_at']
    list_filter = ['service_type', 'is_converted', 'created_at']
    search_fields = ['user__first_name', 'user__last_name', 'user__username', 'service_type']
    readonly_fields = ['created_at']
    date_hierarchy = 'created_at'
    list_per_page = 20
    list_editable = ['is_converted']

    def has_contact(self, obj):
        return obj.user.has_shared_contact

    has_contact.boolean = True
    has_contact.short_description = 'Есть контакт'

#
# class DashboardAdmin(admin.ModelAdmin):
#     """Кастомная страница дашборда для быстрого доступа к статистике"""
#
#     def has_add_permission(self, request):
#         return False
#
#     def has_change_permission(self, request, obj=None):
#         return False
#
#     def has_delete_permission(self, request, obj=None):
#         return False


# # Опционально: если хотите добавить кастомное представление для дашборда в админке
# from django.urls import path
# from django.shortcuts import render
# from django.db.models import Count, Q
# from django.utils import timezone
# from datetime import timedelta
#
#
# def bot_dashboard_view(request):
#     """Кастомный дашборд для админки"""
#     # Статистика пользователей
#     total_users = BotUser.objects.count()
#     users_with_contact = BotUser.objects.filter(has_shared_contact=True).count()
#
#     # Статистика расчетов
#     total_calculations = BotCalculation.objects.count()
#
#     # Статистика лидов
#     total_potential_leads = BotPotentialLead.objects.count()
#     total_leads = BotLead.objects.count()
#     converted_leads = BotLead.objects.filter(is_converted=True).count()
#
#     # Активность за последние 7 дней
#     seven_days_ago = timezone.now() - timedelta(days=7)
#
#     recent_calculations = BotCalculation.objects.filter(
#         created_at__gte=seven_days_ago
#     ).count()
#
#     recent_leads = BotLead.objects.filter(
#         created_at__gte=seven_days_ago
#     ).count()
#
#     # Популярные услуги
#     popular_services = BotCalculation.objects.values('service_type').annotate(
#         count=Count('id')
#     ).order_by('-count')[:5]
#
#     context = {
#         'total_users': total_users,
#         'users_with_contact': users_with_contact,
#         'total_calculations': total_calculations,
#         'total_potential_leads': total_potential_leads,
#         'total_leads': total_leads,
#         'converted_leads': converted_leads,
#         'recent_calculations': recent_calculations,
#         'recent_leads': recent_leads,
#         'popular_services': popular_services,
#         **admin.site.each_context(request)
#     }
#
#     return render(request, 'admin/bot_dashboard.html', context)
#
#
# # Добавляем кастомный URL в админку
# def get_admin_urls():
#     from django.urls import path
#     return [
#         path('bot_dashboard/', admin.site.admin_view(bot_dashboard_view), name='bot_dashboard'),
#     ]
#
#
# admin.site.get_urls = lambda: get_admin_urls() + admin.site.get_urls()