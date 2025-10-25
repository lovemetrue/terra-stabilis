from django.contrib import admin
from django.utils.html import format_html
from .models import BotUser, BotUserEvent, BotCalculation, BotLead


@admin.register(BotUser)
class BotUserAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'username', 'first_name', 'last_name', 'phone', 'has_shared_contact', 'created_at']
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


@admin.register(BotLead)
class BotLeadAdmin(admin.ModelAdmin):
    list_display = ['user', 'service_type', 'calculated_price', 'get_phone', 'get_has_contact', 'is_converted', 'created_at']
    list_filter = ['service_type', 'is_converted', 'created_at']
    search_fields = ['user__first_name', 'user__last_name', 'user__username', 'user__phone', 'service_type']
    readonly_fields = ['created_at']
    date_hierarchy = 'created_at'
    list_per_page = 20
    list_editable = ['is_converted']

    def get_phone(self, obj):
        return obj.user.phone
    get_phone.short_description = 'Phone'

    def get_has_contact(self, obj):
        return obj.user.has_shared_contact
    get_has_contact.boolean = True
    get_has_contact.short_description = 'Has Contact'