# admin/apps/bot_data/management/commands/fix_bot_data.py
from django.core.management.base import BaseCommand
from django.db import transaction
from apps.bot_data.models import BotUserEvent, BotCalculation, BotLead, BotUser

class Command(BaseCommand):
    help = 'Fix bot data by creating missing users and linking records'

    def handle(self, *args, **options):
        with transaction.atomic():
            # 1. Создаем пользователей для событий
            events_without_user = BotUserEvent.objects.filter(user__isnull=True)
            for event in events_without_user:
                if hasattr(event, 'user_id_backup'):
                    user, created = BotUser.objects.get_or_create(
                        user_id=event.user_id_backup,
                        defaults={'first_name': 'Auto-created'}
                    )
                    event.user = user
                    event.save()
                    self.stdout.write(f'Fixed event {event.id} with user {user.user_id}')

            # 2. Создаем пользователей для расчетов
            calculations_without_user = BotCalculation.objects.filter(user__isnull=True)
            for calc in calculations_without_user:
                if hasattr(calc, 'user_id_backup'):
                    user, created = BotUser.objects.get_or_create(
                        user_id=calc.user_id_backup,
                        defaults={'first_name': 'Auto-created'}
                    )
                    calc.user = user
                    calc.save()
                    self.stdout.write(f'Fixed calculation {calc.id} with user {user.user_id}')

            # 3. Создаем пользователей для лидов
            leads_without_user = BotLead.objects.filter(user__isnull=True)
            for lead in leads_without_user:
                if hasattr(lead, 'user_id_backup'):
                    user, created = BotUser.objects.get_or_create(
                        user_id=lead.user_id_backup,
                        defaults={'first_name': 'Auto-created'}
                    )
                    lead.user = user
                    lead.save()
                    self.stdout.write(f'Fixed lead {lead.id} with user {user.user_id}')

        self.stdout.write(self.style.SUCCESS('Successfully fixed bot data'))