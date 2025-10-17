FROM python:3.12-slim

WORKDIR /app

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Создание директории для SSL сертификатов
RUN mkdir -p /root/.cloud-certs && \
    curl -o /root/.cloud-certs/root.crt "https://st.timeweb.com/cloud-static/ca.crt" && \
    chmod 0600 /root/.cloud-certs/root.crt

ENV PGSSLROOTCERT=/root/.cloud-certs/root.crt

# Копирование requirements и установка зависимостей
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копирование кода приложения
COPY . .

# Создание пользователя для безопасности
RUN useradd -m -u 1000 botuser && chown -R botuser:botuser /app
USER botuser

# Запуск бота
CMD ["python", "-m", "app.bot.django_bot"]