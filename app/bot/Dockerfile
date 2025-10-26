FROM python:3.12-slim

WORKDIR /app

ENV SERVICE_TYPE=bot
ENV PGSSLROOTCERT=/app/.cloud-certs/root.crt

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    curl \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Создание пользователя для безопасности
RUN useradd -m -u 1000 botuser

# SSL сертификаты в единую директорию
RUN mkdir -p /app/.cloud-certs && \
    curl -o /app/.cloud-certs/root.crt "https://st.timeweb.com/cloud-static/ca.crt" && \
    chmod 0644 /app/.cloud-certs/root.crt

# Копируем всю структуру проекта
COPY . .

# Переходим в директорию бота и устанавливаем пакет
WORKDIR /app/app/bot
RUN pip install --no-cache-dir -e .

# Возвращаемся в корень и устанавливаем PYTHONPATH
WORKDIR /app
ENV PYTHONPATH=/app

# Даем права botuser на доступ к сертификату
RUN chown -R botuser:botuser /app/.cloud-certs

USER botuser

# Запуск бота
CMD ["python", "-c", "import asyncio; from app.bot.django_bot import main; asyncio.run(main())"]