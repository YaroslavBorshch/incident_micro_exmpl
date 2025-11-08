#!/bin/bash
set -e

echo "Waiting for PostgreSQL to be ready..."
until pg_isready -h postgres -U root -d incidents_db; do
  sleep 1
done

echo "PostgreSQL is ready!"

if [ "${APPLY_MIGRATIONS}" = "true" ]; then
  echo "Applying database migrations..."
  alembic upgrade head
  echo "Migrations applied successfully!"
fi

echo "Starting application..."
exec "$@"

