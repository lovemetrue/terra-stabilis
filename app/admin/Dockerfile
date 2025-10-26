# Stage 1: Node.js build stage
FROM node:18-alpine as node-builder

WORKDIR /build

# Копируем package files
COPY app/admin/package*.json ./
COPY app/admin/package-lock.json* ./

# Устанавливаем зависимости и собираем статику
RUN npm ci
COPY app/admin/ ./
RUN npm run build
RUN npx tailwindcss -i ./static/assets/style.css -o ./static/dist/css/output.css

# Stage 2: Python runtime stage
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PGSSLROOTCERT=/root/.cloud-certs/root.crt

WORKDIR /app

# Установка системных зависимостей для Python
RUN apt-get update && apt-get install -y \
    curl \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Создание директории для SSL сертификатов PostgreSQL
RUN mkdir -p /root/.cloud-certs && \
    curl -o /root/.cloud-certs/root.crt "https://st.timeweb.com/cloud-static/ca.crt" && \
    chmod 0600 /root/.cloud-certs/root.crt

# Копирование requirements и установка зависимостей Python
COPY app/admin/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копирование исходного кода админки
COPY app/admin/ .

# Копирование собранных статических файлов из node-builder stage
COPY --from=node-builder /build/static/dist ./static/dist
COPY --from=node-builder /build/package-lock.json ./
COPY --from=node-builder /build/node_modules ./node_modules

# Manage Assets & DB
RUN python manage.py collectstatic --no-input
RUN python manage.py makemigrations
RUN python manage.py migrate

# Создание пользователя для безопасности
RUN useradd -m -u 1000 webuser && chown -R webuser:webuser /app
USER webuser

# gunicorn
CMD ["gunicorn", "--config", "gunicorn-cfg.py", "config.wsgi"]