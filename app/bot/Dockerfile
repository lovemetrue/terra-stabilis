FROM python:3.12-slim

WORKDIR /app

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    curl \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Создание пользователя для безопасности
RUN useradd -m -u 1000 botuser && mkdir -p /home/botuser/.cloud-certs && chown -R botuser:botuser /app/home/botuser

# Копирование requirements и установка зависимостей
COPY app/bot/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копирование исходного кода бота
COPY app/bot/ .

USER botuser

# Запуск бота
CMD ["python", "-m", "app.bot.django_bot"]