from django.core.management.base import BaseCommand
from django.utils import timezone
from apps.bot_data.models import BotUserEvent, BotCalculation, BotLead
import asyncio
import asyncpg
import json
import os
from datetime import datetime


class Command(BaseCommand):
    help = 'Синхронизирует данные из PostgreSQL бота в Django модели'

    def add_arguments(self, parser):
        parser.add_argument(
            '--db-url',
            type=str,
            help='URL подключения к PostgreSQL бота',
            default=os.environ.get('BOT_DATABASE_URL', 'postgresql://elma365:SecretPassword@master.sale.elewise.com:5000/geobotdb')
        )

    def handle(self, *args, **options):
        db_url = options['db_url']
        asyncio.run(self.sync_data(db_url))

    async def sync_data(self, db_url):
        """Синхронизация данных из PostgreSQL бота"""
        try:
            # Подключение к базе данных бота
            conn = await asyncpg.connect(db_url)
            
            self.stdout.write('Начинаем синхронизацию данных...')
            
            # Синхронизация UserEvent
            await self.sync_user_events(conn)
            
            # Синхронизация Calculation
            await self.sync_calculations(conn)
            
            # Синхронизация Lead
            await self.sync_leads(conn)
            
            await conn.close()
            self.stdout.write(
                self.style.SUCCESS('Синхронизация завершена успешно!')
            )
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Ошибка синхронизации: {e}')
            )

    async def sync_user_events(self, conn):
        """Синхронизация событий пользователей"""
        self.stdout.write('Синхронизация событий пользователей...')
        
        rows = await conn.fetch('''
            SELECT user_id, event_type, event_data, created_at 
            FROM user_events 
            ORDER BY created_at DESC
        ''')
        
        for row in rows:
            event_data = json.loads(row['event_data']) if row['event_data'] else {}
            
            BotUserEvent.objects.update_or_create(
                user_id=row['user_id'],
                event_type=row['event_type'],
                created_at=row['created_at'],
                defaults={
                    'event_data': event_data
                }
            )
        
        self.stdout.write(f'Синхронизировано {len(rows)} событий пользователей')

    async def sync_calculations(self, conn):
        """Синхронизация расчетов"""
        self.stdout.write('Синхронизация расчетов...')
        
        rows = await conn.fetch('''
            SELECT user_id, service_type, parameters, result, price, created_at 
            FROM calculations 
            ORDER BY created_at DESC
        ''')
        
        for row in rows:
            parameters = json.loads(row['parameters']) if row['parameters'] else {}
            
            BotCalculation.objects.update_or_create(
                user_id=row['user_id'],
                service_type=row['service_type'],
                created_at=row['created_at'],
                defaults={
                    'parameters': parameters,
                    'result': row['result'],
                    'price': row['price']
                }
            )
        
        self.stdout.write(f'Синхронизировано {len(rows)} расчетов')

    async def sync_leads(self, conn):
        """Синхронизация лидов"""
        self.stdout.write('Синхронизация лидов...')
        
        rows = await conn.fetch('''
            SELECT name, phone, email, company, service_type, calculated_price, source, created_at 
            FROM leads 
            ORDER BY created_at DESC
        ''')
        
        for row in rows:
            BotLead.objects.update_or_create(
                name=row['name'],
                phone=row['phone'],
                created_at=row['created_at'],
                defaults={
                    'email': row['email'],
                    'company': row['company'],
                    'service_type': row['service_type'],
                    'calculated_price': row['calculated_price'],
                    'source': row['source']
                }
            )
        
        self.stdout.write(f'Синхронизировано {len(rows)} лидов')
