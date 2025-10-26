FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    curl \
    gcc \
    python3-dev \
    gnupg \
    && rm -rf /var/lib/apt/lists/*

# Установка Node.js 18
RUN mkdir -p /etc/apt/keyrings && \
    curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key | gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg && \
    echo "deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_18.x nodistro main" > /etc/apt/sources.list.d/nodesource.list && \
    apt-get update && apt-get install -y nodejs npm

# SSL сертификаты PostgreSQL
RUN mkdir -p /root/.cloud-certs && \
    curl -o /root/.cloud-certs/root.crt "https://st.timeweb.com/cloud-static/ca.crt" && \
    chmod 0600 /root/.cloud-certs/root.crt

ENV PGSSLROOTCERT=/root/.cloud-certs/root.crt

# Копируем только админку
COPY app/admin/ .

# Устанавливаем зависимости
RUN pip install --no-cache-dir .

# Node.js зависимости и сборка
RUN npm ci
RUN npm run build
RUN npx tailwindcss -i ./static/assets/style.css -o ./static/dist/css/output.css

# Миграции и статика
RUN python manage.py collectstatic --no-input
RUN python manage.py makemigrations
RUN python manage.py migrate

CMD ["gunicorn", "--config", "gunicorn-cfg.py", "config.wsgi"]