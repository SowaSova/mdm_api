#!/bin/sh
set -e

# Ожидаем, пока PostgreSQL станет доступен.
until pg_isready -h ${POSTGRES_HOST:-db} -p ${POSTGRES_PORT:-5432} -U ${POSTGRES_USER}; do
  echo "PostgreSQL недоступен - ждем..."
  sleep 1
done
echo "PostgreSQL доступен."

# Применяем миграции через Alembic.
echo "Запуск миграций Alembic..."
alembic upgrade head

# Запускаем uvicorn.
echo "Старт приложения через Uvicorn..."
exec uvicorn src.main:app --host 0.0.0.0 --port 8000 --forwarded-allow-ips "*" --proxy-headers --workers 4
