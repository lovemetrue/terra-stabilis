import os
import sys
import django
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(PROJECT_ROOT))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.rocket-django-main.config.settings')

try:
    django.setup()
    print("✅ Django настроен успешно!")

    # Проверяем импорт моделей
    from apps.bot_data.models import BotLead, BotUserEvent, BotCalculation

    print("✅ Модели импортированы успешно!")

    # Проверяем доступ к базе данных
    lead_count = BotLead.objects.count()
    print(f"✅ Доступ к БД: {lead_count} лидов")

except Exception as e:
    print(f"❌ Ошибка: {e}")
    import traceback

    traceback.print_exc()