FROM python:3.12-slim

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# Установка системных зависимостей для админки
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

# Создание директории для SSL сертификатов PostgreSQL
RUN mkdir -p /root/.cloud-certs && \
    curl -o /root/.cloud-certs/root.crt "https://st.timeweb.com/cloud-static/ca.crt" && \
    chmod 0600 /root/.cloud-certs/root.crt

ENV PGSSLROOTCERT=/root/.cloud-certs/root.crt

# Копирование pyproject.toml и установка пакета в режиме разработки
COPY app/admin/pyproject.toml .
COPY app/admin/ .
RUN pip install --no-cache-dir -e .

# Install Node.js modules, Webpack and Tailwind set up
RUN npm ci
RUN npm run build
RUN npx tailwindcss -i ./static/assets/style.css -o ./static/dist/css/output.css

# Manage Assets & DB
RUN python manage.py collectstatic --no-input
RUN python manage.py makemigrations
RUN python manage.py migrate

# gunicorn
CMD ["gunicorn", "--config", "gunicorn-cfg.py", "config.wsgi"]