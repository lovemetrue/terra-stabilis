from django.contrib import admin
from .models import BotUserEvent, BotCalculation, BotLead


@admin.register(BotUserEvent)
class BotUserEventAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'event_type', 'created_at']
    list_filter = ['event_type', 'created_at']
    search_fields = ['user_id', 'event_type']
    readonly_fields = ['created_at']
    date_hierarchy = 'created_at'


@admin.register(BotCalculation)
class BotCalculationAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'service_type', 'price', 'created_at']
    list_filter = ['service_type', 'created_at']
    search_fields = ['user_id', 'service_type']
    readonly_fields = ['created_at']
    date_hierarchy = 'created_at'


@admin.register(BotLead)
class BotLeadAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'service_type', 'calculated_price', 'created_at']
    list_filter = ['service_type', 'source', 'created_at']
    search_fields = ['name', 'phone', 'email', 'company']
    readonly_fields = ['created_at']
    date_hierarchy = 'created_at'
