# Этап 1: Сборка зависимостей
FROM python:3.12-slim AS builder

# Установите build-зависимости, включая PostgreSQL-клиент
RUN apt-get update \
    && apt-get install -y postgresql-client curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Установка Poetry через pip
RUN pip install poetry

# Копирование только pyproject.toml и poetry.lock для использования кэша Docker
WORKDIR /app
COPY pyproject.toml poetry.lock ./
RUN poetry config virtualenvs.create false \
    && poetry install --no-root --no-interaction --no-ansi

# Этап 2: Сборка финального образа
FROM python:3.12-slim

# Установите PostgreSQL-клиент во втором этапе
RUN apt-get update \
    && apt-get install -y postgresql-client \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Установка Poetry через pip
RUN pip install poetry

# Копирование зависимостей из builder-этапа
COPY --from=builder /usr/local /usr/local
COPY --from=builder /app /app

# Копирование оставшихся файлов проекта
WORKDIR /app
COPY src /app/src
COPY alembic.ini /app/
# COPY logging_config.yml /app/

# Создайте папку для логов
RUN mkdir -p /app/log

# Set default command to run `uvicorn`
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--forwarded-allow-ips", "*", "--proxy-headers", "--workers", "4"]
