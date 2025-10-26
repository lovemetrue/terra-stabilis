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

# Копирование pyproject.toml и установка пакета в режиме разработки
COPY app/bot/pyproject.toml .
COPY app/bot/ .
RUN pip install --no-cache-dir -e .

USER botuser

# Запуск бота через установленный пакет
CMD ["python", "-c", "from app.bot.django_bot import main; main()"]