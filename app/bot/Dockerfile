FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    curl \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -m -u 1000 botuser && \
    mkdir -p /home/botuser/.cloud-certs && \
    chown -R botuser:botuser /app /home/botuser

# копируем всю папку app, чтобы модуль app был виден
COPY app/ ./app

WORKDIR /app/bot

RUN pip install --no-cache-dir -e .

USER botuser

CMD ["python", "-c", "from app.bot.django_bot import main; main()"]