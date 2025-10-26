FROM python:3.12-slim

WORKDIR /app

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    curl \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Создание пользователя для безопасности
RUN useradd -m -u 1000 botuser

# SSL сертификаты для root и botuser
RUN mkdir -p /root/.cloud-certs && \
    curl -o /root/.cloud-certs/root.crt "https://st.timeweb.com/cloud-static/ca.crt" && \
    chmod 0600 /root/.cloud-certs/root.crt

# Создаем директорию для botuser и копируем сертификат
RUN mkdir -p /home/botuser/.cloud-certs && \
    cp /root/.cloud-certs/root.crt /home/botuser/.cloud-certs/root.crt && \
    chown -R botuser:botuser /home/botuser/.cloud-certs && \
    chmod 0600 /home/botuser/.cloud-certs/root.crt

# Копируем всю структуру проекта
COPY . .

# Переходим в директорию бота и устанавливаем пакет
WORKDIR /app/app/bot
RUN pip install --no-cache-dir -e .

# Возвращаемся в корень и устанавливаем PYTHONPATH
WORKDIR /app
ENV PYTHONPATH=/app

USER botuser

# Устанавливаем переменную окружения для SSL сертификата
ENV PGSSLROOTCERT=/home/botuser/.cloud-certs/root.crt

# Запуск бота
CMD ["python", "-c", "import asyncio; from app.bot.django_bot import main; asyncio.run(main())"]