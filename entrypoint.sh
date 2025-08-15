#!/bin/sh
set -e

: "${DB_HOST:=db}"
: "${DB_PORT:=5432}"
: "${PORT:=8000}"

echo "Waiting for database $DB_HOST:$DB_PORT ..."

# wait until db is reachable (uses netcat from Dockerfile)
while ! nc -z "$DB_HOST" "$DB_PORT" >/dev/null 2>&1; do
  echo "  -> waiting for postgres..."
  sleep 1
done

echo "Postgres reachable."

# optional: run alembic migrations if alembic present
if [ -f "alembic.ini" ]; then
  echo "Running alembic upgrade head ..."
  alembic upgrade head || echo "alembic upgrade failed (continuing)"
fi

# start uvicorn
exec uvicorn main:app --host 0.0.0.0 --port "$PORT" --proxy-headers
