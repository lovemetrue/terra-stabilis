FROM python:3.12-slim

WORKDIR /app

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    curl \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Создание пользователя для безопасности
RUN useradd -m -u 1000 botuser && \
    mkdir -p /home/botuser/.cloud-certs && \
    chown -R botuser:botuser /app /home/botuser

# ✅ Копируем всю структуру проекта
COPY app ./app

# Переходим в директорию бота
WORKDIR /app/app/bot

# ✅ Устанавливаем пакет в режиме разработки (здесь уже точно есть pyproject.toml)
RUN pip install --no-cache-dir -e .

USER botuser

# Запуск бота
CMD ["python", "-c", "from app.bot.django_bot import main; main()"]