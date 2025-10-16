# check_db.py
import os
import django
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

try:
    django.setup()

    from django.db import connection

    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT version();")
            version = cursor.fetchone()
            print(f"Database version: {version}")

        print("Database connection successful!")
    except Exception as e:
        print(f"Database connection failed: {e}")

except Exception as e:
    print(f"Django setup failed: {e}")