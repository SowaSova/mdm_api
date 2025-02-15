# Этап 1: Сборка зависимостей
FROM python:3.12-slim AS builder

RUN apt-get update \
    && apt-get install -y postgresql-client curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN pip install poetry

WORKDIR /app
COPY pyproject.toml poetry.lock ./
RUN poetry config virtualenvs.create false \
    && poetry install --no-root --no-interaction --no-ansi

# Последний этап сборки
FROM python:3.12-slim

RUN apt-get update \
    && apt-get install -y postgresql-client \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN pip install poetry

COPY --from=builder /usr/local /usr/local
COPY --from=builder /app /app

WORKDIR /app
COPY src /app/src
COPY alembic.ini /app/

RUN mkdir -p /app/log

# Копируем entrypoint-скрипт и делаем его исполняемым.
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Создаем нового пользователя и назначаем ему права
RUN adduser --disabled-password --gecos "" appuser \
    && chown -R appuser:appuser /app

# Переключаемся на непредельного пользователя
USER appuser

ENTRYPOINT ["/app/entrypoint.sh"]

