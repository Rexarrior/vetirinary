#!/bin/bash
set -e

echo "Waiting for database..."

# Wait for PostgreSQL to be ready
while ! nc -z ${DB_HOST:-db} ${DB_PORT:-5432}; do
    echo "PostgreSQL is unavailable - sleeping"
    sleep 1
done

echo "PostgreSQL is up - continuing..."

# Run migrations
echo "Applying database migrations..."
python manage.py migrate --noinput

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Starting server..."
exec "$@"



