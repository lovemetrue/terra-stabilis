# admin/apps/bot_data/management/commands/check_and_fix_bot_data.py
from django.core.management.base import BaseCommand
from django.db import transaction
from apps.bot_data.models import BotUser, BotUserEvent, BotCalculation, BotLead, BotPotentialLead


class Command(BaseCommand):
    help = 'Check and fix all bot data relationships'

    def handle(self, *args, **options):
        self.stdout.write("🔍 Checking bot data integrity...")

        with transaction.atomic():
            # 1. Проверяем и создаем недостающих пользователей
            self.fix_missing_users()

            # 2. Проверяем и исправляем связи
            self.fix_broken_relationships()

            # 3. Статистика
            self.show_statistics()

    def fix_missing_users(self):
        """Создаем пользователей для записей с user_id_backup"""
        # Для событий
        events_without_user = BotUserEvent.objects.filter(user__isnull=True)
        for event in events_without_user:
            if event.user_id_backup:
                user, created = BotUser.objects.get_or_create(
                    user_id=event.user_id_backup,
                    defaults={'first_name': 'Auto-created from event'}
                )
                event.user = user
                event.save()
                if created:
                    self.stdout.write(f'✅ Created user {user.user_id} for event {event.id}')

        # Для расчетов
        calculations_without_user = BotCalculation.objects.filter(user__isnull=True)
        for calc in calculations_without_user:
            if calc.user_id_backup:
                user, created = BotUser.objects.get_or_create(
                    user_id=calc.user_id_backup,
                    defaults={'first_name': 'Auto-created from calculation'}
                )
                calc.user = user
                calc.save()
                if created:
                    self.stdout.write(f'✅ Created user {user.user_id} for calculation {calc.id}')

        # Для лидов
        leads_without_user = BotLead.objects.filter(user__isnull=True)
        for lead in leads_without_user:
            if lead.user_id_backup:
                user, created = BotUser.objects.get_or_create(
                    user_id=lead.user_id_backup,
                    defaults={'first_name': 'Auto-created from lead'}
                )
                lead.user = user
                lead.save()
                if created:
                    self.stdout.write(f'✅ Created user {user.user_id} for lead {lead.id}')

    def fix_broken_relationships(self):
        """Исправляем несоответствия в user_id_backup"""
        # Проверяем события
        for event in BotUserEvent.objects.filter(user__isnull=False):
            if event.user_id_backup != event.user.user_id:
                event.user_id_backup = event.user.user_id
                event.save()
                self.stdout.write(f'🔄 Fixed user_id_backup for event {event.id}')

        # Проверяем расчеты
        for calc in BotCalculation.objects.filter(user__isnull=False):
            if calc.user_id_backup != calc.user.user_id:
                calc.user_id_backup = calc.user.user_id
                calc.save()
                self.stdout.write(f'🔄 Fixed user_id_backup for calculation {calc.id}')

        # Проверяем лиды
        for lead in BotLead.objects.filter(user__isnull=False):
            if lead.user_id_backup != lead.user.user_id:
                lead.user_id_backup = lead.user.user_id
                lead.save()
                self.stdout.write(f'🔄 Fixed user_id_backup for lead {lead.id}')

    def show_statistics(self):
        """Показываем статистику"""
        stats = {
            'Total Users': BotUser.objects.count(),
            'Users with contact': BotUser.objects.filter(has_shared_contact=True).count(),
            'User Events': BotUserEvent.objects.count(),
            'Events without user': BotUserEvent.objects.filter(user__isnull=True).count(),
            'Calculations': BotCalculation.objects.count(),
            'Calculations without user': BotCalculation.objects.filter(user__isnull=True).count(),
            'Leads': BotLead.objects.count(),
            'Leads without user': BotLead.objects.filter(user__isnull=True).count(),
            'Potential Leads': BotPotentialLead.objects.count(),
        }

        self.stdout.write("\n📊 Final Statistics:")
        for key, value in stats.items():
            self.stdout.write(f"   {key}: {value}")

        # Проверяем целостность
        broken_events = BotUserEvent.objects.filter(user__isnull=True).count()
        broken_calculations = BotCalculation.objects.filter(user__isnull=True).count()
        broken_leads = BotLead.objects.filter(user__isnull=True).count()

        if broken_events + broken_calculations + broken_leads == 0:
            self.stdout.write(self.style.SUCCESS("✅ All data relationships are intact!"))
        else:
            self.stdout.write(self.style.WARNING(
                f"⚠️  Still have {broken_events + broken_calculations + broken_leads} broken relationships"))